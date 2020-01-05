# Raspberry PI & Django base server
> Base server of multiple uses - like IoT - made totally in Python+Django from a maker to makers

[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]

The project was totally created to be used in a Raspberry PI board with linux system in order to provide for developers and makers a base django server to change and add their own server with their own requeriments. For this reason, the project has simply a totally python+django backend in order to control the web pages, a full admin page in order to manipulate users and a simple database to record the logins and logouts of users with webpages to view these datas.

![](header.png)

## Requirements
  - Raspberry PI with linux installed
  - Python 3
  - pip3
  - Django 3
  - Apache 2
  - Desire to learn and try

## Installation on server

Linux:
  - Instaling requirements, downloading and starting project
    ```sh
    sudo apt-get install apache2 -y # install apache2
    sudo apt-get install libapache2-mod-wsgi-py3 # requirements of apache
    sudo apt-get install libapache2-mod-wsgi # if using Python2
    git clone https://github.com/Wanghley/Raspberry-Home-Server.git djpitime #clone repository
    cd djpitime
    virtualenv . -p python3 #start the virtual environment
    pip3 install -r REQUIREMENTS # install the requiremets of python
    source bin/activate
    cd src
    python manage.py makemigrations
    python manage.py migrate
    ```
  - Settings of Apache2:
    ```sh
    sudo nano /etc/apache2/sites-available/000-default.conf
    ```
    Note: If errors happen with below, just do the following and it will re-install apache


    ```     
    <VirtualHost *:80>
        ServerName www.example.com

        ServerAdmin webmaster@localhost

        Alias /static <PATH TO FOLDER>/djpitime/static
            <Directory <PATH TO FOLDER>/djpitime/static>
               Require all granted
             </Directory>

        <Directory <PATH TO FOLDER>/djpitime/src/cfehome>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>

        WSGIDaemonProcess djpitime python-path=<PATH TO FOLDER>/djpitime/src:<PATH TO FOLDER>/djpitime/lib/<pythonX.Y>/site-packages
        WSGIProcessGroup djpitime
        WSGIScriptAlias / <PATH TO FOLDER>/djpitime/src/cfehome/wsgi.py


        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

    </VirtualHost>

    ```
  - Allow use of local database:
    ``` sh
    sudo adduser $USER www-data
    sudo chown www-data:www-data /home/$USER/Dev/cfehome    
    sudo chown www-data:www-data /home/$USER/Dev/cfehome/src/db.sqlite3
    sudo chmod -R 775 ~/Dev/cfehome

    # if above fails, try (thanks Mike!):
    sudo chown -R www-data:www-data ~/Dev/cfehome
    sudo chown www-data:www-data /home/pi/Dev/cfehome/src
    ```
  - Allow use of local IP Address:
    First of all is get the IP address of your raspberry pi with ```ifconfig```
    then use:
    ```sh
    sudo nano <PATH TO FOLDER>/djpitime/src/djpitime/settings.py
    ```
    and find the line: ALLOWED_HOSTS = ['127.0.0.1'] and add yours IP address, like: ALLOWED_HOSTS = ['127.0.0.1','192.168.1.xxx']
  
  -Restart apache2 and have fun!

## Usage example

This project can be used in so many puposes as your need. It can be used since a simple backup server to an IoT server of your smarthouse project.

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

To develop, follow these steps.

  ```sh
      sudo apt-get install apache2 -y # install apache2
      sudo apt-get install libapache2-mod-wsgi-py3 # requirements of apache
      sudo apt-get install libapache2-mod-wsgi # if using Python2
      git clone https://github.com/Wanghley/Raspberry-Home-Server.git djpitime #clone repository
      cd djpitime
      virtualenv . -p python3 #start the virtual environment
      pip3 install -r REQUIREMENTS # install the requiremets of python
      source bin/activate
      cd src
      python manage.py makemigrations
      python manage.py migrate
      python manage.py runserver # this will start the server in localhost to development purposes
  ```
  then, start programming in yuor preferred IDE.
  Keep Coding! ;)


## Meta

Wanghley Soares Martins – [@Wanghley](https://www.instagram.com/Wanghley/) – wanghleys@gmail.com

Distributed under the MIT license. See [``LICENSE``](https://github.com/Wanghley/Raspberry-Home-Server/blob/master/LICENSE) for more information.

[https://github.com/Wanghley](https://github.com/Wanghley)

## Contributing

1. Fork it (<https://github.com/Wanghley/Raspberry-Home-Server/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
