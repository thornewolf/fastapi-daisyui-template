# Turing test game

## Setup

Env variables:

`.env`

```bash
DATABASE_URL="sqlite:///db.sqlite"
```

## Create Migrations

```bash
# change some schema
poetry run alembic revision -m "revision title"
# inspect migration script
poetry run alembic upgrade
```

## References

- https://fastapi.tiangolo.com/
- https://tailwindcss.com/
- https://daisyui.com/
