default: docker_build

DOCKER_IMAGE ?= bskim45/s3-url-shortener
DOCKER_TAG ?= `git rev-parse --abbrev-ref HEAD`
APP_VERSION ?= `cat version.txt`

docker_build:
	@docker build \
	  --build-arg VCS_REF=`git rev-parse --short HEAD` \
	  --build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
	  --build-arg APP_VERSION=$(APP_VERSION) \
	  -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker_push:
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)
