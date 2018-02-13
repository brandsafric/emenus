# EMenus
## A python-based full stack Restaurant Menu Application that allows the creation and manipulation of restaurant menus.
## Utilizes Oauth2 Authentication for Google+ and Facebook IDs for logiu access.

Utilizes:
* [Python 2.7](https://www.python.org/)
* Python libraries: Flask, sqlalchemy, oauth2client, requests, pyscopg2
* [jQuery](https://jquery.com/)
* [Bootstrap](http://getbootstrap.com/)
* [Tether](http://tether.io/)
* [animcateCSS](https://daneden.github.io/animate.css/)

Prerequisites:
* [Python 2.7](https://www.python.org/)
* Amazon Web Services or equivalent instance


To deploy, follow these steps:
* Clone the repo
* Change the SSH port to 2200
* Permit firewall exceptions in both UFW and Web Services firewall to allow incoming ports for the following:
    port 2200
    HTTP
    NTP
    Apache Full
* Restart SSH service
* Install Apache2
* Install libapache2-mod-wsgi
* Set time to UTC time.
* Create user grader with sudo access.
* Create new SSH key for grader and copy the public key contents to authorized_keys file for user.
* Create 'itemcatalog' directory under /var/www/html
* Create an app.wsgi file in the itemcatalog directory with the following contents:
 ```
activate_this = '/var/www/html/itemcatalog/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0,'/var/www/html/itemcatalog')
from application import app as application
application.secret_key = 'super_secret_key'
```

* Either create a new virtual host and modify the .conf file or modify the default 000-default.conf file to include
the following:
```    
    WSGIDaemonProcess itemcatalog user=grader
    WSGIScriptAlias / /var/www/html/itemcatalog/app.wsgi
    <Directory /var/www/html/itemcatalog>
            WSGIProcessGroup itemcatalog
            WSGIApplicationGroup %{GLOBAL}
            Order allow,deny
            Allow from all
    </Directory>
	Alias /static /var/www/itemcatalog/static
	<Directory /var/www/itemcatalog/static/>
		Order allow,deny
		Allow from all
	</Directory>
``` 
* Change the following lines in the file:
``` ServerName <IP Address>
    DocumentRoot /var/www/html/itemcatalog
```
* Install the following dependencies: postgresql, flask, sqlalchemy, oauth2client, pycopg2, requests
* In psql, create the catalog database and catalog role.
* Set the catalog role to be the owner of the catalog database.
* Install git
* Create directory git under itemcatalog directory
* Clone the repo AWS branch
* Move all files from the newly clones EMenus subdirectory to the item-catalog directory.
* Install virtual environment (virtualenv)
* Activate the virtual environment
* Run the following commands to setup the initial database tables and dummy entries:
```
sudo python database_setup.py
sudo python lotsofmenus.py
```
* Restart Apache service
* Create new OAuth credentials in both Google sign-in and Facebook Developer APIs (specify the DNS name of the server
which can be accomplished by running ```ping -a ipaddress```)
* Replace the client_secrets.json and fb_client_secrets.json with the newly created oauth credentials.
* Visit the server's site via the DNS name.
* Enjoy in creating restaurant menus complete with sections for appetizers, entrees, and more!
* Make sure to stay hydrated while you experience the joy of making menus!

code by [Phillip Stafford](http://philliprstafford.com)
