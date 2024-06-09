#!/bin/bash
service cron start
exec python3 main_app.py
