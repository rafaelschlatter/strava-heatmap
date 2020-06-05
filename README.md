# Strava-heatmap
[![Build Status](https://dev.azure.com/rafaelschlatter/strava-heatmap/_apis/build/status/rafaelschlatter.strava-heatmap?branchName=master)](https://dev.azure.com/rafaelschlatter/strava-heatmap/_build/latest?definitionId=17&branchName=master)
[![Requirements Status](https://requires.io/github/rafaelschlatter/strava-heatmap/requirements.svg?branch=master)](https://requires.io/github/rafaelschlatter/strava-heatmap/requirements/?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d8aa61d5c6bd469a9e05073088d998d3)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rafaelschlatter/strava-heatmap&amp;utm_campaign=Badge_Grade)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About
A flask web app that contains a static heatmap from GSP data from my Strava activities.

## Development
Requirements:
- Python 3.7 (i use 3.7 because the Azure app service that hosts this runs 3.7, but 3.5+ should also work)
- Docker & an account at Docker hub
- Azure subscription
- Account at Google reCAPTCHA

Create a virtual environment and install the dependencies:
````
pip install virtualenv
virtualenv venv # venv or env are common names for virtual environments
venv\scripts\activate # or source venv\bin\activate on mac/linux
pip install -r requirements.txt
````

The following environment variables are required to make use of all functionality:
- `GMAIL_ADRESS`
- `GMAIL_PW`
- `RECAPTCHA_USE_SSL`
- `RECAPTCHA_PUBLIC_KEY`
- `RECAPTCHA_PRIVATE_KEY`

You can run the app locally with (you might want to change the `host` and `port` when calling `app.run()`):
````
python application.py
````
This is running a flask web server for development, you should not run this in production. 


## Deployment with Docker & Azure app service
### Build & push a container
It is easiest to deploy the app as a docker container. The container will start a gunicorn web server to run the application. Build and push the Docker image with the following commands:
````
docker login
docker build -t <your_docker_user>/stravaheatmap:latest .
docker push <your_docker_user>/stravaheatmap:latest
````

Running & testing the container locally (passing environment variables with `-e`):
````
docker run -p 5000:8080 -e SECRET_KEY=<your_secret_key> -e GMAIL_ADRESS=<your_gmail_adress> -e GMAIL_PW=<your_gmail_pw> -e RECAPTCHA_PRIVATE_KEY=<your_private_key> -e RECAPTCHA_PUBLIC_KEY=<your_public_key> <your_docker_user>/stravaheatmap:latest
````

Point a browser to <http://localhost:5000/> to see the containerized app running.

### Host it on an Azure app service
tba ...

## License
This project is licensed under the the MIT license. See [LICENSE](LICENSE.txt) for details.