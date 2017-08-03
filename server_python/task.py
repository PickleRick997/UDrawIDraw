from flask import Flask
from celery import Celery
from pyfcm import FCMNotification

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
	
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask('task_1094635483')
app.config.update(CELERY_BROKER_URL='amqp://guest@localhost')
celery = make_celery(app)

@celery.task()
def distribute(token, user_name, msg):
    push_service = FCMNotification(api_key="AAAA13g3h9w:APA91bEWrlBUNq1uL3q6-O_ue6LGEh7s7QCn7EpN-7_MR9S6F-b0DjTgyP0rwDpmVZlTjD5A8FN9UAn9mxB3gTmWBclTxUcSrUO891G1Uw9Xs-DNOQdcDhnW89fdycPtiIR3KjlfJRMk")

    print('get msg:')
    print(msg)
    print('from:' + user_name)
    result = push_service.notify_multiple_devices(
        registration_ids=token,
        data_message = msg)