# Django + PostgreSQL — a SPARC Cloud template

A **Django 5.2 LTS** web app with the **admin** site, **PostgreSQL** (via `DATABASE_URL`), static files served by
**WhiteNoise**, and the **gunicorn** web server. Needs a database.

```
mysite/settings.py           settings (everything server-specific comes from environment variables)
mysite/urls.py               which address shows which page
mysite/health.py             GET /healthz (checks the database)
pages/                       your app: models.py, views.py, admin.py, templates/, migrations/
bin/start.sh                 how SPARC Cloud starts it: migrations -> static files -> gunicorn
requirements.txt             exact versions of every package; .python-version = Python 3.13
sparc.json                   port, health check, start command, database, and the generated DJANGO_SECRET_KEY
```

## Run it on your computer

```sh
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
docker run -d --name pg -e POSTGRES_USER=app -e POSTGRES_PASSWORD=app -e POSTGRES_DB=app -p 5432:5432 postgres:17-alpine
export DATABASE_URL=postgresql://app:app@localhost:5432/app DJANGO_DEBUG=1
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8080          # http://localhost:8080 and http://localhost:8080/admin/
```

## Deploy on SPARC Cloud

1. Dashboard → **Templates** → *Django + PostgreSQL* → **Create my copy on GitHub** (your account/organization, a
   repository name). The copy is yours.
2. **I've created it** → pick the new repository (**Refresh** if needed).
3. Review: port 8080, health check `/healthz`, start command `sh bin/start.sh`, the setting `DJANGO_DEBUG=0`, a
   **generated secret `DJANGO_SECRET_KEY`** (made by SPARC Cloud, never shown) and **a PostgreSQL database**.
   Secrets and databases need a startup **owner**. **Create**.
4. SPARC Cloud builds it (no Dockerfile), deploys it and sets `DATABASE_URL`.

**Create your admin login** once the app runs: app page → **Console** tab (owners/developers with two-factor login) →

```sh
python manage.py createsuperuser
```

then log in at `https://<app>.<startup>.hosting.sparcinnovations.africa:21443/admin/`.

At every start the migrations run first (`bin/start.sh`). If they fail, the log says `MIGRATIONS FAILED …` and the new
version never becomes ready. The app runs as user 1000, not root; static files are collected into `/tmp`.

## Change things

- **Add a page:** a function in `pages/views.py`, a template in `pages/templates/pages/`, a line in `mysite/urls.py`.
- **Add a model:** a class in `pages/models.py`, then on your computer `python manage.py makemigrations`, commit the
  new file in `pages/migrations/`. Register it in `pages/admin.py` to edit it in the admin.
- **Another domain name:** add it to the setting `DJANGO_ALLOWED_HOSTS` (comma-separated) and
  `DJANGO_CSRF_TRUSTED_ORIGINS` (`https://…`). The SPARC Cloud names are allowed by default.
- **Update packages:** change the version in `requirements.txt` (exact `==`), test, commit.

## Licence

MIT (see `LICENSE`). The copy you made is yours.
