FROM ubuntu:18.04

# apt 업그레이트 및 업데이트
RUN apt-get -y update && apt-get -y dist-upgrade

# pip setuptools 업그레이드
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

# requirements만 복사
COPY requirements.txt /srv/requirements.txt
RUN pip3 install -r requirements.txt

# 소스 폴더 복사
COPY . /srv/airbnb-clone

# 작업 디렉토리 src로 변경
WORKDIR /src