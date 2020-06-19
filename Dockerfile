FROM        alpine:3.9

ARG         VER
ENV         VER=${VER}

ARG         DIR=/app

WORKDIR     $DIR
ADD .       $DIR

RUN         apk add -U ca-certificates linux-headers make automake autoconf libtool netcat-openbsd
RUN         apk add -U gcc g++ python3 python3-dev postgresql-dev

RUN         pip3 install -r requirements.txt

EXPOSE      8080

CMD         make api