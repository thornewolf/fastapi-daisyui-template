# Turing test game

## Setup

Env variables:

`.env`

```bash
DATABASE_URL="sqlite:///db.sqlite"
```

## Database Management

Whenever you change the schema, run the following commands to migrate the databse. Be sure your env variables are set.

```bash
# change some schema
poetry run alembic revision -m "revision title"
# inspect migration script
poetry run alembic upgrade
```

## Launching the server

```bash
poetry run uvicorn project.app:app --reload
```

## References

- https://fastapi.tiangolo.com/
- https://tailwindcss.com/
- https://daisyui.com/
