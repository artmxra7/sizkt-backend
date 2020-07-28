## Pipeline status and coverage report


[![pipeline status](https://gitlab.cs.ui.ac.id/sizakat/5.0/sizakat-backend/badges/master/pipeline.svg)](https://gitlab.cs.ui.ac.id/sizakat/5.0/sizakat-backend/-/commits/master)
[![coverage report](https://gitlab.cs.ui.ac.id/sizakat/5.0/sizakat-backend/badges/master/coverage.svg)](https://gitlab.cs.ui.ac.id/sizakat/5.0/sizakat-backend/-/commits/master)

# SiZakat 5.0

## Environment

### Backend environment

File `.env`:

```
SECRET_KEY=foobarbarfoo
ALLOWED_HOSTS=*
DEBUG=1
SQL_DATABASE=sizakat
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=db
SQL_PORT=5432
BACKEND_PORT=8000
```

- `SECRET_KEY`

  https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY

- `ALLOWED_HOSTS`

  https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-ALLOWED_HOSTS

- `DEBUG`

  https://docs.djangoproject.com/en/3.0/ref/settings/#debug

- `SQL_*`

  Pengaturan untuk database

- `BACKEND_PORT`

  Port untuk service backend. Digunakan dalam `docker-compose`

### Database environment

File `.db.env`

```
POSTGRES_DB=sizakat
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

https://github.com/docker-library/docs/tree/master/postgres#environment-variables
