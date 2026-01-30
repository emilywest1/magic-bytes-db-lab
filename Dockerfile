FROM ubuntu:latest

RUN apt-get update && apt-get install -y flask

WORKDIR /mb-lab

COPY . .

CMD ["/bin/bash"]