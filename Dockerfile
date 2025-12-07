FROM python:3.12

RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/
