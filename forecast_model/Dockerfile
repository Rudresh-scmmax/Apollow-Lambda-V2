FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies for compilation
RUN yum update -y && \
    yum install -y gcc gcc-c++ make cmake3 && \
    yum clean all

# Set environment variables
ENV CC=gcc
ENV CXX=g++

# Copy requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy Lambda handler code
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}
COPY insert_forecast_data.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_handler.lambda_handler" ]
