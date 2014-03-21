# -*- coding: utf-8 -*-


def build_instance_redis_key(config):
    return '%s:%s' % (config.get('SCRAPYD_TASK_KEY'),
                      config.get('SCRAPYD_INSTANCE'))


def finish_task(redis, config, job_id):
    redis_key = build_instance_redis_key(config)
    redis.hdel(redis_key, job_id)


def schedule_task(redis, config, job_id, spider_name, spider_args):
    task_key = '%s:%s' % (spider_name, str(spider_args))
    redis_key = build_instance_redis_key(config)
    redis.hset(redis_key, job_id, task_key)
