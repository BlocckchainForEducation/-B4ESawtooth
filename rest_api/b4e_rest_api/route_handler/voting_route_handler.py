import logging

from aiohttp.web import json_response
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
