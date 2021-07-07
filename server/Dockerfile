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
        pkg-config \
        software-properties-common \
        graphviz\
        wget \
        nano \
        sudo \
    && apt-get -y autoclean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_FOLDER java-se-8u41-ri

ENV JVM_ROOT /usr/lib/jvm

ENV JAVA_PKG_NAME openjdk-8u41-b04-linux-x64-14_jan_2020.tar.gz
ENV JAVA_TAR_GZ_URL https://download.java.net/openjdk/jdk8u41/ri/$JAVA_PKG_NAME

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*    && \
    apt-get clean                                                               && \
    apt-get autoremove                                                          && \
    echo Downloading $JAVA_TAR_GZ_URL                                           && \
    wget -q $JAVA_TAR_GZ_URL                                                    && \
    tar -xvf $JAVA_PKG_NAME                                                     && \
    rm $JAVA_PKG_NAME                                                           && \
    mkdir -p /usr/lib/jvm                                                       && \
    mv ./$JAVA_FOLDER $JVM_ROOT                                                 && \
    update-alternatives --install /usr/bin/java java $JVM_ROOT/$JAVA_FOLDER/bin/java 1        && \
    update-alternatives --install /usr/bin/javac javac $JVM_ROOT/$JAVA_FOLDER/bin/javac 1     && \
    java -version
####
#### OPTIONAL : 4. SET JAVA_HOME environment variable, uncomment the line below if you need it

ENV JAVA_HOME=$JVM_ROOT/$JAVA_FOLDER


#Install Spark
RUN mkdir /opt/spark
RUN wget https://downloads.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop2.7.tgz
RUN tar xvf spark-3.1.2-bin-hadoop2.7.tgz
RUN mv spark-3.1.2-bin-hadoop2.7/* /opt/spark
RUN rm -d spark-3.1.2-bin-hadoop2.7.tgz


RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR ${APP_DIR}
COPY openapi_server openapi_server/
COPY data data/
COPY requirements.txt prod-requirements.txt uwsgi.ini ./
RUN pip install --no-cache-dir \
    -r requirements.txt -r prod-requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir pyspark==3.1.1 spark-nlp==3.1.0 numpy pandas 
RUN pip install -q spark-nlp-jsl==3.1.0 --extra-index-url https://pypi.johnsnowlabs.com/3.1.0-1778570a3f59d3059ed1e58375192fd61b114fc9 --upgrade

ENV SPARK_HOME="/opt/spark/"



RUN echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc
RUN echo "source ~/.bashrc"
RUN echo "export PATH=$PATH:/opt/spark/bin:/opt/spark/sbin" >> ~/.bashrc
RUN echo "export JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
RUN echo "source ~/.bashrc"
RUN echo "export PYSPARK_PYTHON=/usr/local/bin/python" >> ~/.bashrc
RUN echo "source ~/.bashrc"

RUN echo "bin/spark-shell --conf 'spark.driver.extraJavaOptions=-Dhttp.proxyHost=<proxyHost> -Dhttp.proxyPort=<proxyPort> -Dhttps.proxyHost=<proxyHost> -Dhttps.proxyPort=<proxyPort>' --packages <somePackage>"

RUN echo "export JSL_SECRET=${JSL_SECRET}" >> ~/.bashrc
RUN echo "export SPARK_NLP_LICENSE=${SPARK_NLP_LICENSE}" >> ~/.bashrc 
RUN echo "export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" >> ~/.bashrc
RUN echo "export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" >> ~/.bashrc 
RUN echo "export JSL_VERSION=${JSL_VERSION}" >> ~/.bashrc 
RUN echo "export PUBLIC_VERSION=3.1.0" >> ~/.bashrc


WORKDIR /
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]

# Run server in development mode
# CMD ["python", "-m", "openapi_server"]

# Run server in production mode
CMD ["uwsgi", "--ini", "uwsgi.ini", "--lazy", "--http", ":8080"]
