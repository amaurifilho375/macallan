# Macallan Django App - Template

This repository is a ready-to-run template for the Macallan form + Django admin test.

##

- opteo por compilar .po → .mo com gettext

- sudo apt install gettext

- pip install django-widget-tweaks

## Requirements

- Python 3.10+
- pip
- (optional) Docker & docker-compose

## Quick start (local, no Docker)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py create_readonly_group
python manage.py compilemessages
python manage.py runserver
```

- Open the public form: http://localhost:8000/macanall (typo in older versions — correct path is `/macallan/`)
- Admin: http://localhost:8000/admin/

## Docker (optional)

Use the included Dockerfile and docker-compose.yml to run via Docker.

## Internationalization

Strings in code use `gettext_lazy`. To create Portuguese translations:

```bash
django-admin makemessages -l pt_BR
# edit locale/pt_BR/LC_MESSAGES/django.po
django-admin compilemessages
```

## Notes

http://localhost:8000/macallan/ #rotas para formulario

http://127.0.0.1:8000/admin #rota admin

http://127.0.0.1:8000/macallan/clients/ #rotas para listagem
