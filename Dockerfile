FROM python:3
WORKDIR /usr/src/app

RUN pip install oci

COPY . .

CMD [ "python", "./run.py" ]
