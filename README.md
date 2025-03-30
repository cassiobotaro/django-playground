# django-playground

🛝 A place to play and have fun.

## Requirements

[uv](https://docs.astral.sh/uv/)

## Installation

```bash
cp .env.example .env
uv python install 3.13
uv python pin 3.13
uv sync
uv run pre-commit install
uv run ./manage.py migrate
uv run ./manage.py loaddata ./all_data.json
docker compose up -d
uv run ./manage.py runserver
# em outro terminal
uv run python manage.py rundramatiq
```

| User         | Password  | admin | grupo |
| ------------ | --------- | ----- | ----- |
| cassiobotaro | user@1234 | yes   | no    |
| user         | user1234  | no    | no    |
| userg        | user1234  | no    | yes   |
