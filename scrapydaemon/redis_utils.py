# -*- coding: utf-8 -*-


def build_instance_redis_key(config):
    return '%s:%s' % (config.get('SCRAPYD_TASK_KEY'),
                      config.get('SCRAPYD_INSTANCE'))


def build_task_key(spider_name, spider_args):
    return '%s:%s' % (spider_name, str(spider_args))


def finish_task(redis, config, job_id):
    redis_key = build_instance_redis_key(config)
    redis.hdel(redis_key, job_id)


def schedule_task(redis, config, job_id, spider_name, spider_args):
    task_key = build_task_key(spider_name, spider_args)
    redis_key = build_instance_redis_key(config)
    redis.hset(redis_key, job_id, task_key)


def is_spider_blocked(redis, spider_name, spider_args):
    task_key = build_task_key(spider_name, spider_args)
    return redis.sismember('Spider:Blocked', task_key)
