#https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/
FROM python:3.10
WORKDIR /test_app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY ./app /test_app/
# COPY ../test_app ./src

ENV PYTHONPATH=/test_app

EXPOSE 8000

# # Setup an app user so the container doesn't run as the root user
# RUN useradd app
# USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]