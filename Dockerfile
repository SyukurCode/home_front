# syntax=docker/dockerfile:1

FROM python:3.10.12-slim-buster

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir /app/logs
RUN touch /app/logs/gui.log

COPY . .

# Set environment variable untuk debug mode
ENV FLASK_APP=index.py
ENV FLASK_ENV=development  

# Jalankan Flask
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
# CMD [ "python3", "index.py"]
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "index:app"]