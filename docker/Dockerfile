FROM python:3
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y zip wget awscli jq

ENV TERRAFORMVERSION=0.12.16

RUN aws configure set region eu-west-2 --profile default

RUN wget https://releases.hashicorp.com/terraform/${TERRAFORMVERSION}/terraform_${TERRAFORMVERSION}_linux_amd64.zip &&\
        wget https://releases.hashicorp.com/terraform/${TERRAFORMVERSION}/terraform_${TERRAFORMVERSION}_SHA256SUMS &&\
        wget https://releases.hashicorp.com/terraform/${TERRAFORMVERSION}/terraform_${TERRAFORMVERSION}_SHA256SUMS.sig &&\
        gpg --version &&\
        gpg --keyserver hkps://keyserver.ubuntu.com --receive-keys 51852D87348FFC4C &&\
        gpg -d terraform_${TERRAFORMVERSION}_SHA256SUMS.sig &&\
        sha256sum --ignore-missing -c terraform_${TERRAFORMVERSION}_SHA256SUMS &&\
        unzip terraform_${TERRAFORMVERSION}_linux_amd64.zip &&\
        chmod 555 terraform &&\
        cp terraform /bin/

COPY docker/sts-assume-role.sh /usr/local/bin/sts-assume-role.sh

RUN mkdir .target

# Install python deps
# COPY lambda/health_package/requirements-dev.txt .
# COPY lambda/health_package/requirements.txt .
# RUN pip install --no-cache-dir -r requirements-dev.txt
# ENV PYTHONDONTWRITEBYTECODE=1

# COPY . .
