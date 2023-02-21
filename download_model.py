from transformers import DetrImageProcessor, DetrForObjectDetection

def get_model(model):
    """Loads model from Hugginface model hub"""
    try:
        model = DetrForObjectDetection.from_pretrained(model)
        model.from_pretrained('./model')
    except Exception as e:
        raise e


def get_processor(processor):
    """Loads tokenizer from Hugginface model hub"""
    try:
        processor = DetrImageProcessor.from_pretrained(processor)
        processor.from_pretrained('./model')
    except Exception as e:
        raise e


get_model("facebook/detr-resnet-50")
get_processor("facebook/detr-resnet-50")
