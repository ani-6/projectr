python manage.py seed_users

0 */6 * * * /path/to/venv/bin/python /path/to/projectr/manage.py check_system_health >> /path/to/projectr/logs/health_check.log 2>&1