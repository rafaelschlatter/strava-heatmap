# strava-heatmap
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d8aa61d5c6bd469a9e05073088d998d3)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rafaelschlatter/strava-heatmap&amp;utm_campaign=Badge_Grade)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About
A flask web app that contains a static heatmap from GSP data from Strava activities.

## Development
Requirements:
- Python 3.6,
- Docker & an account at Docker hub
````
pip install -r requirements.txt
````


## Build Docker image
Build and push the Docker image:
````
docker login
docker build -t rafaelschlatter/stravaheatmap:latest .
docker push rafaelschlatter/stravaheatmap:latest
````

## Host it on an Azure container instance
tba ...