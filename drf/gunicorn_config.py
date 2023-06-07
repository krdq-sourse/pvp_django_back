command = '/home/www/code/venv/bin/gunicorn'
pythonpath = '/home/www/code/drf'
bind = '127.0.0.1:8000'
workers = 5
user = 'root'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=drf.settings'