FROM        python:3.8.3

ARG         VER
ENV         VER=${VER}

ARG         DIR=/app

WORKDIR     $DIR
ADD .       $DIR

#RUN         apt update
#RUN         apt install -y ca-certificates linux-headers make automake autoconf libtool netcat-openbsd
#RUN         apt install -y g++ python3 python3-dev

RUN         pip3 install -r requirements.txt

EXPOSE      8080

CMD         make api