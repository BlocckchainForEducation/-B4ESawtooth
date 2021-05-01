import logging

LOGGER = logging.getLogger(__name__)


class BlockchainRouteHandler(object):
    def __init__(self, loop, messenger, database):
        self._messenger = messenger
        self._database = database

    async def get_student_data(self, request):
        pass

    async def get_record(self, request):
        pass

    def add_route(self, app):
        pass
