 start "Development Mail Server" python -m smtpd -n -c DebuggingServer localhost:1025
 start "Development Django Server" python dj_gplex\manage.py runserver
