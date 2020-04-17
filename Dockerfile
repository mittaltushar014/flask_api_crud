



FROM mcr.microsoft.com/vscode/devcontainers/base:0-ubuntu-18.04
LABEL maintainer="Tushar Mittal"

ENV C_FORCE_ROOT=True
RUN apt-get update -y
RUN apt install -y systemd python3 python3-pip 

RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-amd64.deb
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-amd64.deb.sha512
RUN shasum -a 512 -c elasticsearch-7.6.2-amd64.deb.sha512 
RUN sudo dpkg -i elasticsearch-7.6.2-amd64.deb
RUN sudo update-rc.d elasticsearch defaults 95 10

COPY . /app
WORKDIR /app

RUN pip3 install wheel
RUN pip3 install -r requirements.txt

EXPOSE 5001 
ENTRYPOINT ["/bin/bash", "-c", "./deploy.sh"]
