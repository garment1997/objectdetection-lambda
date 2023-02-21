FROM public.ecr.aws/lambda/python:3.8

# install our dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code and models

COPY model/ ${LAMBDA_TASK_ROOT}/model/
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "lambda_function.detect_objects" ]