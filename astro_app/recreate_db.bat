set PGPASSWORD=1
psql -U postgres < recreate_db.sql

call ..\.venv\Scripts\activate
python manage.py migrate

echo from rest_app.controllers.init_db import InitorSystem; InitorSystem().init() | python manage.py shell