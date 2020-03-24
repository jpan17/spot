# SPOT
A web application to help pet owners find pet enthusiasts to watch over their animals. This branch is a very early demonstration of the database management system we plan on using (Flask), and the Flask code is intended to be reusable for later versions of the project.

## Information for Setup and Configuration
- [config.py](config.py) contains a reference to os.environ.get('DATABASE_URL'), but I have gitignore-d the .env file I store that in (as it contains my password).
    - An example .env file would contain a line with exactly these contents: "DATABASE_URL = 'postgresql://postgres:my_password@localhost:5432/spot_dev'"
    - General format: "DATABASE_URL = 'dialect+driver://username:password@host:port/database'"

## Developer Information
- The [.flaskenv](.flaskenv) contains the environment variable FLASK_ENV set to 'development', enabling all development features.

## Required Packages (see [requirements.txt](requirements.txt) for versions)
- pip install flask (to run web app)
- pip install flask-sqlalchemy (to handle ORM from web app)
- pip install python-dotenv (for .flaskenv to work, otherwise the environment variable would have to be set every time a new terminal is opened)
- pip install flask-migrate (for database migration)
- pip install psycopg2 (for PostgreSQL)
- PostgreSQL for DBMS

## Testing Information
### Hard-coded tests
To test using desired test script (generally in the [test](test) folder), replace the first line of [test.py](test.py) with the appropriate test module, then run [test.py](test.py). The format should be:

``` from test.<module_name> import run_tests ```

### Text Interaction (Simple Forms)
To test, in [.flaskenv](.flaskenv), make sure to set SPOT_TEST to 'true'. For example:

```SPOT_TEST = true```