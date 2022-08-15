FROM python:3.7-slim
WORKDIR /back 
COPY requirements.txt /back
RUN pip3 install -r /back/requirements.txt --no-cache-dir
COPY ./ /back
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
