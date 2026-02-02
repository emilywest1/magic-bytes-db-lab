FROM python:3.11-slim

WORKDIR /app
COPY database-server .
RUN apt-get update && apt-get install -y nano && \
    pip install --no-cache-dir flask pillow && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]