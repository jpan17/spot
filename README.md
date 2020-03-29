# SPOT
A web application to help pet owners find pet enthusiasts to watch over their animals. This branch is a very early demonstration of the database management system we plan on using (Flask), and the Flask code is intended to be reusable for later versions of the project.

## Information for Setup and Configuration
- [config.py](config.py) contains a reference to os.environ.get('DATABASE_URL'), but I have gitignore-d the .env file I store that in (as it contains my password).
    - An example .env file would contain a line with exactly these contents: "DATABASE_URL = 'postgresql://postgres:my_password@localhost:5432/spot_dev'"
    - General format: "DATABASE_URL = 'dialect+driver://username:password@host:port/database'"
- Before running the application, but after creating your Postgres database, run the following command to structure the database correctly:
    - ``` flask db upgrade ```
    - Also, run this anytime the database structure changes (the migration scripts are in [migrations](migrations)).
- To run the application:
    - Navigate to the highest level directory ([app](app), [config.py](config.py), etc. should be in that directory), and run the command:
        - ``` flask run ```
    - Open localhost:5000 in your browser. This may vary across computers/environments, but when Flask initializes, it will display where it opens (0.0.0.0 should be equivalent to localhost, I think)

## Developer Information
- The [.flaskenv](.flaskenv) contains the environment variable FLASK_ENV set to 'development', enabling all development features.
- When creating HTML pages, make sure [background.html](templates/background.html) is included *before* [header.html](templates/header.html), because the spots are intended to be covered by the header bar, not the other way around.

## Required Packages (see [requirements.txt](requirements.txt) for versions)
- pip install flask (to run web app)
- pip install flask-sqlalchemy (to handle ORM from web app)
- pip install python-dotenv (for .flaskenv to work, otherwise the environment variable would have to be set every time a new terminal is opened)
- pip install flask-migrate (for database migration)
- pip install psycopg2 (for PostgreSQL)
- pip install -U sphinx (for documentation)
- PostgreSQL for DBMS

## Testing Information
### Hard-coded tests
To test using desired test script (generally in the [test](test) folder), replace the first line of [test.py](test.py) with the appropriate test module, then run [test.py](test.py). The format should be:

``` from test.<module_name> import run_tests ```

### Text Interaction (Simple Forms)
To test, in [.flaskenv](.flaskenv), make sure to set SPOT_TEST to 'true'. For example:

```SPOT_TEST = true```

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

### Todos
- User Updating (Very Optional, given listing updating works, user updating should work too)

### Known Issues
None