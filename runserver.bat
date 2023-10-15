 set DJANGO_SETTINGS_MODULE=dj_gplex.settings
 start "Development Mail Server" python -m smtpd -n -c DebuggingServer localhost:1025
 start "Development Websocket Server" python dj_gplex\ws_server.py
 start "Development Django Server" python dj_gplex\manage.py runserver
