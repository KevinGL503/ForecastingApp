FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /ForecastingApp

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 5578

RUN apt-get update && apt-get install -y cron
RUN chmod +x main_update.py
RUN echo "*/15 * * * * cd /ForecastingApp && /usr/local/bin/python /ForecastingApp/main_update.py >> /var/log/cron.log 2>&1" > /etc/cron.d/main-update-job \
    && chmod 0644 /etc/cron.d/main-update-job \
    && crontab /etc/cron.d/main-update-job \
    && touch /var/log/cron.log

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
