REGISTRY ?=
IMAGE_OWNER ?=
IMAGE_NAME ?= tc31-xar-base
IMAGE_TAG ?= latest

IMAGE = $(REGISTRY)$(IMAGE_OWNER)$(IMAGE_NAME)

APT_AUTH_CONF?=./tc31-xar-base/apt-config/bhf.conf

build-image:
	docker build --no-cache --secret id=apt,src=$(APT_AUTH_CONF) --network host -t $(IMAGE):$(IMAGE_TAG) -f ./tc31-xar-base/Dockerfile ./tc31-xar-base

push-image:
	docker push $(IMAGE):$(IMAGE_TAG)

run-containers:
	docker compose up -d

list-containers:
	docker compose ps -a

stop-and-remove-containers:
	docker compose down

container-logs:
	docker compose logs -ft
