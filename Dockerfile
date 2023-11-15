# pull official base image
FROM python:3.10.6-alpine

# set work directory
#WORKDIR /usr/src/

# set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
#Upgrade PIP
RUN python -m pip install --upgrade pip
#pymongo
RUN pip3 install pymongo

#ODBC
RUN apk add gcc
RUN apk add g++
RUN apk add unixodbc-dev
RUN apk add redis
RUN pip install setuptools
RUN pip install pyodbc
RUN pip install --upgrade pip
RUN apk add curl
RUN apk add --no-cache --upgrade bash
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN apk add rustup
RUN pip install make
RUN pip install --upgrade setuptools

#Download the desired package(s)
RUN apk add curl
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.5.2.1-1_amd64.apk


#Install the package(s)
RUN apk add --allow-untrusted msodbcsql17_17.5.2.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.5.2.1-1_amd64.apk
RUN apk add mssql-tools
RUN apk add unixodbc-dev

COPY requirements.txt .
COPY .env .
COPY start.sh .
COPY ./Autocorreccion/ .


RUN chmod +rx start.sh
RUN pip3 install -r requirements.txt

