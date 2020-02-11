FROM alpine:3.11

LABEL version="1.0" \
      description="Run `kakoune-blackboard` in a docker container" \
      maintainer="Frank LENORMAND <lenormf@gmail.com>" \
      source="https://github.com/kakoune-editor/kakoune-blackboard"

RUN \
    apk update \
    && echo http://dl-cdn.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories \
    && apk add git kakoune python3

RUN \
    addgroup kakoune \
    && adduser -D -G kakoune kakoune \
    && chown -R kakoune:kakoune /home/kakoune

USER kakoune

RUN \
    cd /home/kakoune \
    && git clone https://github.com/kakoune-editor/kakoune-blackboard.git

WORKDIR /home/kakoune/kakoune-blackboard

RUN \
    python3 -m venv .env \
    && source .env/bin/activate \
    && pip3 install -r requirements.txt

COPY kakoune_blackboard.cfg .

CMD source .env/bin/activate \
    && irc3 -d kakoune_blackboard.cfg
