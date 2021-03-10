import datetime
from json.decoder import JSONDecodeError
import logging
import time

from aiohttp.web import json_response
import bcrypt
from Crypto.Cipher import AES
from itsdangerous import BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from rest_api.b4e_rest_api.errors import ApiBadRequest
from rest_api.b4e_rest_api.errors import ApiNotFound
from rest_api.b4e_rest_api.errors import ApiUnauthorized

from rest_api.b4e_rest_api.blockchain_get_data import get_data_from_transaction
from rest_api.b4e_rest_api.blockchain_get_data import get_state
from rest_api.b4e_rest_api.blockchain_get_data import get_student_data
from rest_api.b4e_rest_api.blockchain_get_data import get_record_transaction

from config.config import SawtoothConfig
from rest_api.b4e_rest_api.route_handler.route_handler import decode_request, validate_fields, tolist, slice_per, \
    get_time

LOGGER = logging.getLogger(__name__)


class ClassRouteHandler(object):
    def __init__(self, loop, messenger, database):
        self._messenger = messenger
        self._database = database

    async def create_class(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'classId', 'subjectId', 'credit', 'teacherPublicKey', 'studentPublicKeys']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_create_class(private_key=body.get('privateKeyHex'),
                                                                 class_id=body.get('classId'),
                                                                 subject_id=body.get('subjectId'),
                                                                 credit=body.get('credit'),
                                                                 teacher_public_key=body.get('teacherPublicKey'),
                                                                 student_public_keys=body.get('studentPublicKeys'),
                                                                 timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactionId': transaction_id
            })

    async def create_classes(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'classes']
        validate_fields(required_fields, body)

        required_fields = ['classId', 'subjectId', 'credit', 'teacherPublicKey', 'studentPublicKeys']
        for class_ in body.get('classes'):
            validate_fields(required_fields, class_)

        list_transaction_id = await self._messenger.send_create_classes(private_key=body.get('privateKeyHex'),
                                                                        classes=body.get('classes'),
                                                                        timestamp=get_time())

        list_classes = tolist(slice_per(body.get('classes'), SawtoothConfig.MAX_BATCH_SIZE))
        transactions = []
        for i in range(len(list_transaction_id)):
            transactions.append({
                "classId": list_classes[i].get("classId"),
                "transactionId": list_transaction_id[i]
            })

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactions': transactions

            })

    def add_route(self, app):
        app.router.add_post('/staff/create-class', self.create_class)
        app.router.add_post('/staff/create-classes', self.create_classes)
