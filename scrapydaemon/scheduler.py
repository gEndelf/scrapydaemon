import redis
from zope.interface import implements
from scrapyd.interfaces import ISpiderScheduler
from scrapyd.scheduler import SpiderScheduler

from scrapydaemon import redis_utils


class BookieoddsSpiderScheduler(SpiderScheduler):
    """
    settings keys:
    SCRAPYD_TASK_KEY = 'ScrapydTasks:%s'
    SCRAPYD_INSTANCE = [unique instance name]
    REDIS_HOST
    REDIS_PORT
    REDIS_PASSWORD
    """
    implements(ISpiderScheduler)

    def __init__(self, config):
        SpiderScheduler.__init__(self, config)
        self.redis_connecton = redis.StrictRedis(host=config.get('REDIS_HOST'),
                                                 port=config.get('REDIS_PORT'),
                                                 db=0,
                                                 password=config.get(
                                                     'REDIS_PASSWORD', ''))

    def schedule(self, project, spider_name, **spider_args):
        clean_spider_args = self._cleanup_spider_args(spider_args)
        if redis_utils.is_spider_blocked(self.redis_connecton, spider_name, clean_spider_args):
            print "Spider %s was blocked, task will not be scheduled" % spider_name
            return

        q = self.queues[project]
        q.add(spider_name, **spider_args)

        redis_utils.schedule_task(self.redis_connecton,
                                  self.config,
                                  job_id=spider_args['_job'],
                                  spider_name=spider_name,
                                  spider_args=clean_spider_args)

    def _cleanup_spider_args(self, spider_args):
        """
        remove system spider arguments
        """
        return {k: v for k, v in spider_args.items() if
                k not in ('_job', 'settings', )}
