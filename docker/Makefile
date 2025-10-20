include ../config.mk

IMAGE_NAME=perseqpipe_viz
DOCKER_USER=ktrachtok

# Build for amd64
docker_build_amd64: Dockerfile
	docker buildx build \
		--platform linux/amd64 \
		-t $(IMAGE_NAME):amd64-$(PERSEQPIPE_VIZ_VERSION) \
		-f Dockerfile ..

# Build for arm64
docker_build_arm64: Dockerfile
	docker buildx build \
		--platform linux/arm64 \
		-t $(IMAGE_NAME):arm64-$(PERSEQPIPE_VIZ_VERSION) \
		-f Dockerfile ..

# Tag images
docker_tag_amd64:
	docker tag $(IMAGE_NAME):amd64-$(PERSEQPIPE_VIZ_VERSION) $(DOCKER_USER)/$(IMAGE_NAME):amd64-$(PERSEQPIPE_VIZ_VERSION)
	
docker_tag_arm64:
	docker tag $(IMAGE_NAME):arm64-$(PERSEQPIPE_VIZ_VERSION) $(DOCKER_USER)/$(IMAGE_NAME):arm64-$(PERSEQPIPE_VIZ_VERSION)

# Push images
docker_push_amd64:
	docker push $(DOCKER_USER)/$(IMAGE_NAME):amd64-$(PERSEQPIPE_VIZ_VERSION)

docker_push_arm64:
	docker push $(DOCKER_USER)/$(IMAGE_NAME):arm64-$(PERSEQPIPE_VIZ_VERSION)

# Optional: Build all and push
docker_all: docker_build_amd64 docker_build_arm64 docker_tag_amd64 docker_tag_arm64 docker_push_amd64 docker_push_arm64