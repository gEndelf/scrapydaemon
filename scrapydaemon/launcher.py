# -*- coding: utf-8 -*-

import sys
import redis
from datetime import datetime
from multiprocessing import cpu_count
from scrapyd.launcher import ScrapyProcessProtocol, Launcher

from twisted.internet import reactor, defer, protocol, error
from twisted.application.service import Service
from twisted.python import log

from scrapy.utils.python import stringify_dict
from scrapyd.utils import get_crawl_args
from scrapyd import __version__
from scrapyd.interfaces import IPoller, IEnvironment
from scrapydaemon import redis_utils


class BookieoddsLauncher(Launcher):

    name = 'launcher'

    def __init__(self, config, app):
        Launcher.__init__(self, config, app)
        self.config = config
        self.redis_connecton = redis.StrictRedis(host=config.get('REDIS_HOST'),
                                                 port=config.get('REDIS_PORT'),
                                                 db=0,
                                                 password=config.get(
                                                     'REDIS_PASSWORD', ''))

    def startService(self):
        for slot in range(self.max_proc):
            self._wait_for_project(slot)
        log.msg(format='Scrapyd %(version)s started: max_proc=%(max_proc)r, runner=%(runner)r',
                version=__version__, max_proc=self.max_proc,
                runner=self.runner, system='Launcher')

    def _wait_for_project(self, slot):
        poller = self.app.getComponent(IPoller)
        poller.next().addCallback(self._spawn_process, slot)

    def _spawn_process(self, message, slot):
        msg = stringify_dict(message, keys_only=False)
        project = msg['_project']
        args = [sys.executable, '-m', self.runner, 'crawl']
        args += get_crawl_args(msg)
        e = self.app.getComponent(IEnvironment)
        env = e.get_environment(msg, slot)
        env = stringify_dict(env, keys_only=False)
        pp = ScrapyProcessProtocol(slot, project, msg['_spider'],
                                   msg['_job'], env)
        pp.deferred.addBoth(self._process_finished, slot)
        reactor.spawnProcess(pp, sys.executable, args=args, env=env)
        self.processes[slot] = pp

    def _process_finished(self, _, slot):
        process = self.processes.pop(slot)
        process.end_time = datetime.now()
        self.finished.append(process)
        del self.finished[:-self.finished_to_keep] # keep last 100 finished jobs

        print (">> Task finished!")
        redis_utils.finish_task(self.redis_connecton, self.config, process.job)

        self._wait_for_project(slot)

    def _get_max_proc(self, config):
        max_proc = config.getint('max_proc', 0)
        if not max_proc:
            try:
                cpus = cpu_count()
            except NotImplementedError:
                cpus = 1
            max_proc = cpus * config.getint('max_proc_per_cpu', 4)
        return max_proc


