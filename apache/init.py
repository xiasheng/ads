
import os

os.system('cp ads /etc/apache2/sites-available/')
os.system('a2dissite *')
os.system('a2ensite ads')
os.system('apachectl restart')

