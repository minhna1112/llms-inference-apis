FROM python:3.9.16-slim-buster


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    dpkg-sig \
    python3-dev 


RUN pip3 install --upgrade pip

WORKDIR /app

COPY requirements/client.requirements requirements.txt

RUN pip3 install -r requirements.txt

COPY src/tgi_client .

COPY .env .env

EXPOSE 5000

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "5000", "app:app"]
