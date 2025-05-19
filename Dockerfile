FROM python:3.9.0

WORKDIR /home/

RUN echo "django_ar_image218"

RUN git clone https://github.com/Jamescode7/almighty_reading.git

WORKDIR /home/almighty_reading/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

RUN echo "REMEMBER 218"

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=almighty_reading.settings.deploy && python manage.py migrate --settings=almighty_reading.settings.deploy && gunicorn almighty_reading.wsgi --env DJANGO_SETTINGS_MODULE=almighty_reading.settings.deploy --bind 0.0.0.0:8000 -t 120"]
