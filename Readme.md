# Object detection lambda

TODO

- `download_model.py`: Script to download the detr-resnet-50. Must be executed prior to the Docker image build.
- `Dockerfile`
- `docker_build_and_push.sh`: Commands to build and push the image to ECR. Also there are comments on how to test the lambda locally with the LRIE.
- `lambda_function.py`: Lambda function that takes the s3 bucket and key from the event, reads the image and perform an object detection inference on it. It saves the detected objects on a json and a output image with the bounding boxes in the same bucket.
- `test_event.json`: Json to use as a test event for created objects in a s3 bucket.