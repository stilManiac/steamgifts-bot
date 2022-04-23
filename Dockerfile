FROM python:3.9-alpine

RUN mkdir -p /app
WORKDIR /app

# resolves gcc issue with installing regex dependency
RUN apk add build-base --no-cache

ENV VIRTUAL_ENV=/app/env
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./src/* /app/
VOLUME /config

CMD ["python", "run.py"]
