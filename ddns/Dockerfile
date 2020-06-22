FROM python:3.8
WORKDIR /app
COPY gcp_ddns.py requirements.txt ./

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
CMD ["./gcp_ddns.py"]
