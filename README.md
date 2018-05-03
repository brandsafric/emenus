# EMenus
## A python-based full stack Restaurant Menu Application that allows the creation and manipulation of restaurant menus.
## Utilizes Oauth2 Authentication for Google+ and Facebook IDs for login access.

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
* In app.js, replace the Google and Facebook credentials with your own.
* Replace the client_secrets.json with the Google JSON credentials.
* Replace the text in fb_client_secrets.json with your Facebook developer credentials.
* Install Apache2
```
    sudo apt-get install apache2
```
* Install libapache2-mod-wsgi
```
    sudo apt-get install libapache2-mod-wsgi python-dev
```
* Set time to UTC time (choose None of the Above, then UTC)
```
    sudo dpkg-reconfigure tzdata
```
* Install git
```
    sudo install git
```
* Install python packages
```
    sudo apt-get install python-pip
```
* Clone the repo into /var/www
* Create an app.wsgi file in the itemcatalog directory with the following contents:
 ```
    activate_this = '/var/www/emenus/venv/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
    import sys
    sys.path.insert(0,'/var/www/emenus')
    from application import app as application
    application.secret_key = 'super_secret_key'
```

* Either create a new virtual host and modify the .conf file or modify the default 000-default.conf file to include
the following:
``` 
    <VirtualHost *: 80>
    ServerName (name of ip of server)
    DocumentRoot /var/www/emenus

    WSGIDaemonProcess emenus user=(username) python-path=/var/www/emenus/catalog/venv/bin/python2.7
    WSGIScriptAlias / /var/www/emenus/app.wsgi
    <Directory /var/www/html/emenus/catalog>
            WSGIProcessGroup emenus
            WSGIApplicationGroup %{GLOBAL}
            Order allow,deny
            Allow from all
    </Directory>
	Alias /static /var/www/emenus/catalog/static
	<Directory /var/www/emenus/catalog/static/>
		Order allow,deny
		Allow from all
	</Directory>
``` 
* Change into the directory /var/www/emenus
* Install PostgreSQL
```
    sudo-apt-get install postgresql postgresql-contrib
```
* Install virtual environement
```
    sudo virtualenv venv
```
* Activate the virtual environment
```
    source venv/bin/activate
```
* Install dependencies in virtual environment
```
    pip install flask
    pip install sqlalchemy
    pip install oauth2client
    pip install psycorpg2
    pip install requests
```
* Deactivate Virtual Environemnt
```
    deactivate
```
* In psql, create the catalog database and catalog role.
```
    sudo su - postgres
    psql
    create role catalog;
```
* Set the catalog role to be the owner of the catalog database.
```
    CREATE DATABASE catalog OWNER catalog;
    ALTER ROLE "catalog" WITH LOGIN;
    ALTER USER catalog WITH PASSWORD 'catalog';
```
* Run the following commands to setup the initial database tables and dummy entries:
```
    sudo python database_setup.py
    sudo python lotsofmenus.py
```
* Restart Apache service
```
    sudo apachectl restart
```
* Enjoy in creating restaurant menus complete with sections for appetizers, entrees, and more!
* Make sure to stay hydrated while you experience the joy of making menus!

code by [Phillip Stafford](http://philliprstafford.com)