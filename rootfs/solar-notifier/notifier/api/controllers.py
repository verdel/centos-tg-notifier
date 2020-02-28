from flask import Blueprint, g, current_app
from flask_restful import Api, Resource, reqparse
from notifier.data.models import Channels, User
from mongoengine.queryset import Q
from flask_httpauth import HTTPTokenAuth
import telegram
from emoji import emojize
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
parser = reqparse.RequestParser()
parser.add_argument('message', required=True, help='Message text')

auth = HTTPTokenAuth()
if current_app.config.get('TG_PROXY_URL'):
    request = telegram.utils.request.Request(proxy_url=current_app.config.get('TG_PROXY_URL'),
                                             urllib3_proxy_kwargs={'username': current_app.config.get('TG_PROXY_USER'),
                                                                   'password': current_app.config.get('TG_PROXY_PASS')})
    bot = telegram.Bot(token=current_app.config.get('TG_TOKEN'), request=request)
else:
    bot = telegram.Bot(token=current_app.config.get('TG_TOKEN'))


@auth.verify_token
def verify_token(token):
    try:
        application = Channels.objects(token=token).first()

    except Exception:
        application = None

    if not application:
        return False

    g.application = application.name
    return True


class MessageItem(Resource):
    method_decorators = [auth.login_required]

    def post(self):
        args = parser.parse_args()
        channel = Channels.objects(name=g.application).first()
        users = User.objects(Q(channels__contains=channel) & Q(chatId__exists=True))
        message = emojize(args['message'], use_aliases=True)
        if users:
            for user in users:
                try:
                    bot.send_message(chat_id=user.chatId, text=message)
                    result = {'success': True}, 200
                except telegram.TelegramError as e:
                    result = {'success': False, 'error': {'message': e.message}}, 400
        else:
            result = {'success': True}, 200
        return result


api.add_resource(MessageItem, '/message')
