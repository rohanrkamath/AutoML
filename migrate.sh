rm -r migrations
rm myproject/data.sqlite
flask db init
flask db migrate -m 'first migration'
flask db upgrade
rm -r user_profiles/*