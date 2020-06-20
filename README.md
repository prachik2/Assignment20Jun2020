**Network Details**

One Page application for keeping records of network addresses and their values stored into system database.

**Getting Started**\
1.Prerequisites :\
Your system should have Python3 installed and Django version 3.0.7\
Clone the repository using `git clone <repository_url>`.\
Create virtual environment using  `virtualenv <name of environment>`


2.Installing :\
 install all required requirements from  requirements.txt file from above repository that you cloned.\
` pip3 install -r requirements.txt
`

**Built With**\
1.Django Framework\
2.HTML5,CSS3,JavaScript

**Database**

In settings.py file add your username and database name and other settings accordingly.

    'default': {
        'ENGINE': '<database_engine>',
        'NAME': '<database_name>',
        'USER': '<user_name>',
        'PASSWORD':'<password>',
        'HOST':'<host_name>',
        'PORT': <port_no>,
    }

**Note: Don't push your credentials into settings.py that is global.Keep it into local_settings.py file which you can keep at locally by adding  it in .gitignore.

**Run migrations**

run the migrations using command below\
`python3 manage.py migrate
`

and if any changes made for the app;\
`python3 manage.py makemigrations <app_name>`


**Running Application**

Use command below to run application\
`python3 manage.py runserver`


**Data Generation Script**

run below script to insert "n" no. of records for creating your dummy database.

`python3 data_generator_script`


**Bug Tracker**\
Bugs are tracked on GitHub Issues. In case of trouble, please check there if your issue has already been reported. If you spotted it first, help us smashing it by providing a detailed and welcomed feedback here.