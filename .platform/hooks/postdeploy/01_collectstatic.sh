#!/bin/bash
set -e
export $(cat /opt/elasticbeanstalk/deployment/env | grep -v '^#' | xargs)
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py migrate --noinput
python manage.py collectstatic --noinput