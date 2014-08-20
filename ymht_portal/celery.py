from __future__ import absolute_import

from celery import Celery

app = Celery('ymht_portal',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['ymht_portal.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()