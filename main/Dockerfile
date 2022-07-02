FROM python:3.8-slim-buster

WORKDIR /usr/src/app
COPY request_info_provider/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY request_info_provider .
COPY utils .

CMD [ "python3", "-m" , "request_info_provider_app"]
