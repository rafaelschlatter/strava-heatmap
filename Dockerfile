FROM python:3.7-slim
LABEL maintainer="rafaelschlatter@gmail.com"
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "--config", "./conf/gunicorn_conf.py", "application:app"]
