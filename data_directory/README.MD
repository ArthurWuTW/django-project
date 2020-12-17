# data_directory
This directory stores the persistent database files

## Prerequisites
#### Move django_project directory to <USER_HOME>/Desktop

## Setup Persistent Database Files
#### 1. Modify container settings and enter container shell
Delete the line
```sh
# file: run-container
...
    ...
    $DATABASE_OPTS \
    ...
...

```
in **[django-docker-script/docker/project/run-container](https://github.com/ArthurWuTW/django-docker-script/blob/master/docker/project/run-container)**, start container and then enter the container shell
> We need to disable docker volume mapping or database files will be replaced with empty directory(data_directory should have nothing at this moment)

#### 2. Inside container, run the command below to copy the original Postgresql data files to this directory

```sh
sudo rsync -av /var/lib/postgresql /<path>/django_project/data_directory
```
#### 3. exit container, stop container
#### 4. restore the code in step 1
#### 5. start container again
> At this moment, /<USER_HOME>/Desktop/django_project/data_directory/postgresql has been mapping to /var/lib/postgresql in /<DJANGO_DOCKER_REPO>/docker/project/run-container

Finish

## Note(Redundant)
> this section just saves some postesql information and old method which is never used

Steps:
1. Moving the PostgreSQL Data Directory: default data_directory is "/var/lib/postgresql/9.5/main"
```sh
sudo rsync -av /var/lib/postgresql /<path>/django-project/data_directory
```
2. Pointing to the New Data Location: the data_diretory configuration is in "/etc/postgresql/9.5/main/postgresql.conf"
```sh
sudo vim /etc/postgresql/9.5/main/postgresql.conf
```

postgresql.conf
```
...
data_directory = '<path>/django_project/data_directory/postgresql/9.5/main'
...
```

3. Restarting PostgreSQL
```
sudo service postgresql restart
```
Or
```
sudo service postgresql stop && sudo service postgresql start
```
