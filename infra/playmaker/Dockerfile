FROM docker:18.09

RUN apk add --no-cache \
    bash \
    bash-completion \
    vim \
    python3

COPY requirements.txt /home

WORKDIR /home

RUN pip3 install -r requirements.txt

COPY scripts ./scripts