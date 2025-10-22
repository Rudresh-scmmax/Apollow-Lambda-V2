FROM public.ecr.aws/lambda/python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./

CMD ["private_db_query.lambda_handler"]
