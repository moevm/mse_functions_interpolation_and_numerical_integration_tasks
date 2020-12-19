FROM ubuntu:18.04
LABEL maintainer="myxin200015@mail.ru"
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY ./ ./

RUN apt-get update && apt-get upgrade -y
RUN apt-get install \
	python3.8 \
	python3-pip \
	python3-dev \
	texlive-fonts-recommended \
	texlive-lang-cyrillic \
	texlive-latex-extra \
	texlive-latex-recommended -y
RUN python3.8 -m pip install -r requirements.txt

WORKDIR /app/Generator
ENTRYPOINT ["python3.8", "manage.py", "runserver", "0.0.0.0:8000"]