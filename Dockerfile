# syntax=docker/dockerfile:1.2
FROM python:3.9-slim

RUN pip install pipenv

WORKDIR /app

# must be installed using pip
RUN pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "kitchenware-model.tflite", "./"]

# EXPOSE 9696

CMD ["prediction.predict"]