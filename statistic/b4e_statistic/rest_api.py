import asyncio
import logging
import sys
import nest_asyncio

from aiohttp import web

from aiohttp.web import json_response

from addressing.b4e_addressing import addresser

LOGGER = logging.getLogger(__name__)


class StudentAPI(object):
    def __init__(self, database, host="0.0.0.0", port=8000):
        self._database = database
        self._host = host
        self._port = port
        pass

    def run(self):
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()

        app = web.Application(loop=loop)
        # WARNING: UNSAFE KEY STORAGE
        # In a production application these keys should be passed in more securely
        app['aes_key'] = 'ffffffffffffffffffffffffffffffff'
        app['secret_key'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        LOGGER.info('Starting Student REST API on %s:%s', self._host, self._port)

        app.router.add_get('/student/data/{student_public_key}', self.student_data)
        app.router.add_get('/record/{address}', self.record_address)
        app.router.add_get('/', self.hello_student)

        web.run_app(
            app,
            host=self._host,
            port=self._port,
            access_log=LOGGER,
            access_log_format='%r: %s status, %b size, in %Tf s'
        )

    def student_data(self, request):
        public_key = request.match_info.get('student_public_key', '')
        records = self._database.get_student_data(public_key)
        # records = list(records)
        certificates = []
        subjects = []
        for record in records:
            record_id = record.get("record_id")
            owner_public_key = record.get("owner_public_key")
            manager_public_key = record.get("manager_public_key")
            address = addresser.get_record_address(record_id, owner_public_key, manager_public_key)
            record_data = {"address": address,
                           "versions": self.standard_versions(record.get("versions"))}

            if record.get("record_type") == "SUBJECT":
                subjects.append(record_data)
            elif record.get("record_type") == "CERTIFICATE":
                certificates.append(record_data)

            student_data = {
                "certificates": certificates,
                "subjects": subjects
            }
        return json_response(student_data)

    def record_address(self, request):
        address = request.match_info.get('address', '')
        try:
            record = self._database.get_record_by_address(address)
            record_data = {"address": address,
                           "versions": self.standard_versions(record.get("versions"))}
        except Exception as e:
            record_data = {"err": str(e)}

        return json_response(record_data)

    def hello_student(self, request):
        return "hello"

    def standard_versions(self, versions):
        for version in versions:
            status = version.get("record_status")
            version['type'] = self._version_status_type(status)
            del version['record_status']
            version['txid'] = version['transaction_id']
            del version["transaction_id"]

        return versions

    def _version_status_type(self, i):
        switch = {
            "CREATED": "create",
            "REVOKED": "revoke",
            "REACTIVATED": "reactive"
        }
        return switch.get(i)
