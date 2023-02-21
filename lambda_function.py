import logging
from PIL import Image, ImageDraw
import json
import boto3
from io import BytesIO
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch


def detect_objects(event, context):
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Get bucket name and key
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    logging.info(f"Processing object with key: {key}")
    s3 = boto3.client("s3")

    # download image from S3
    response = s3.get_object(Bucket=bucket_name, Key=key)
    image_bytes = response["Body"].read()
    image = Image.open(BytesIO(image_bytes))

    # define confidence threshold
    threshold = 0.9

    # load model
    logging.info("Load model")
    processor = DetrImageProcessor.from_pretrained("./model")
    model = DetrForObjectDetection.from_pretrained("./model", use_pretrained_backbone=False)

    # process image
    logging.info("Starting inference")
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=threshold)[0]
    logging.info("Inference finished")

    # Create ImageDraw object to draw bounding boxes
    draw = ImageDraw.Draw(image)

    # create a list of results
    output = []
    i = 1
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        # Save and print results
        label = model.config.id2label[label.item()]
        confidence = round(score.item(), 3)
        box = [round(coord, 3) for coord in box.tolist()]
        result_dict = {'id': i, 'label': label, 'score': confidence, 'box': box}
        output.append(result_dict)
        logging.info(f"Id: {i}. Detected {label} with confidence {confidence} at location {box}")

        # Draw bounding box
        x, y, x2, y2 = tuple(box)
        draw.rectangle((x, y, x2, y2), outline="red", width=1)
        draw.text((x, y), f'{i} {label}', fill="white")

        i += 1

    # Save image with detected objects to S3
    output_key = key.replace(".jpg", ".jpg").replace('input', 'output')
    output_image_buffer = BytesIO()
    image.save(output_image_buffer, format="JPEG")
    s3.put_object(Bucket=bucket_name, Key=output_key, Body=output_image_buffer.getvalue())
    logging.info(f"Image with detected objects saved to: s3://{bucket_name}/{output_key}")

    # Save results as JSON file to S3
    json_key = key.replace('.jpg', '.json').replace('input', 'output')
    json_data = json.dumps(output)
    s3.put_object(Bucket=bucket_name, Key=json_key, Body=json_data)
    logging.info(f"Detection results saved to: s3://{bucket_name}/{json_key}")

    return {'status': 200}

# with open('test_event.json') as f:
#     event_data = json.load(f)
# detect_objects(event_data, 1)
# def detect_objects(event, context):
#     bucket_name = event['Records'][0]['s3']['bucket']['name']
#     key = event['Records'][0]['s3']['object']['key']
#     return {f'Hello {bucket_name} {key}!'}
