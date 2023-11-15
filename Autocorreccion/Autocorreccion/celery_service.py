from os import truncate
import sys
from pymongo import MongoClient
from datetime import datetime, date
from celery import Celery, shared_task, current_task
from celery import app, chain, current_task, group, shared_task

from pathlib import Path
from re import search
import copy
from celery.schedules import crontab
import sys
from pathlib import Path
var_default_directory = str(Path(Path.cwd().parent))
sys.path.append(var_default_directory)
sys.path.append(var_default_directory+'/')
from .basicconfig import *


var_default_directory = str(Path(Path.cwd()))
print("Directory by command", var_default_directory)
sys.path.append(var_default_directory)

app = Celery('Autocorreccion', backend='rpc://', broker='amqp://ufinet:ufinet.2020@10.40.6.67//')
#app = Celery('Autocorreccion', backend='rpc://', broker='amqp://guest:guest@127.0.0.1//')
app.conf.task_default_queue = 'autocorrect'
app.conf.broker_heartbeat = '60'
app.conf.task_ignore_result = True
app.autodiscover_tasks(["Autocorreccion"])
app.conf.task_routes = {
                        'Autocorreccion.code.basicconfig.procces_communities': {'queue': 'autocorrect'},
                        'Autocorreccion.code.basicconfig.main_basic': {'queue': 'autocorrect'},
                        'Autocorreccion.code.basicconfig.ntp_configurator': {'queue': 'autocorrect'},
                        'Autocorreccion.code.basicconfig.ssh_configurator': {'queue': 'autocorrect'},
                        }


#last_change False fuerza que se ejecute, last
app.conf.timezone = 'America/Guatemala'


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
   #sender.add_periodic_task(1 * 3600, main.s(), name='add every 10 Minutes')
   #sender.add_periodic_task(crontab(minute = 12, hour = 49, day_of_week = "thu"),main.s(),)
   sender.add_periodic_task(crontab(minute = 1, hour = 10, day_of_week = "wed"),main.s(),)
   #sender.add_periodic_task(crontab(minute = 36, hour = 9, day_of_week = "thu"),llamado.s(),)
   return False
@app.task
def main():
    from .basicconfig import  main_basic
    main_basic.delay()


# def llamado():
#     from .basicconfig import ntp_configurator
#     ntp_configurator.delay

 