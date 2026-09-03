FROM python:3.13-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt 

# OLD: EXPOSE 80 (Direct public port binding without Nginx)
EXPOSE 5000

# OLD: CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]



