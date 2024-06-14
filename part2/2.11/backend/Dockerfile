FROM osgeo/gdal:alpine-normal-3.5.3

ENV PYTHONUNBUFFER2 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Install required system packages
RUN apk add --no-cache python3 py3-pip postgresql-client geos

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your application
COPY . /app

# Use an entrypoint script to conditionally run migrations
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
