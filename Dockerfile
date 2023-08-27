FROM python:3
WORKDIR /usr/src/app

RUN pip3 install oci
RUN pip3 install telethon

COPY . .

CMD [ "python3", "./run.py" ]
