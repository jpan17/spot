# SPOT
A web application to help pet owners find pet enthusiasts to watch over their animals.

## Information for Setup and Configuration
### Deploying to Heroku
- [spot_config.py](spot_config.py) references several security-related and other configuration environment variables, but .flaskenv and .env are ignored in Heroku's environment. Instead, use their configurations variables feature to set _all_ of the required environment variables (see [Staging locally](#staging-locally) for descriptions of environment variables).
    - For example:
    ```
    heroku config:set SPOT_MODE=production
    ```
- Note that a [manage.py](#), [wsgi.py](#), and [Procfile](#) will be required in order to deploy on Heroku. See [this link](https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/) and [this link](https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0) for a couple of tutorials for general deployment, and [this link](https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres) for setting up Postgres on Heroku (not sure what we used previously, but the tutorials should cover most of the required aspects of deployment)
    - Upon deployment, one must upgrade the database. Most likely, the command to do so should be:
    ```
    heroku run upgrade
    ```
    - See [Staging locally](#staging-locally) for doing this for our current method of introducing significant changes to database schema.

### Staging Locally
- [spot_config.py](spot_config.py) contains a reference to several security-related environment variables, but I have gitignore-d the .env file I store that in (as it contains my password and other passwords/secret keys).
    - An example .env file would contain a line with exactly these contents: 
    ``` DATABASE_URL = 'postgresql://postgres:my_password@localhost:5432/spot_dev' 
    SPOT_SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8' 
    SPOT_SECURITY_PASSWORD_SALT = 'this is a salt'
    
    APP_MAIL_USERNAME='princeton.spot.team'
    APP_MAIL_PASSWORD='this_is_a_password'
    ```
    - General format for DATABASE_URL: "DATABASE_URL = 'dialect+driver://username:password@host:port/database'"
    - SPOT_SECRET_KEY can be generated with os.urandom(24)
        - To generate a new one, 'python gen_key.py > temp.txt' will save a keystring to a new file called temp.txt
    - SPOT_SECURITY_PASSWORD_SALT can be any string
    - APP_MAIL_USERNAME is the gmail username (everything before the @gmail.com)
    - APP_MAIL_PASSWORD is the corresponding password for the account.
- Before running the application, but after creating your Postgres database, run the following command to structure the database correctly:
    - ``` flask db upgrade ```
    - Also, run this anytime the database structure changes (the migration scripts are in [migrations](migrations)).
        - Note: For significant changes, it will be easiest to clear the database, which can be done by running the app with SPOT_MODE set to 'test' and clicking "Clear Database" on the homepage, then changing SPOT_MODE back.
- To run the application:
    - Navigate to the highest level directory ([app](app), [config.py](config.py), etc. should be in that directory), and run the command:
        - ``` flask run ```
    - Open localhost:5000 in your browser. This may vary across computers/environments, but when Flask initializes, it will display where it opens (0.0.0.0 should be equivalent to localhost, I think)

## Developer Information
- The [.flaskenv](.flaskenv) contains the environment variable FLASK_ENV set to 'development', enabling all development features.
- When creating HTML pages, make sure to include [background.html](templates/background.html), [header.html](templates/header.html), [links.html](templates/links.html), and [footer.html](templates/footer.html) (see any of the html templates in [templates/users/](templates/users/) for an example).

## Maintenance
- Two important services used for addresses and maps have free tiers with the following limits (so if an error occurs with these, it may be due to hitting the limit):
    - Algolia (address autocomplete): 100,000 requests per month
    - Leaflet (Currently using Open Streets Map which has *no limit*, but if switch to Mapbox Static Tiles API): 200,000 requests per month

## Required Packages (see [requirements.txt](requirements.txt) for versions)
- pip install flask (to run web app)
- pip install flask-sqlalchemy (to handle ORM from web app)
- pip install python-dotenv (for .flaskenv to work, otherwise the environment variable would have to be set every time a new terminal is opened)
- pip install flask-migrate (for database migration)
- pip install flask-login (for user authentication)
- pip install psycopg2 (for PostgreSQL)
- pip install -U sphinx (for documentation)
- pip install flask-mail (for email sending)
- PostgreSQL for DBMS

## Testing Information
### Prototype
To run prototype, set SPOT_MODE to 'prototype' in [.flaskenv](.flaskenv). For example:

``` SPOT_MODE = prototype ```

### Hard-coded tests
To test using desired test script (generally in the [test](test) folder), replace the first line of [test.py](test.py) with the appropriate test module, then run [test.py](test.py). The format should be:

``` from test.<module_name> import run_tests ```

### Text Interaction (Simple Forms)
To test, in [.flaskenv](.flaskenv), make sure to set SPOT_MODE to 'test'. For example:

```SPOT_MODE = test ```

### Features
- User Creation
- List of Users (unsorted)
- User Deletion (partially)
- Listing Creation
- List of Listings (in user details, so it is by user)
- Most of the error catching so far (have not tested this extensively)
- Listing Updating
- Listing Deletion
- Accepting Listings (for sitters)
- List of Listings, not by user (which can be related to accepting listings)

### WIP
- Full-time feature in listing creation
- AM/PM dropdown when creating new listings
