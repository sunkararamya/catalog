#ITEM CATALOG-WEBAPP  UDACITY PROJECT
##By Sunkara Ramya
This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

##Introduction to item-catalog project:

ITEM CATALOG  application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit, and delete their own items.I have done my item catalog project on FILM CAMERAS which gives information about different types of film cameras.users can be login into this appliction and they can be able to do delete,edit,add crud operations. 


## Main Features of this catalog app are :

i.correct authentication and authorisation checking of user.
ii.Implements oAuth using Google Sign-in API
iii.It supports all CRUD operations using flask and SQLAlchemy.
iv.It has to satisfy all JSON endpoints


##Main tools required for building this web app are following:
1. Python
2. HTML
3. CSS
4.Flask Framework
5.SQLAlchemy
6. DataBaseModels
7.OAuth

##The  Main files included in this project are following:
1.`ModelDataSetup.py`
First we have to create a database file for storing all data about items.
I had created `filmcameras.db` 
In this file I had created three database models for storing user details and items  details.They are 
i.GoogleMailuser
ii.Filmy_Cameras
iii.Filmy_cam_Name
 
2.'DataBase_Items_init.py' 
In this file insert all items and userdetails into database.

3.`web_app.py` .
This file contains the  code  which is used for doing crud operations.

4.templates folder 
This folder contains all HTML files.

## Steps we have to follow for run this project are following:
1.we have to run this item catalaog web-app in  virtualenvironment.So, we have to create virtual environment.   
For  this first download and install `vagrant`. 
for downloading vagrant go to below link
--- [Vagrant](https://www.vagrantup.com/)

2.Next install virtualBox.
for downloading  virtualBox go to below link 
---[VirtualBox](https://www.virtualbox.org/wiki/Downloads)

3.Clone or download the Vagrant VM configuration file from below link
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)


4. first we have to run vagrant init command for initializing 
open command prompt in  project folder and run.

   ` vagrant init ubuntu/xenial64`
   
5.To boot your first Vagrant environment type the vagrant up command.
      `vagrant up`.
when this  will finished, you will have a virtual machine running Ubuntu	  

6.Next type following command
  ``vagrant ssh``
This command will drop you into a full-fledged SSH session
7.change your directory to vagrant.
Type  ``cd vagrant``
8. For installing python type
   `sudo apt-get install python`
9.For installing pip type
       `sudo apt-get install python-pip`
10.For installing  or upgrading Flask type
       `sudo python3 -m pip install --upgrade flask`
11.we have to import SQLAlchemy module so type
     ``pip install sqlalchemy``   
 12.Next run your datasetup file 
      ``ModelDataSetup.py``
13.To insert data into database run
      ``DataBase_Items_init.py``
## For signin to Google Mail account
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Film Camera Hub'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in signin.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in ``film_camera_item_catalog_project`` directory that you cloned from here
14. Run application using 
``python /film_camera_item_catalog_project/web_app.py``

# JSON Endpoints


i.allfilm_camerasJSON(): `/CameraHub/JSON`
    - Displays the whole filmcamera  catalog.All cameras will be displayed.

ii.categoriesJSON(): `/film_camerastore/cameracategories/JSON`
    - Displays all Camera categories
iii.itemsJSON(): `/film_camerastore/film_cameras/JSON`
	- Displays all Camera Models

iv.categoryItemsJSON: `/film_camerastore/<path:film_camera_name>/models/JSON`
    - Displays camera models for a specific camera category

v.ItemJSON: ``/film_camerastore/<path:film_camera_name>/<path:cam_model_name>/JSON``
    - Displays a specific Film_Camera category Model.

## Miscellaneous

This project is inspiration from [arrickx](https://github.com/arrickx/Item-Catalog-Application
