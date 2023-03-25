FROM debian:11

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y python3 && \
    pip3 install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]