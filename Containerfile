FROM python:3.12-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir Flask
EXPOSE 8080
ENV NAME Webhook
CMD ["python", "./main.py"]
