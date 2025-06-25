FROM python:3.10
WORKDIR /test_app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /test_app/

ENV PYTHONPATH=/test_app

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
