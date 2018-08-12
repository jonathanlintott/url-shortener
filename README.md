# url-shortener

The url-shortener application allows for the hosting of a flask application
with two main endpoints.

POST /shorten_url - When provided with a valid URL, will return a replacement
URL.

Example post body:
```json
{
    "url": "www.google.com"
}
```

Example response (with host URL of host.com):
```json
{
    "shortened_url": "www.host.com/Fhdj45Jd"
}
```

GET /{shortened url} - When the 8 digit hash is passed back, a redirection will
occur to the original url.

## Running

First install the package requirements in the environment of your choice.

```bash
pip install -r requirements.txt
```

Then set the FLASK_APP variable to point to the cli.py file.

```bash
export FLASK_APP=cli.py
```

Initialise the database.
```bash
flask db upgrade
```

Then run to run a local development server.

```bash
flask run
```

You can also run the package tests.
```bash
flask test
```

Use gunicorn to serve the application. 
```bash
gunicorn -b 0.0.0.0:5000 cli:app
```

## Scale
Gunicorn can usually handle hundreds to thousands of requests per second 
depending on the server. Additional requirments for scaling would be to 
implement a database such a MySql or Postgres to replace the development 
sqlite database. 

Alternative hosting choices would be employing a serverless architecture, or
enforcing a load balancer to distribute requests to a number of servers running
the application. 