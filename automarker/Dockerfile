FROM node:14.19

# Install Python3.9.5
WORKDIR /home/downloads

RUN apt-get update && apt-get install -y \
    software-properties-common \
    python-pip \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev wget

RUN curl -O https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tar.xz
RUN tar -xf Python-3.9.5.tar.xz
WORKDIR /home/downloads/Python-3.9.5
RUN ./configure --enable-optimizations
RUN make
RUN make altinstall
RUN python3.9 --version

RUN pip install virtualenv

# Install Java

RUN echo 'deb http://ftp.debian.org/debian stretch-backports main' | tee /etc/apt/sources.list.d/stretch-backports.list
RUN apt-get -y update
RUN apt-get -y install default-jdk
RUN apt-get -y install openjdk-11-jdk

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /home/node/app
COPY . .

RUN npm install -g jasmine
RUN npm install

ENV CLONE_PATH /clone
RUN mkdir $CLONE_PATH

ENV AUTO_MARKER_CONFIGURATION_REPO_PATH /home/node/app/project_config
COPY automarker-config $AUTO_MARKER_CONFIGURATION_REPO_PATH

ENV AUTO_MARKER_PORT 8080
EXPOSE $AUTO_MARKER_PORT

CMD [ "node", "app.mjs" ]
