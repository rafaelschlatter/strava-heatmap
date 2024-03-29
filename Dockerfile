FROM python:3.9-slim
LABEL maintainer="rafaelschlatter@gmail.com"
RUN useradd -ms /bin/bash myuser
WORKDIR /app
COPY . /app
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN chmod +x boot.sh
RUN chown -R myuser:myuser ./
USER myuser
EXPOSE 8080
ENTRYPOINT ["./boot.sh"]
