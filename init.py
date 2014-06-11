import os,sys

# init db
print '-----init django database-----'
os.system('cd db;python init.py')

# init django model
print '-----init django model-----'
os.system('python manage.py sqlall models')
os.system('python manage.py syncdb')

# init apache
print '-----init apache-----'
os.system('cd apache;python init.py')
