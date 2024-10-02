FROM python:3.12.6-slim-bookworm
EXPOSE 8080
WORKDIR /app/
COPY  . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
