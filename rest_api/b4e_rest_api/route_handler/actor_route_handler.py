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


class ActorRouteHandler(object):
    def __init__(self, loop, messenger, database):
        self._messenger = messenger
        self._database = database

    async def create_institution(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'profile']
        validate_fields(required_fields, body)

        profile = body.get('profile')
        required_fields = ['email', 'universityName']
        validate_fields(required_fields, profile)
        transaction_id = await self._messenger.send_create_institution(private_key=body.get('privateKeyHex'),
                                                                       profile=body.get('profile'),
                                                                       timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactionId': transaction_id
            })

    async def create_teacher(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'profile']
        validate_fields(required_fields, body)

        profile = body.get('profile')
        required_fields = ['teacherId', 'publicKey']
        validate_fields(required_fields, profile)

        transaction_id = await self._messenger.send_create_teacher(private_key=body.get('privateKeyHex'),
                                                                   profile=profile,
                                                                   timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactionId': transaction_id
            })

    async def create_teachers(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'profiles']
        validate_fields(required_fields, body)
        profiles = body.get('profiles')
        required_fields = ['teacherId', 'publicKey']
        for profile in profiles:
            validate_fields(required_fields, profile)

        list_transaction_id = await self._messenger.send_create_teachers(private_key=body.get('privateKeyHex'),
                                                                         profiles=profiles,
                                                                         timestamp=get_time())
        list_teachers = tolist(slice_per(profiles, SawtoothConfig.MAX_BATCH_SIZE))
        transactions = []
        for i in range(len(list_transaction_id)):
            transactions.append({
                "teacherId": list_teachers[i].get("teacherId"),
                "transactionId": list_transaction_id[i]
            })

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactions': transactions

            })

    def add_route(self, app):
        app.router.add_post('/staff/register', self.create_institution)
        app.router.add_post('/staff/create-teacher', self.create_teacher)
        app.router.add_post('/staff/create-teachers', self.create_teachers)
