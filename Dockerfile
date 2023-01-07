FROM python:3
WORKDIR /usr/src/app

RUN pip3 install oci

COPY . .

CMD [ "python3", "./run.py" ]
