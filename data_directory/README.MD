Date: Sep 17, 2020
Purpose:
* to store the persistent database in this directory

Steps:
1. Moving the PostgreSQL Data Directory: default data_directory is "/var/lib/postgresql/9.5/main"
>> sudo rsync -av /var/lib/postgresql /<path>/django-project/data_directory

2. Pointing to the New Data Location: the data_diretory configuration is in "/etc/postgresql/9.5/main/postgresql.conf"
>> sudo vim /etc/postgresql/9.5/main/postgresql.conf

--------------postgresql.conf----------------
...
data_directory = '<path>/django_project/data_directory/postgresql/9.5/main'
...
----------------------------------------------

3. Restarting PostgreSQL
>> sudo service postgresql restart
Or
>> sudo service postgresql stop && sudo service postgresql start
