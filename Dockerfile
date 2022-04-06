FROM ubuntu:18.04
LABEL maintainer="myxin200015@mail.ru"
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get install \
	python3.8 \
	python3-pip \
	python3-dev \
  texlive-fonts-extra \
  texlive-lang-greek \
	texlive-lang-cyrillic \
	texlive-lang-greek \
	texlive-latex-extra \
	texlive-latex-recommended -y

WORKDIR /app
COPY ./ ./
RUN python3.8 -m pip install -r requirements.txt

WORKDIR /app/Generator
ENTRYPOINT ["python3.8", "manage.py", "runserver", "0.0.0.0:8000"]
