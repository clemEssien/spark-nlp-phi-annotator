FROM python:3.9.5-slim-buster

ENV APP_DIR=/opt/app

ARG JSL_VERSION="3.1.0"
ENV JSL_VERSION=${JSL_VERSION}

ARG JSL_SECRET=""
ENV JSL_SECRET=${JSL_SECRET}

ARG SPARK_NLP_LICENSE=""
ENV SPARK_NLP_LICENSE=${SPARK_NLP_LICENSE}

ARG AWS_ACCESS_KEY_ID=""
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}

ARG AWS_SECRET_ACCESS_KEY=""
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

# hadolint ignore=DL3008
RUN apt-get update -qq -y \
    && apt-get install --no-install-recommends -qq -y \
        build-essential \
        gosu \
        libpcre3 \
        libpcre3-dev \
    && apt-get -y autoclean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR ${APP_DIR}
COPY openapi_server openapi_server/
COPY data data/
COPY requirements.txt prod-requirements.txt uwsgi.ini ./
RUN pip install --no-cache-dir \
    -r requirements.txt -r prod-requirements.txt

RUN export SPARK_HOME=/opt/spark

RUN pip install -q spark-nlp-jsl==${JSL_VERSION} --extra-index-url https://pypi.johnsnowlabs.com/${JSL_SECRET} --upgrade

WORKDIR /
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]

# Run server in development mode
# CMD ["python", "-m", "openapi_server"]

# Run server in production mode
CMD ["uwsgi", "--ini", "uwsgi.ini", "--lazy", "--http", ":8080"]