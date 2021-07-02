#Download base image ubuntu 18.04
FROM python:3.9.5-slim-buster

ENV APP_DIR=/opt/app

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
    && rm -rf /var/lib/apt/lists/

RUN wget https://mirrors.huaweicloud.com/java/jdk/8u151-b12/jdk-8u151-linux-x64.tar.gz 
RUN tar zxvf jdk-8u151-linux-x64.tar.gz 
RUN rm -d jdk-8u151-linux-x64.tar.gz
RUN mv jdk1.8.0_151 /usr/lib/jvm
ENV JAVA_HOME /usr/lib/jvm/jdk1.8.0_15/
RUN export JAVA_HOME

RUN echo "export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_15/" >> ~/.bashrc

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/" >> ~/.bashrc

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*



WORKDIR ${APP_DIR}
COPY openapi_server openapi_server/
COPY data data/
COPY requirements.txt prod-requirements.txt uwsgi.ini ./
RUN pip install --no-cache-dir \
    -r requirements.txt -r prod-requirements.txt

RUN pip3 install --upgrade pip
# You only need pyspark and spark-nlp paclages to use Spark NLP
# The rest of the PyPI packages are here as examples
RUN pip3 install --no-cache-dir pyspark==3.1.1 spark-nlp==3.1.1
# numpy pandas mlflow Keras matplotlib pydot tensorflow==2.4.1 graphviz

WORKDIR /
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]

# Specify the default command to run
# Run server in development mode
CMD ["python", "-m", "openapi_server"]