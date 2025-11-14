FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

RUN yum update -y && \
    yum install -y gcc gcc-c++ make && \
    yum clean all

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY get_correlation_data.py .
COPY db_query.py .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["get_correlation_data.lambda_handler"]
