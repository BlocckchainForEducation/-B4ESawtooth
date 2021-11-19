import logging

from aiohttp.web import json_response

from config.config import SawtoothConfig
from rest_api.b4e_rest_api.route_handler.route_handler import decode_request, validate_fields, tolist, slice_per, \
    get_time

LOGGER = logging.getLogger(__name__)


class RecordRouteHandler(object):
    def __init__(self, loop, messenger, database):
        self._messenger = messenger
        self._database = database

    async def create_record(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'ownerPublicKey', 'managerPublicKey', 'id', 'programId', 'cipher', 'hash']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_create_subject(private_key=body.get('privateKeyHex'),
                                                                   owner_public_key=body.get('ownerPublicKey'),
                                                                   manager_public_key=body.get('managerPublicKey'),
                                                                   record_id=body.get('classId'),
                                                                   portfolio_id=body.get('programId'),
                                                                   cipher=body.get('cipher'),
                                                                   record_hash=body.get('hash'),
                                                                   timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Create record transaction submitted',
                'transactionId': transaction_id
            })

    async def create_subject(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'classId', 'grades', 'studentPublicKey', 'eduProgramId', 'cipher', 'hash']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_create_subject(private_key=body.get('privateKeyHex'),
                                                                   owner_public_key=body.get('studentPublicKey'),
                                                                   manager_public_key=body.get('universityPublicKey'),
                                                                   record_id=body.get('classId'),
                                                                   portfolio_id=body.get('eduProgramId'),
                                                                   cipher=body.get('cipher'),
                                                                   record_hash=body.get('hashData'),
                                                                   timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Create record transaction submitted',
                'transactionId': transaction_id
            })

    async def create_subjects(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'universityPublicKey', 'classId', 'grades']
        validate_fields(required_fields, body)

        required_fields = ['studentPublicKey', 'eduProgramId', 'cipher', 'hash']
        grades = body.get('grades')
        for grade in grades:
            validate_fields(required_fields, grade)

        list_transaction_id = await self._messenger.send_create_subjects(private_key=body.get('privateKeyHex'),
                                                                         manager_public_key=body.get(
                                                                             'universityPublicKey'),
                                                                         class_id=body.get('classId'),
                                                                         list_subjects=body.get('grades'),
                                                                         timestamp=get_time())

        list_subjects = tolist(slice_per(body.get('grades'), SawtoothConfig.MAX_BATCH_SIZE))
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
                'msg': 'Create records transaction submitted',
                'transactions': transactions

            })

    async def create_cert(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'eduProgramId', 'studentPublicKey', 'cipher', 'hashData']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_create_cert(private_key=body.get('privateKeyHex'),
                                                                owner_public_key=body.get('studentPublicKey'),
                                                                record_id=body.get('eduProgramId'),
                                                                portfolio_id=body.get('eduProgramId'),
                                                                record_data=body.get('cipher'),
                                                                record_hash=body.get('hashData'),
                                                                timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Create record transaction submitted',
                'transactionId': transaction_id
            })

    async def create_certs(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'certificates']
        validate_fields(required_fields, body)
        required_fields = ['school', 'eduProgramId', 'studentPublicKey', 'cipher', 'hash']
        certs = body.get('certificates')
        for cert in certs:
            validate_fields(required_fields, cert)

        list_transaction_id = await self._messenger.send_create_certs(private_key=body.get('privateKeyHex'),
                                                                      certs=certs,
                                                                      timestamp=get_time())

        list_certs = tolist(slice_per(body.get('certificates'), SawtoothConfig.MAX_BATCH_SIZE))
        transactions = []
        for i in range(len(list_transaction_id)):
            transactions.append({
                "eduProgramId": list_certs[i].get("eduProgramId"),
                "studentPublicKey": list_certs[i].get("studentPublicKey"),
                "transactionId": list_transaction_id[i]
            })

        return json_response(
            {
                'ok': True,
                'msg': 'Create record transaction submitted',
                'transactions': transactions

            })

    async def update_record(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'OwnerPublicKey', 'recordId', 'cipher', 'hash', 'status',
                           'manager_public_key']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_update_record(private_key=body.get('privateKeyHex'),
                                                                  owner_public_key=body.get('OwnerPublicKey'),
                                                                  record_id=body.get('recordId'),
                                                                  cipher=body.get('cipher'),
                                                                  record_hash=body.get('hash'),
                                                                  status=body.get('status'),
                                                                  timestamp=get_time())
        return json_response(
            {
                'ok': True,
                'msg': 'Edit record transaction submitted',
                'transactionId': transaction_id
            })

    async def modify_subject(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'studentPublicKey', 'universityPublicKey', 'classId', 'cipher', 'hash']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_modify_subject(private_key=body.get('privateKeyHex'),
                                                                   owner_public_key=body.get('studentPublicKey'),
                                                                   manager_public_key=body.get('universityPublicKey'),
                                                                   record_id=body.get('classId'),
                                                                   cipher=body.get('cipher'),
                                                                   record_hash=body.get('hash'),
                                                                   timestamp=get_time())
        return json_response(
            {
                'ok': True,
                'msg': 'Edit record transaction submitted',
                'transactionId': transaction_id
            })

    async def modify_cert(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'studentPublicKey', 'eduProgramId', 'cipher', 'hash']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_modify_cert(private_key=body.get('privateKeyHex'),
                                                                owner_public_key=body.get('studentPublicKey'),
                                                                record_id=body.get('eduProgramId'),
                                                                cipher=body.get('cipher'),
                                                                record_hash=body.get('hash'),
                                                                timestamp=get_time())
        return json_response(
            {
                'ok': True,
                'msg': 'Edit record transaction submitted',
                'transactionId': transaction_id
            })

    async def revoke_cert(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'studentPublicKey', 'eduProgramId']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_revoke_cert(private_key=body.get('privateKeyHex'),
                                                                owner_public_key=body.get('studentPublicKey'),
                                                                record_id=body.get('eduProgramId'),
                                                                timestamp=get_time())
        return json_response(
            {
                'ok': True,
                'msg': 'Revoke cert transaction submitted',
                'transactionId': transaction_id
            })

    async def reactive_cert(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'studentPublicKey', 'eduProgramId']
        validate_fields(required_fields, body)

        transaction_id = await self._messenger.send_reactive_cert(private_key=body.get('privateKeyHex'),
                                                                  owner_public_key=body.get('studentPublicKey'),
                                                                  record_id=body.get('eduProgramId'),
                                                                  timestamp=get_time())
        return json_response(
            {
                'ok': True,
                'msg': 'Reactive cert transaction submitted',
                'transactionId': transaction_id
            })

    def add_route(self, app):
        app.router.add_post('/create-record', self.create_record)
        app.router.add_post('/staff/create-subject', self.create_subject)
        app.router.add_post('/teacher/submit-grade', self.create_subjects)
        app.router.add_post('/staff/create-certificate', self.create_cert)
        app.router.add_post('/staff/create-certificates', self.create_certs)
        app.router.add_post('/staff/update-record', self.update_record)
        app.router.add_post('/teacher/edit-grade', self.modify_subject)
        app.router.add_post('/staff/modify-certificate', self.modify_cert)
        app.router.add_post('/staff/revoke-certificate', self.revoke_cert)
        app.router.add_post('/staff/reactive-certificate', self.reactive_cert)
