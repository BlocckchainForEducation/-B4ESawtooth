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


class StudentRouteHandler(object):
    def __init__(self, loop, messenger, database):
        self._messenger = messenger
        self._database = database

    async def create_student(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'publicKey', 'eduProgram']
        validate_fields(required_fields, body)

        required_fields = ['eduProgramId', 'name', 'totalCredit', 'minYear', 'maxYear']
        validate_fields(required_fields, body.get('eduProgram'))
        transaction_id = await self._messenger.send_create_edu_program(private_key=body.get('privateKeyHex'),
                                                                       student_public_key=body.get('publicKey'),
                                                                       edu_program=body.get('eduProgram'),
                                                                       timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactionId': transaction_id
            })

    async def create_students(self, request):
        body = await decode_request(request)

        required_fields = ['privateKeyHex', 'profiles']
        validate_fields(required_fields, body)
        pre_required_fields = ['publicKey', 'eduProgram']
        required_fields = ['eduProgramId', 'name', 'totalCredit', 'minYear', 'maxYear']
        for profile in body.get('profiles'):
            validate_fields(pre_required_fields, profile)
            validate_fields(required_fields, profile.get('eduProgram'))

        list_transaction_id = await self._messenger.send_create_edu_programs(private_key=body.get('privateKeyHex'),
                                                                             profiles=body.get('profiles'),
                                                                             timestamp=get_time())

        list_classes = tolist(slice_per(body.get('profiles'), SawtoothConfig.MAX_BATCH_SIZE))
        transactions = []
        for i in range(len(list_transaction_id)):
            transactions.append({
                "publicKey": list_classes[i].get("publicKey"),
                "eduProgramId": list_classes[i].get("eduProgram").get("eduProgramId"),
                "transactionId": list_transaction_id[i]
            })

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactions': transactions

            })

    def add_route(self, app):
        app.router.add_post('/staff/create-student', self.create_student)
        app.router.add_post('/staff/create-students', self.create_students)
