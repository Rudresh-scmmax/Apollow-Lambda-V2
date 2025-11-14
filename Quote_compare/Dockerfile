FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

RUN yum update -y && \
    yum install -y gcc postgresql-devel postgresql-libs && \
    yum clean all

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["quote_comapare.lambda_handler"]
