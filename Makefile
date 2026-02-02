.PHONY: all build run stop clean

IMAGE_NAME := db-lab_image
CONTAINER_NAME := db-lab_container

all: stop clean build run

build:
	sudo docker build -t $(IMAGE_NAME) .

run:
	sudo docker run -p 5000:5000 -it --name $(CONTAINER_NAME) $(IMAGE_NAME) /bin/bash

stop:
	-sudo docker stop $(CONTAINER_NAME)

clean:
	-sudo docker image prune -f
	-sudo docker container prune -fS