FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./notifications .

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD [ "python", "./main.py" ]