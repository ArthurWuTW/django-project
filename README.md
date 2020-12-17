# Plant Monitor

A Django web app to visualize plant data and system status

> To realize automatic planting in our farmland, I decided to create an application to get the data and system status, and visualize them as well. This application provides a convenient way to manage the farmland remotely.

![image](https://github.com/ArthurWuTW/django-project/blob/develop/readme_materials/1.png)

## Features
- **[Python](https://www.python.org/)** with **[Django](https://www.djangoproject.com/)** framework
- **[Postgresql](https://www.postgresql.org/)** database with **[Django](https://www.djangoproject.com/)** ORM
- Chart visualization with **[Chart.js](https://www.chartjs.org/)**
- Image serialization/deserialization with **[OpenCV](https://opencv.org/)**
- Environment variables management with **[Docker](https://www.docker.com/)** in another repository
- Email authentication for activating account and resetting forgot password as well
- Configuration management
- Database backup management
- Field 3d reconstruction with **[OpenSfm](https://www.opensfm.org/)**
- Frontend template with **[sb admin 2](https://github.com/StartBootstrap/startbootstrap-sb-admin-2)**

## Django Project Structure
```
django_project/
├── backup_git.py                         # backup .sql with git version control
├── backup_thread.py                      # the python script to backup .sql
├── data_directory
│   ├── postgresql                        # persistent db directory              
│   └── README.MD                         # instructions to store the persistent db in this directory
├── data_image
├── django_project
│   ├── asgi.py
│   ├── settings.py                       
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── monitor_app
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models_collection                  # one file contains only one class, and file name is the same as class name
│   ├── models.py                          # import all the models in models_collection
│   ├── static
│   │   └── dashboard
│   ├── system_check                       # run unit test before starting the app
│   ├── templates
│   │   └── template_dashboard
│   ├── tests.py
│   ├── urls.py                            # url settings
│   ├── views_collection                   # one file contains only one class, and file name is the same as class name
│   │   └── handlers                       # view handlers
│   └── views.py                           # import all the views in views_collection directory
├── readme_materials
├── script
│   ├── create-apps                       
│   ├── create-superuser                   
│   ├── make-migrations-and-migrate
│   └── start-project-server               # run web application
├── secure_data
│   ├── secure_data_example.json           # secure data configuration
│   └── secure_data_loader.py
└── test_script

```

## Setup
#### 1. Linux Environment
See repository **[Django-docker-script](https://github.com/ArthurWuTW/django-docker-script)** and follow the instructions to install docker and create docker image.

#### 2. Database
Postgresql Database is saved as a persistent file(s) outside Docker. If you first setup the database, See **[README](https://github.com/ArthurWuTW/django-project/tree/master/data_directory)**, and if you have existed database, copy and paste into **[data_directory](https://github.com/ArthurWuTW/django-project/tree/master/data_directory)**

#### 3. Configuration
See directory **[secure_data](https://github.com/ArthurWuTW/django-project/tree/master/secure_data)**

#### 4. Others
- 3D Reconstruction App(OpenSfm)
We need to create another Docker image for OpenSfm, See **[docker-script-opensfm](https://github.com/ArthurWuTW/docker-script-opensfm)** for Docker and **[OpenSfm custom fork](https://github.com/ArthurWuTW/OpenSfM)**

- Hardware in Farmland
DC motor, belt, DC power supply, L298N and Raspberry. Code run in raspberry pi is in **[HERE](https://github.com/ArthurWuTW/crawler-script)**

- Local Backup Directory
Create an empty directory with git init for database backup management

## Run Server
```sh
# start container
cd <DOCKER_REPO_DIR>/docker
./project-start-container

# enter container
./project-enter-container-shell

# run app
cd <DJANGO_PROJECT_DIR>/script
./start-project-server
```

## Extension

#### 1. Create a new Class-based View
> In general, the code of Django View classes is written in file <strong><APP_DIR>/views.py</strong>, but as time goes by the code grows and becomes more and more complicated. In order to make the code clean, every class is written into a single file(.py) located in views_collection directory.

The file name has to be the same as the name of view class. For example, there is a class named "ViewExample", and its file name must be ViewExample.py

```py
from django.views import View
class ViewsExample(View):
    def get(self, request):
        handler = Handler()
        contextHandler = ContextHandler()
        contextHandler.join(handler)
        contextHandler.fillInContext()
        return render(request, "XX.html", contextHandler.getContext())
    def post(self, request):
        handler = Handler()
        contextHandler = ContextHandler()
        contextHandler.join(handler)
        contextHandler.fillInContext()
        return render(request, "XX.html", contextHandler.getContext())
```
#### 2. Create a new Data Handler
Data handler which wants to fill data into the Context has to inherit ModelDataHandler class and overwrite getData and getTitle methods.
```py
# monitor_app/views_collection/handlers/ModelDataHandler.py
import abc
class ModelDataHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getData(self):
        return NotImplemented
    @abc.abstractmethod
    def getTitle(self):
        return NotImplemented
```
ContextHandler collects data handlers and generates a Context dictionary by their keys(title) and values(data).
```py
# monitor_app/views_collection/handlers/ContextHandler.py
class ContextHandler():
    def __init__(self):
        self.data_handler_list = list()
        self.context = {}
    def join(self, dataHandler):
        self.data_handler_list.append(dataHandler)
    def fillInContext(self):
        for data in self.data_handler_list:
            self.context[data.getTitle()] = data.getData()
    def getContext(self):
        return self.context
```
#### 3. Create a new Class-based Model
Every model class is written into a single file(.py) located in models_collection directory. The file name has to be the same as the name of model class. For example, there is a class named "ModelExample", and its file name must be ModelExample.py

```py
from django.db import models
class ModelExample(models.Model):
    name = models.CharField(max_length=25)
    status = models.CharField(max_length=25)
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name_plural = 'Model'
```
