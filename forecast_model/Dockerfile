FROM public.ecr.aws/lambda/python:3.11

# Install build dependencies for compiling Python packages
RUN yum update -y && \
    yum install -y gcc gcc-c++ make cmake python3-devel && \
    yum clean all

# Verify compiler version (optional)
RUN gcc --version && g++ --version

# Copy requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install packages in stages to handle dependencies better
RUN pip install --no-cache-dir --upgrade pip

# Install core packages first
RUN pip install --no-cache-dir boto3==1.40.53 pandas==2.2.3 numpy==1.26.4

# Install scikit-learn and statsmodels
RUN pip install --no-cache-dir scikit-learn==1.5.2 statsmodels==0.14.4

# Install XGBoost
RUN pip install --no-cache-dir xgboost==2.1.1

# Install PyTorch (this is large, so install separately)
RUN pip install --no-cache-dir torch==2.5.1

# Install pyarrow
RUN pip install --no-cache-dir pyarrow==16.1.0

# Install darts with specific version that doesn't require C++20
RUN pip install --no-cache-dir darts==0.24.0 || \
    (pip install --no-cache-dir --no-deps darts==0.24.0 && \
     pip install --no-cache-dir --no-deps darts[torch]==0.24.0)

# Copy your Lambda code
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}
COPY insert_forecast_data.py ${LAMBDA_TASK_ROOT}
COPY db_query.py ${LAMBDA_TASK_ROOT}
# Lambda entrypoint
CMD [ "lambda_handler.lambda_handler" ]
