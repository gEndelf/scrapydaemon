scrapydaemon
============
This is patch for scrapyd, which allows you monitoring active scrapyd tasks.
If you have several instances - all of them will manage tasks states in redis

## Scrapyd customization

scrapy config

```
[scrapyd]
eggs_dir    = eggs
logs_dir    = logs
items_dir   = items
jobs_to_keep = 5
dbs_dir     = dbs
max_proc    = 0
max_proc_per_cpu = 4
finished_to_keep = 100
http_port   = 6800
debug       = off
application = scrapydaemon.app.application
launcher    = scrapydaemon.launcher.BookieoddsLauncher
SCRAPYD_TASK_KEY = ScrapydTasks
SCRAPYD_INSTANCE = instance_1
REDIS_HOST = 127.0.0.1
REDIS_PORT = 6379
```

What was added:
* custom app (**scrapydaemon.app.application**)
* custom launcher (**scrapydaemon.launcher.BookieoddsLauncher**)
* SCRAPYD_INSTANCE (unique scrapyd instance name - used as complex key for redis)
* SCRAPYD_TASK_KEY - used as complex key for redis (ScrapydTasks:instance_1)

Redis connection config
* REDIS_HOST = 127.0.0.1
* REDIS_PORT = 6379


## Installation

Package should be installed to virtual env, which is working with scrapyd

```
pip install -e [path to this package]
```
