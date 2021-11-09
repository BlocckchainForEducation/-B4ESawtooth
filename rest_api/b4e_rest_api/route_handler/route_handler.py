# Copyright 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
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

LOGGER = logging.getLogger(__name__)


def slice_per(source, step):
    if len(source) < step:
        return [source]
    return [source[i::step] for i in range(step)]


def tolist(source):
    list_temp = []
    for list_ in source:
        for element in list_:
            list_temp.append(element)
    return list_temp


class RouteHandler(object):
    def __init__(self, loop, messenger, database):

        self._messenger = messenger
        self._database = database

    async def get_new_key_pair(self, request):
        public_key, private_key = self._messenger.get_new_key_pair()
        return json_response(
            {
                'publicKey': public_key,
                'privateKey': private_key
            })

    async def set_b4e_environment(self, request):
        await self._messenger.send_set_b4e_environment(get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Set environment submitted'
            })

    async def create_institution(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'profile']
        validate_fields(required_fields, body)

        profile = body.get('profile')
        try:
            profile['uid']
        except Exception as e:
            return json_response({'err': 'profile must have uid field'})
        transaction_id = await self._messenger.send_create_institution(private_key=body.get('privateKeyHex'),
                                                                       profile=body.get('profile'),
                                                                       timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Create institution transaction submitted',
                'transactionId': transaction_id
            })

    async def create_teacher(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'profile']
        validate_fields(required_fields, body)
        try:
            profile = body.get('profile')
            profile['teacherId']
            profile['publicKey']
        except Exception as e:
            return json_response({'err': 'profile must have teacherId field'})

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
                'msg': 'Create record transaction submitted',
                'transactions': transactions

            })

    async def create_edu_officer(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'profile']
        validate_fields(required_fields, body)

        try:
            profile = body.get('profile')
            profile['bureauId']
            profile['publicKey']
        except Exception as e:
            return json_response({'err': 'profile must have bureauId field'})

        transaction_id = await self._messenger.send_create_edu_officer(private_key=body.get('privateKeyHex'),
                                                                       profile=profile,
                                                                       timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Create transaction submitted',
                'transactionId': transaction_id
            })

    async def create_edu_officers(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'profiles']
        validate_fields(required_fields, body)
        profiles = body.get('profiles')

        list_transaction_id = await self._messenger.send_create_edu_officers(private_key=body.get('privateKeyHex'),
                                                                             profiles=profiles,
                                                                             timestamp=get_time())

        list_edu_officers = tolist(slice_per(profiles, SawtoothConfig.MAX_BATCH_SIZE))
        transactions = []
        for i in range(len(list_transaction_id)):
            transactions.append({
                "bureauId": list_edu_officers[i].get("bureauId"),
                "transactionId": list_transaction_id[i]
            })

        return json_response(
            {
                'ok': True,
                'msg': 'Create transaction submitted',
                'transactions': transactions

            })

    async def create_vote(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'publicKeyOfRequest', 'decision']
        validate_fields(required_fields, body)

        if body.get('decision') == "accept":
            accepted = True
        elif body.get('decision') == "decline":
            accepted = False

        transaction_id = await self._messenger.send_create_vote(private_key=body.get('privateKeyHex'),
                                                                elector_public_key=body.get('publicKeyOfRequest'),
                                                                decision=accepted,
                                                                timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Create vote transaction submitted',
                'transactionId': transaction_id
            })

    async def create_class(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'classId', 'teacherPublicKey', 'bureauPublicKey']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_create_class(private_key=body.get('privateKeyHex'),
                                                                 teacher_public_key=body.get('teacherPublicKey'),
                                                                 edu_officer_public_key=body.get('bureauPublicKey'),
                                                                 class_id=body.get('classId'),
                                                                 timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Create class transaction submitted',
                'transactionId': transaction_id
            })

    async def create_classes(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'classes']
        validate_fields(required_fields, body)

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
                'msg': 'Create classes transaction submitted',
                'transactions': transactions

            })

    async def create_subject(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'universityPublicKey', 'classId', 'studentPublicKey', 'cipher', 'hashData']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_create_subject(private_key=body.get('privateKeyHex'),
                                                                   owner_public_key=body.get('studentPublicKey'),
                                                                   manager_public_key=body.get('universityPublicKey'),
                                                                   record_id=body.get('classId'),
                                                                   record_data=body.get('cipher'),
                                                                   record_hash=body.get('hashData'),
                                                                   timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Create Subject transaction submitted',
                'transactionId': transaction_id
            })

    async def create_subjects(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'universityPublicKey', 'classId', 'points']
        validate_fields(required_fields, body)

        list_transaction_id = await self._messenger.send_create_subjects(private_key=body.get('privateKeyHex'),
                                                                         institution_public_key=body.get(
                                                                             'universityPublicKey'),
                                                                         class_id=body.get('classId'),
                                                                         list_subjects=body.get('points'),
                                                                         timestamp=get_time())

        list_subjects = tolist(slice_per(body.get('points'), SawtoothConfig.MAX_BATCH_SIZE))
        transactions = []
        class_id = body.get('classId')
        for i in range(len(list_transaction_id)):
            transactions.append({
                "classId": class_id,
                "studentPublicKey": list_subjects[i].get("studentPublicKey"),
                "transactionId": list_transaction_id[i]
            })

        return json_response(
            {
                'ok': True,
                'msg': 'Create subjects transaction submitted',
                'transactions': transactions

            })

    async def create_cert(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'globalregisno', 'studentPublicKey', 'cipher', 'hashData']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_create_cert(private_key=body.get('privateKeyHex'),
                                                                owner_public_key=body.get('studentPublicKey'),
                                                                record_id=body.get('globalregisno'),
                                                                record_data=body.get('cipher'),
                                                                record_hash=body.get('hashData'),
                                                                timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Create certificate transaction submitted',
                'transactionId': transaction_id
            })

    async def create_certs(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'certificates']
        validate_fields(required_fields, body)

        list_transaction_id = await self._messenger.send_create_certs(private_key=body.get('privateKeyHex'),
                                                                      certs=body.get('certificates'),
                                                                      timestamp=get_time())

        list_certs = tolist(slice_per(body.get('certificates'), SawtoothConfig.MAX_BATCH_SIZE))
        transactions = []
        for i in range(len(list_transaction_id)):
            transactions.append({
                "globalregisno": list_certs[i].get("globalregisno"),
                "studentPublicKey": list_certs[i].get("studentPublicKey"),
                "transactionId": list_transaction_id[i]
            })

        return json_response(
            {
                'ok': True,
                'msg': 'Create certificates transaction submitted',
                'transactions': transactions

            })

    async def update_record(self, request):
        body = await decode_request(request)
        required_fields = ['private_key', 'record_id', 'record_data', 'record_hash', 'active', 'owner_public_key',
                           'manager_public_key']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_update_record(private_key=body.get('private_key'),
                                                                  owner_public_key=body.get('owner_public_key'),
                                                                  manager_public_key=body.get('manager_public_key'),
                                                                  record_id=body.get('record_id'),
                                                                  record_data=body.get('record_data'),
                                                                  record_hash=body.get('record_hash'),
                                                                  active=body.get('active'),
                                                                  timestamp=get_time())
        return json_response(
            {
                'ok': True,
                'msg': 'Update record transaction submitted',
                'transactionId': transaction_id
            })

    async def update_actor_info(self, request):
        body = await decode_request(request)
        required_fields = ['private_key', 'name', 'phone', 'email', 'address']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_update_actor_info(private_key=body.get('private_key'),
                                                                      name=body.get('name'),
                                                                      phone=body.get('phone'),
                                                                      email=body.get('email'),
                                                                      address=body.get('address'),
                                                                      timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Update actor transaction submitted',
                'transactionId': transaction_id
            })

    async def reject_institution(self, request):
        body = await decode_request(request)
        required_fields = ['private_key', 'institution_public_key']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_reject_institution(private_key=body.get('private_key'),
                                                                       institution_public_key=body.get(
                                                                           'institution_public_key'),
                                                                       timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Reject institution transaction submitted',
                'transactionId': transaction_id
            })

    async def test_time_create_transaction(self, request):
        body = await decode_request(request)
        required_fields = ['numberTransaction', 'maxBatchSize']
        validate_fields(required_fields, body)

        num_transactions = body.get('numberTransaction')
        max_batch_size = body.get('maxBatchSize')
        commit_time = await self._messenger.send_test_time_create_transaction(num_transactions, max_batch_size)

        return json_response(
            {
                'ok': True,
                'numberTransaction': num_transactions,
                "max_batch_size": max_batch_size,
                'commitTime': commit_time
            })

    async def fetch_data_transaction(self, request):
        transaction_id = request.match_info.get('transaction_id', '')
        # transaction_id = request.rel_url.query['transaction_id']  # to get data from prams in get request
        data = get_data_from_transaction(transaction_id)

        return json_response(data)

    async def fetch_record_transaction(self, request):
        transaction_id = request.match_info.get('transaction_id', '')

        data = get_record_transaction(transaction_id)

        return json_response(data)

    async def fetch_data_state(self, request):
        data_address = request.match_info.get('data_address', '')

        data = get_state(data_address)

        return json_response(data)

    async def fetch_data_student(self, request):
        student_public_key = request.match_info.get('student_public_key', '')

        data = get_student_data(student_public_key)

        return json_response(data)

    async def up_to_ipfs(self, request):
        cid = ""
        return json_response({"cid": cid})

    def add_route(self, app):
        app.router.add_post('/set-b4e-environment', self.set_b4e_environment)

        app.router.add_post('/get_new_key_pair', self.get_new_key_pair)
        app.router.add_get('/transaction/{transaction_id}', self.fetch_data_transaction)
        app.router.add_get('/record/{transaction_id}', self.fetch_record_transaction)
        app.router.add_get('/state/{data_address}', self.fetch_data_state)
        app.router.add_get('/student/data/{student_public_key}', self.fetch_data_student)

        app.router.add_post('/test_time_submit_transaction', self.test_time_create_transaction)


async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise ApiBadRequest('Improper JSON format')


def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            raise ApiBadRequest(
                "'{}' parameter is required".format(field))


def encrypt_private_key(aes_key, public_key, private_key):
    init_vector = bytes.fromhex(public_key[:32])
    cipher = AES.new(bytes.fromhex(aes_key), AES.MODE_CBC, init_vector)
    return cipher.encrypt(private_key)


def decrypt_private_key(aes_key, public_key, encrypted_private_key):
    init_vector = bytes.fromhex(public_key[:32])
    cipher = AES.new(bytes.fromhex(aes_key), AES.MODE_CBC, init_vector)
    private_key = cipher.decrypt(bytes.fromhex(encrypted_private_key))
    return private_key


def hash_password(password):
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())


def get_time():
    dts = datetime.datetime.utcnow()
    return round(time.mktime(dts.timetuple()) + dts.microsecond / 1e6)


def generate_auth_token(secret_key, public_key):
    serializer = Serializer(secret_key)
    token = serializer.dumps({'public_key': public_key})
    return token.decode('ascii')


def deserialize_auth_token(secret_key, token):
    serializer = Serializer(secret_key)
    return serializer.loads(token)
