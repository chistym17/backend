FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=core/server.py

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 7755

CMD bash -c "rm -f core/store.sqlite3 && flask db upgrade -d core/migrations/ && bash run.sh"
