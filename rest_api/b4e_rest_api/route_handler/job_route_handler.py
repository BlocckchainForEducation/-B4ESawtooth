import logging

from aiohttp.web import json_response

from config.config import SawtoothConfig
from rest_api.b4e_rest_api.route_handler.route_handler import decode_request, validate_fields, tolist, slice_per, \
    get_time

LOGGER = logging.getLogger(__name__)


class JobRouteHandler(object):
    def __init__(self, loop, messenger, database):
        self._messenger = messenger
        self._database = database

    async def create_job(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'payload']
        validate_fields(required_fields, body)

        required_fields = ['companyPublicKeyHex', 'candidatePublicKeyHex', 'jobId', 'start']
        payload = body.get('payload')
        validate_fields(required_fields, payload)

        required_fields = ['cipher', 'hash']
        start = payload.get('start')
        validate_fields(required_fields, start)

        transaction_id = await self._messenger.send_create_job(private_key=body.get('privateKeyHex'),
                                                               company_public_key=payload.get('companyPublicKeyHex'),
                                                               candidate_public_key=payload.get(
                                                                   'candidatePublicKeyHex'),
                                                               job_id=payload.get('jobId'),
                                                               cipher=start.get('cipher'),
                                                               record_hash=start.get('hash'),
                                                               timestamp=get_time())

        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactionId': transaction_id
            })

    async def update_job_end(self, request):
        body = await decode_request(request)
        required_fields = ['privateKeyHex', 'payload']
        validate_fields(required_fields, body)

        required_fields = ['companyPublicKeyHex', 'candidatePublicKeyHex', 'jobId']
        payload = body.get('payload')
        validate_fields(required_fields, payload)

        transaction_id = await self._messenger.send_update_job_end(private_key=body.get('privateKeyHex'),
                                                                   company_public_key=payload.get(
                                                                       'companyPublicKeyHex'),
                                                                   candidate_public_key=payload.get(
                                                                       'candidatePublicKeyHex'),
                                                                   job_id=payload.get('jobId'),
                                                                   timestamp=get_time())
        return json_response(
            {
                'ok': True,
                'msg': 'Transfer record transaction submitted',
                'transactionId': transaction_id
            })

    def add_route(self, app):
        app.router.add_post('/company/job-begin', self.create_job)
        app.router.add_post('/company/job-end', self.update_job_end)
