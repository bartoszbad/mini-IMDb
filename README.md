# mini-IMDb
Mini IMDb using Django Rest Framework and OMDbAPI<br><br>



    To start the API

    Open your terminal
    $ sudo easy_install pip # installs Pip package manager
    $ git clone https://github.com/maikelnabil/django-rest-movies.git
    $ cd mini-IDBm # Browse into the repo root directory
    $ pip install virtualenv # Virtualenv is a tool to create isolated Python environments.
    $ virtualenv venv #Create virtual enviroment
    $ source venv/bin/activate # Launch the environment
    $ pip3 install -r requirements #Install dependiences
    $ python3 manage.py migrate #Migrate models
    $ python3 manage.py createsuperuser #Create Django Admin, some functions requires Admin.auth
    $ python3 manage.py runserver

APP allows to:
<br>search OMDbAPI by movie title, type and year
<br>register and login
<br>rate movies and maintain user's rates
<br>see other users rate
<br>save movie on user's "favourites" and "want to see" lists and maintain them
<br>see whats new in app (movies added since last two week)


URLs and its functions:<br>
/register/ - Allow to create new user<br>
/movies/ - Allow to view all movies with its details from local database<br>
/movies/pk/ - Allow Superusers to delete movie from database <br>
/movies-by-title/ - Allow to search for a movie in OMDbAPI by Title(required), year(optional), type(required). Returns one closet match<br>
/newest/ - Shows all movie added to database in last 2 week<br>
/favourites-movies/ - Allow logged in users to add movies on its favourites list, shows all user's favourites movies<br>
/favourites-movies/pk/ - Allow creator to upadete and delete movie from favourite list<br>
/wanted-movies/ - Allow logged in users to add movies on its "Want to see" list, shows all user's "want to see" movies<br>
/wanted-movies/pk/ - Allow creator to upadete and delete movie from "want to see". list<br>
/rate/ - Allow logged in users to rate movies and shows all previous rates made by requesting user<br>
/rate/pk/ - Allow logged in users to view details of rates and allow creator to upadete and delete rate<br>
/users/ - Allow logged in users to view all register users<br>
/users/pk/ - Allow logged in user to view details of user(pk) and its all Movie Rates<br>
