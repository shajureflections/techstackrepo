
# Tech Stack App

This is the basic structure of the Flask App. Folder Structure as well as basic code is included with this app. The Swagger part is also present with this basic app.


How to Setup the Basic Flask App
```
- Create a virtual enviornment and activate the enviornment
- pip install -r requirements.txt
- cd web
- python .\techstack_app.py

```

The basic flask app will be open in http://127.0.0.1:5000
The basic flask swagger api  will be open in http://127.0.0.1:5000/apidocs/

How to upgrade the database

```
- Create a folder 'migrations --mkdir migrations
- cd migrations
- alembic init alembic

```
it will create a alembic folder as well as alembic.ini

- Edit the alembic.ini file by changing the sqlalchemy.url

`sqlalchemy.url = postgresql+psycopg2://{username}:{password}@{hostname}/{dbname}`

- In alembic/env.py Add

`sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "repository"))`

`import models`

`target_metadata = models.Base.metadata`
-
```
- alembic revision --autogenerate -m {proper message}
- alembic upgrade head
```

