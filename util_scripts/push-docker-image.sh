
export LOCAL_DOCKER_IMAGE_NAME=cybulde-data-processing
export GCP_DOCKER_IMAGE_NAME=asia-south1-docker.pkg.dev/cybulde-427611/cybulde-images/cybulde-data-processing

gcloud auth configure-docker --quiet asia-south1-docker.pkg.dev
docker tag ${LOCAL_DOCKER_IMAGE_NAME}:latest ${GCP_DOCKER_IMAGE_NAME}:1
docker push ${GCP_DOCKER_IMAGE_NAME}:1
