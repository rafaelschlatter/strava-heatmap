# strava-heatmap
[![Build Status](https://dev.azure.com/rafaelschlatter/strava-heatmap/_apis/build/status/rafaelschlatter.strava-heatmap?branchName=master)](https://dev.azure.com/rafaelschlatter/strava-heatmap/_build/latest?definitionId=17&branchName=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d8aa61d5c6bd469a9e05073088d998d3)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rafaelschlatter/strava-heatmap&amp;utm_campaign=Badge_Grade)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About
A flask web app that contains a static heatmap from GSP data from my Strava activities.

## Development
Requirements:
- Python 3.7 (i use 3.7 because the Azure app service that hosts this runs 3.7, but 3.5+ should also work),
- Docker & an account at Docker hub
- Azure subscription (I choose services that only incure a minimum cost for running this)

Create a virtual environment and install the dependencies:
````
pip install virtualenv
virtualenv venv # venv or env are common names for virtual environments
venv\scripts\activate # or source venv\bin\activate on mac/linux
pip install -r requirements.txt
````

You can run the app locally with (you might need to change the `host` and `port` when calling `app.run()`):
````
python application.py
````

## Deployment with Docker & Azure app service
### Build & push a container
It is easiest to deploy the app as a docker container, build and push the Docker image with the following commands:
````
docker login
docker build -t rafaelschlatter/stravaheatmap:latest .
docker push rafaelschlatter/stravaheatmap:latest
````

### Host it on an Azure app service
tba ...
