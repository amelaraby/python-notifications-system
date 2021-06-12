import json
from flask import Flask, request
from flask_injector import FlaskInjector
from dependencies import configure
from injector import inject
from mq.message_queue import MessageQueue
from service import NotificationService

app = Flask(__name__)


def __validateNotificationInput(input):
    if input['type'] not in ['email', 'sms', 'push']:
        return 'Type should be one of email, sms, push'

    if "notifiable" not in input.keys():
        return 'Notifiable is required'

    if "message" not in input.keys():
        return 'Message is required'


@inject
@app.route('/asyncNotify', methods=['POST'])
def asyncNotify(mq: MessageQueue):
    request_data = request.get_json()
    error = __validateNotificationInput(request_data)
    if error:
        return {'success': False, 'message': error}, 400

    try:
        mq.publish(json.dumps(request_data))

        return {"success": True}, 200
    except Exception as e:
        return {"success": False, 'message': str(e)}, 500


@app.route('/syncNotify', methods=['POST'])
def syncNotify():
    request_data = request.get_json()
    error = __validateNotificationInput(request_data)

    if error:
        return {'success': False, 'message': error}, 400

    try:
        NotificationService().send(request_data)

        return {"success": True}, 200
    except Exception as e:
        return {"success": False, 'message': str(e)}, 500


FlaskInjector(app=app, modules=[configure])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
