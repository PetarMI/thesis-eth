FROM docker:dind

RUN apk add --no-cache \
		bash \
        vim

WORKDIR /home

COPY frr ./frr
COPY scripts ./scripts
