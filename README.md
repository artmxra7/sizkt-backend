## Pipeline status and coverage report


[![pipeline status](https://gitlab.cs.ui.ac.id/sizakat/5.0/sizakat-backend/badges/master/pipeline.svg)](https://gitlab.cs.ui.ac.id/sizakat/5.0/sizakat-backend/-/commits/master)
[![coverage report](https://gitlab.cs.ui.ac.id/sizakat/5.0/sizakat-backend/badges/master/coverage.svg)](https://gitlab.cs.ui.ac.id/sizakat/5.0/sizakat-backend/-/commits/master)

# SiZakat 5.0

## Environment

File `.env`:

```
SECRET_KEY=foobarbarfoo
ALLOWED_HOSTS=*
DEBUG=1
POSTGRES_DB=sizakat
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
BACKEND_PORT=8000
```

- `SECRET_KEY`

  https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY

- `ALLOWED_HOSTS`

  https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-ALLOWED_HOSTS

- `DEBUG`

  https://docs.djangoproject.com/en/3.0/ref/settings/#debug

- `POSTGRES_*`

  Pengaturan untuk database

  https://github.com/docker-library/docs/tree/master/postgres#environment-variables

- `BACKEND_PORT`

  Port untuk service backend. Digunakan dalam `docker-compose`
