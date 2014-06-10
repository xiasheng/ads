
import os, shutil


# create log file
os.mkdir('/var/log/django')
os.mknod('/var/log/django/debug.log', mode=0777)

# init memcached
#os.system('killall memcached') 
#os.system('memcached -d')

