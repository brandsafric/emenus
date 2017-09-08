# Restaurant Menu App
## A python-based full stack Menu Application.
## Utilizes Oauth2 Authentication for Google+ and Facebook IDs
## Clearly demonstrates use of full CRUD operations to a SQL database.

Utilizes:
* [Python 2.7](https://www.python.org/)
* Python libraries: Flask, sqlalchemy, oauth2client
* [jQuery](https://jquery.com/)
* [Bootstrap](http://getbootstrap.com/)
* [Tether](http://tether.io/)
* [animcateCSS](https://daneden.github.io/animate.css/)

Prerequisites:
* [Python 2.7](https://www.python.org/)
* [VirtualBox](https://www.virtualbox.org/wiki/VirtualBox)
VirtualBox is the software that actually runs the VM. You can download it from virtualbox.org, here. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.
Ubuntu 14.04 Note: If you are running Ubuntu 14.04, install VirtualBox using the [Ubuntu Software Center](https://apps.ubuntu.com/cat/applications/quantal/virtualbox-qt/), not the virtualbox.org web site. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.
* [Vagrant](https://www.vagrantup.com/)
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download it from vagrantup.com. Install the version for your operating system.
Windows Note: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

To launch, follow these steps:
* Install the prerequisites listed above (Python, VirtualBox, Vagrant)
* Clone the repo
* From a command line, change to the directory of the repo and mount the vagrant VM with 'vagrant up'
* Connect to vagrant the VM by entering 'vagrant ssh'
* From the command line, type 'cd /vagrant' followed by 'cd restaurant' to change to the target directory.
* Create the database by entering 'python database_setup.py'
* Create the sample restaurant menus by entering 'python lotsofmenus.py'
* Launch the app by typing 'python finalproject.py'
* From your browser, access the site by going to 'localhost:5000'.
* Grab beverage of choice.
* Enjoy in creating restaurant menus complete with sections for appetizers, entrees, and more!
* Make sure to stay hydrated while you experience the joy of making menus!

code by [Phillip Stafford](http://philliprstafford.com)