FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=config.settings
RUN python manage.py collectstatic --noinput
 
ARG DB_URL
ENV DB_URL=${DB_URL}
RUN python manage.py migrate --noinput
EXPOSE 8000
CMD ["gunicorn","--bind","0.0.0.0:8000","config.wsgi:application"]