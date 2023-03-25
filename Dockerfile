FROM debian:11

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install -r requirements.txt --no-cache-dir && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["python3", "main.py"]