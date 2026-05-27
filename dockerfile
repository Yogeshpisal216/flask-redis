FROM python:3.12

RUN pip install flask

COPY website/ .

EXPOSE 5000

CMD [ "python", "app.py" ]