#from __future__ import absolute_import
import os
from celery import Celery
import subprocess
import time
from datetime import datetime

#1) starts celery code
#2) run docker
#3) fires off alerts
#4) runs run_code.sh
#5) replaces client_code_wrapper __clientfile_
#6)

# Set the default Django settings module for the 'celery' program.
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings_prod')

app = Celery('orweb', broker='amqp://guest:guest@10.1.1.10:5672//')
#app = Celery('orweb')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
#app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(name='tasks.hello', bind=True)
def hello(self, str_name, str_id, str_file):
    print(f'Request: {self.request!r}')
    print(f'-----: ' + str_name + ' ' + str_id + ' ' + str_file)
    save_path = '/home/user01'
    file_name = "hello.txt"
    completeName = os.path.join(save_path, file_name)
    file1 = open(completeName, "w")
    file1.write("file information")
    file1.write(time.strftime("%b %d %Y %H:%M:%S %Z", time.localtime()))
    file1.close()



@app.task(name='tasks.add_job', bind=True)
def add_job(self, str_id, str_email, str_pass, str_docker, str_file):
    print(f'Request: {self.request!r}')
    
    print(time.strftime("%b %d %Y %H:%M:%S %Z", time.localtime()))
    #str_file=str_file.replace('.py','')
    #subprocess.run(['sh', './run_job2.sh', str_id, str_email, str_file, str_pass], capture_output=True)
    sp=subprocess.run(['sh', './run_job2.sh', str_id, str_email, str_file, str_pass, str_docker], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sp=sp.stdout
    with open("/home/user01/log_"+str_pass+"_"+datetime.utcnow().strftime('%Y%m%d_%Hh%Mm%Ss_UTC') +".txt","wb") as file1:
        file1.write(sp)
    print(time.strftime("%b %d %Y %H:%M:%S %Z", time.localtime()))
