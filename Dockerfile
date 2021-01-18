FROM python:3.8-slim-buster
RUN apt-get update \
    && apt-get install build-essential -y \
    && apt-get install libc6 -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./project/app .

EXPOSE 8083

CMD ["uvicorn", "main:app", "--port", "8083", "--host", "0.0.0.0", "--reload"]
