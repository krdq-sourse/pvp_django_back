#!/bin/bash
	source /home/www/code/venv/bin/activate
	source /home/www/code/venv/bin/postactivate
	exec gunicorn  -c "/home/www/code/drf/gunicorn_config.py" drf.wsgi