FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

# Install build dependencies for compiling Python packages
# Install Tesseract OCR for pytesseract
RUN yum update -y && \
    yum install -y gcc gcc-c++ make cmake python3-devel tesseract tesseract-devel && \
    yum clean all

# Upgrade pip and install wheel
RUN pip install --upgrade pip setuptools wheel

# Copy and install Python dependencies
# Using PyMuPDF <1.24.0 to avoid C++20 requirement (compatible with GCC 7.3.1)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ./

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the Lambda handler
CMD ["lambda_handler.lambda_handler"]