FROM        selenium/standalone-chrome:4.0.0

USER        root

ARG         VER
ENV         VER=${VER}

COPY        scrap/ /app/

RUN         apt update && apt install python3-pip -y

ADD         requirements.txt /mnt/
RUN         pip3 install -r /mnt/requirements.txt
