#!/bin/sh
celery -A Autocorreccion worker -B -l info --concurrency=1  -n BeatDAu &
celery -A Autocorreccion worker -Q autocorrect  -l info --concurrency=25
# celery -A ApiProvisioning worker -Q snmp_traps  --pool=solo -l  info --concurrency=10  & 
# celery -A ApiProvisioning worker -Q snmp_traps -l info --concurrency=250