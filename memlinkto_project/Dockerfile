FROM tensorflow/tensorflow:2.12.0
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
