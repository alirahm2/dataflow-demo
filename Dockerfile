FROM gcr.io/revolut-ds/data-infra/revolut-python:3.7 AS base

ARG PYPIUSER
ENV PYPIUSER=${PYPIUSER}
ARG PYPIPASS
ENV PYPIPASS=${PYPIPASS}


# INSTALL REQUIRED SERVICE
USER root
RUN apt-get update \
    && apt-get install -y apt-transport-https ca-certificates gnupg google-cloud-sdk

## MOVE SERVICE AND INSTALL PACKAGES
RUN mkdir /data && chown revolut:revolut /data

USER revolut

COPY Pipfile Pipfile.lock ./

RUN pipenv install --skip-lock --system

COPY --chown=revolut:revolut . .
CMD python setup.py sdist
CMD python -m main.py --runner DataflowRunner --project revolut-ds \
    --temp_location gs://revolut-ds/tmp/ \
    --subnetwork https://www.googleapis.com/compute/v1/projects/revolut-ds/regions/europe-west1/subnetworks/default \
    --staging_location=gs://revolut-ds/tmp/ \
    --extra_package=dist/app-1.0.0.tar.gz \
    --setup_file=./setup.py