#https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/
FROM python:3.10
WORKDIR /my_test_app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY ./ ./
# COPY ../test_app ./src

EXPOSE 8000

# # Setup an app user so the container doesn't run as the root user
# RUN useradd app
# USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]