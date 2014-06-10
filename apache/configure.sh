
#!/bin/bash

sudo -s
cp ads /etc/apaches/sites-available/
a2ensite ads
apachectl restart

