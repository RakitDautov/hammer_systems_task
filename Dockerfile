FROM python:3.10

WORKDIR /app
COPY requirements.txt .
COPY entrypoint.sh .
RUN pip install -r /app/requirements.txt --no-cache-dir
RUN chmod +x entrypoint.sh
COPY api_referal .
ENTRYPOINT ["/app/entrypoint.sh"]