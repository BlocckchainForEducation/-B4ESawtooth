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


class VotingRouteHandler(object):
    def __init__(self, loop, messenger, database):
        self._messenger = messenger
        self._database = database

    async def create_vote(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'requesterPublicKey', 'decision']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_create_vote(private_key=body.get('privateKeyHex'),
                                                                elector_public_key=body.get('requesterPublicKey'),
                                                                decision=body.get('decision'),
                                                                timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactionId': transaction_id
            })

    async def create_voting(self, request):
        body = await decode_request(request)

        required_fields = ['privateKeyHex', 'electorPublicKey', 'votingType']
        validate_fields(required_fields, body)
        transaction_id = await self._messenger.send_create_voting(private_key=body.get('privateKeyHex'),
                                                                  elector_public_key=body.get('requesterPublicKey'),
                                                                  vote_type=body.get('votingType'),
                                                                  timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactionId': transaction_id
            })

    def add_route(self, app):
        app.router.add_post('/vote', self.create_vote)
        app.router.add_post('/create-voting', self.create_voting)
