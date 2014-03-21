scrapydaemon
============

## Scrapyd customization

```
[settings]
default = bookiespiders.settings

[scrapyd]
logs_dir    = logs
http_port   = 6800
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

Package should be installed to virtual env., which is working with scrapyd

```
pip install -e [path to this package]
```