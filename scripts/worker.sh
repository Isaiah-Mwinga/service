#!/bin/bash
celery -A app.workers.celery_app worker --loglevel=info
celery -A app.workers.celery_app worker --loglevel=info --pool=solo
