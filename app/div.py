import logging

workers = 4
threads = 2
loglevel = 'info'

logger = logging.getLogger('gunicorn.error')
logger.setLevel(logging.INFO)
accesslog = 'access.log'
access_log_format = '%(t)s %(s)s %(h)s "%(r)s" %(m)s'
