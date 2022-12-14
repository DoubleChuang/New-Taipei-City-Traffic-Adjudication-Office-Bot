FROM python:3.7
LABEL maintainer="Double <ethan9141@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y tesseract-ocr \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /tmp/src
WORKDIR /tmp/src
RUN sed -i "s/__commit_hash__.*/__commit_hash__ = '$(git rev-parse --short HEAD)'/g" /tmp/src/ntpc_tad_bot/__init__.py
RUN pip install /tmp/src && rm -rf /tmp/src

ENV DEBIAN_FRONTEND=dialog

WORKDIR /
CMD ["ntpc_tad_bot"]
