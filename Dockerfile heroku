FROM python:3.10.5

WORKDIR /

RUN apt-get update

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD python app.py