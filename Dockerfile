FROM python:3.9.12

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 4666

CMD gunicorn -w 5 -b 0.0.0.0:4666 app:app
# CMD waitress-serve --listen=*:5000 app:app