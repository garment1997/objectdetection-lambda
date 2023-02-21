#!/bin/bash

# Build image
docker build -t objectdetection-lambda .
docker run -p 9000:8080 --env-file env_file.txt objectdetection-lambda

# Test locally
curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations -d "{\"Records\":[{\"s3\":{\"bucket\":{\"name\":\"objectdetection-dev\"},\"object\":{\"key\":\"input-image-gasolinera.jpg\"}}}]} "

# Create repository
aws ecr create-repository --repository-name objectdetection --region eu-west-1

# Push image to ECR
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 178541015878.dkr.ecr.eu-west-1.amazonaws.com

# Tag our previously created image to an ECR format
docker tag objectdetection-lambda  178541015878.dkr.ecr.eu-west-1.amazonaws.com/objectdetection

# Push it to ECR
docker push 178541015878.dkr.ecr.eu-west-1.amazonaws.com/objectdetection

