FROM tensorflow/tensorflow:latest
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
EXPOSE 8080