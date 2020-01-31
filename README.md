# Django Helpdesk
> This is just a simple Django helpdesk web application that I am building to solve a problem at my workplace and to better test and expand my abilities


## Installation

**Clone Repo:**
```
git clone https://github.com/Codenii/django-helpdesk.git
```

**Change Directory to the Cloned Repo:**
```
cd django-helpdesk
```

**Create Virtual Environment:**
```
virtualenv hdenv
```

**Activate Environment:**
 - Windows: ```hdenv\Scripts\activate```
 - Linux: ```source hdenv/bin/activate```

**Install Requirments:**
```
pip install -r requirements.txt
```

**Run Migrations:**
```
python manage.py makemigrations
```
```
python manage.py migrate
```

**Run Server:**
```
python manage.py runserver
```

## Release History

* 0.0.1
    * WIP - Currently Blank Django Project
* 0.0.5
    * Basic Functionality
    * User Creation/Login/Auth
    * Basic Ticket Views
    * Basic Ticket Editing/Management

## Meta

Cody Wilson – [@Codeni80](https://twitter.com/codeni80) – codeni80@gmail.com

[https://github.com/codenii/django-helpdesk](https://github.com/Codenii/django-helpdesk)

## Contributing

1. Fork it (<https://github.com/codenii/django-helpdesk/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
