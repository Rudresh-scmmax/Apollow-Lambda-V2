FROM public.ecr.aws/lambda/python:3.11

# Install build dependencies for compiling Python packages
RUN yum update -y && \
    yum install -y gcc gcc-c++ make cmake python3-devel && \
    yum clean all

# Verify compiler version (optional)
RUN gcc --version && g++ --version

# Copy requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your Lambda code
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}
COPY insert_forecast_data.py ${LAMBDA_TASK_ROOT}
COPY db_query.py ${LAMBDA_TASK_ROOT}
# Lambda entrypoint
CMD [ "lambda_handler.lambda_handler" ]
