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

import argparse
import asyncio
import logging
import sys
import nest_asyncio

from zmq.asyncio import ZMQEventLoop

from sawtooth_sdk.processor.log import init_console_logging

from aiohttp import web

from rest_api.b4e_rest_api.route_handler import RouteHandler
from rest_api.b4e_rest_api.database import Database
from rest_api.b4e_rest_api.messaging import Messenger

from config.config import Sawtooth_Config, MongoDBConfig

LOGGER = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Starts the Simple Supply REST API')

    parser.add_argument(
        '-B', '--bind',
        help='identify host and port for api to run on',
        default='localhost:8000')
    parser.add_argument(
        '-C', '--connect',
        help='specify URL to connect to a running validator',
        default='tcp://localhost:4004')
    parser.add_argument(
        '-R', '--restapi',
        help='specify URL to connect to a running validator',
        default='http://localhost:8008')
    parser.add_argument(
        '-t', '--timeout',
        help='set time (in seconds) to wait for a validator response',
        default=500)
    parser.add_argument(
        '--db-name',
        help='The name of the database',
        default='simple-supply')
    parser.add_argument(
        '--db-host',
        help='The host of the database',
        default='localhost')
    parser.add_argument(
        '--db-port',
        help='The port of the database',
        default='27017')
    parser.add_argument(
        '--db-user',
        help='The authorized user of the database',
        default='')
    parser.add_argument(
        '--db-password',
        help="The authorized user's password for database access",
        default='')
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='enable more verbose output to stderr')

    return parser.parse_args(args)


def start_rest_api(host, port, messenger, database):
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(database.connect())

    app = web.Application(loop=loop)
    # WARNING: UNSAFE KEY STORAGE
    # In a production application these keys should be passed in more securely
    app['aes_key'] = 'ffffffffffffffffffffffffffffffff'
    app['secret_key'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    messenger.open_validator_connection()
    messenger.open_db_collection()

    handler = RouteHandler(loop, messenger, database)

    app.router.add_post('/set_b43_environment', handler.set_b4e_environment)
    app.router.add_post('/create_institution', handler.create_institution)
    app.router.add_post('/create_teacher', handler.create_teacher)
    app.router.add_post('/create_teachers', handler.create_teachers)
    app.router.add_post('/create_edu_officer', handler.create_edu_officer)
    app.router.add_post('/create_edu_officers', handler.create_edu_officers)
    app.router.add_post('/create_vote', handler.create_vote)
    app.router.add_post('/create_class', handler.create_class)
    app.router.add_post('/create_classes', handler.create_classes)
    app.router.add_post('/create_subject', handler.create_subject)
    app.router.add_post('/create_subjects', handler.create_subjects)
    app.router.add_post('/create_cert', handler.create_cert)
    app.router.add_post('/create_certs', handler.create_certs)
    app.router.add_post('/update_record', handler.update_record)
    app.router.add_post('/update_actor_info', handler.update_actor_info)

    app.router.add_post('/get_new_key_pair', handler.get_new_key_pair)
    app.router.add_get('/transaction/{transaction_id}', handler.fetch_data_transaction)
    app.router.add_get('/record/{transaction_id}', handler.fetch_record_transaction)
    app.router.add_get('/state/{data_address}', handler.fetch_data_state)
    app.router.add_get('/student_data/{student_public_key}', handler.fetch_data_student)

    app.router.add_post('/test_time_submit_transaction', handler.test_time_create_transaction)

    LOGGER.info('Starting Simple Supply REST API on %s:%s', host, port)
    web.run_app(
        app,
        host=host,
        port=port,
        access_log=LOGGER,
        access_log_format='%r: %s status, %b size, in %Tf s')


def main():
    loop = ZMQEventLoop()
    asyncio.set_event_loop(loop)

    try:
        opts = parse_args(sys.argv[1:])

        init_console_logging(verbose_level=opts.verbose)

        validator_url = opts.connect
        if "tcp://" not in validator_url:
            validator_url = "tcp://" + validator_url

        restapi = opts.restapi
        if "http://" not in restapi:
            restapi = "http://" + restapi

        Sawtooth_Config.REST_API = restapi

        messenger = Messenger(validator_url)

        MongoDBConfig.USER_NAME = opts.db_user
        MongoDBConfig.PASSWORD = opts.db_password
        MongoDBConfig.HOST = opts.db_host
        MongoDBConfig.PORT = opts.db_port

        database = Database(
            opts.db_host,
            opts.db_port,
            opts.db_name,
            opts.db_user,
            opts.db_password,
            loop)
        try:
            host, port = opts.bind.split(":")
            port = int(port)
        except ValueError:
            print("Unable to parse binding {}: Must be in the format"
                  " host:port".format(opts.bind))
            sys.exit(1)

        start_rest_api(host, port, messenger, database)
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception(err)
        sys.exit(1)
    finally:
        database.disconnect()
        messenger.close_validator_connection()


if __name__ == '__main__':
    loop = ZMQEventLoop()
    asyncio.set_event_loop(loop)

    try:
        opts = parse_args(sys.argv[1:])

        init_console_logging(verbose_level=opts.verbose)

        validator_url = 'tcp://0.0.0.0:4004'
        messenger = Messenger(validator_url)

        database = Database(
            opts.db_host,
            opts.db_port,
            opts.db_name,
            opts.db_user,
            opts.db_password,
            loop)

        try:
            host, port = opts.bind.split(":")
            port = int(port)
        except ValueError:
            print("Unable to parse binding {}: Must be in the format"
                  " host:port".format(opts.bind))
            sys.exit(1)

        start_rest_api(host, port, messenger, database)
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception(err)
        sys.exit(1)
    finally:
        database.disconnect()
        messenger.close_validator_connection()
