#!/bin/sh

set -e

if ! python manage.py migrate --plan | grep 'No planned migration' > /dev/null
then
  echo "### Applying migrations."
  python manage.py migrate
fi

if [ -n "$APP_USER" ] && [ -n "$APP_PASSWORD" ]
then
  echo "### Creating user $APP_USER if not exists."
  python manage.py shell -c "from core.models import User; \
                             user, _ = User.objects.get_or_create( \
                                 login='$APP_USER'
                             ); \
                             user.is_superuser=True; \
                             user.is_staff=True; \
                             user.set_password('$APP_PASSWORD'); \
                             user.save()"
fi

if [ -n "$PROD" ]
then
  echo "### Collecting staticfiles."
  python manage.py collectstatic --no-input --clear

  echo "### Starting gunicorn server."
  gunicorn base.wsgi --bind=0.0.0.0:8000 --workers=4 --timeout 600
else
  echo "### Starting django development server."
  python manage.py runserver 0.0.0.0:8005
fi