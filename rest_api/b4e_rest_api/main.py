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

import aiohttp_cors
import nest_asyncio

from zmq.asyncio import ZMQEventLoop

from sawtooth_sdk.processor.log import init_console_logging

from aiohttp import web

from rest_api.b4e_rest_api.route_handler.job_route_handler import JobRouteHandler
from rest_api.b4e_rest_api.route_handler.route_handler import RouteHandler
from rest_api.b4e_rest_api.route_handler.actor_route_handler import ActorRouteHandler
from rest_api.b4e_rest_api.route_handler.blockchain_route_handler import BlockchainRouteHandler
from rest_api.b4e_rest_api.route_handler.class_route_handler import ClassRouteHandler
from rest_api.b4e_rest_api.route_handler.record_route_handler import RecordRouteHandler
from rest_api.b4e_rest_api.route_handler.student_route_handler import StudentRouteHandler
from rest_api.b4e_rest_api.route_handler.voting_route_handler import VotingRouteHandler
from rest_api.b4e_rest_api.database import Database
from rest_api.b4e_rest_api.messaging import Messenger

from config.config import SawtoothConfig, MongoDBConfig

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
    actor_handler = ActorRouteHandler(loop, messenger, database)
    blockchain_handler = BlockchainRouteHandler(loop, messenger, database)
    class_handler = ClassRouteHandler(loop, messenger, database)
    record_handler = RecordRouteHandler(loop, messenger, database)
    student_handler = StudentRouteHandler(loop, messenger, database)
    voting_handler = VotingRouteHandler(loop, messenger, database)
    job_handler = JobRouteHandler(loop, messenger, database)

    handler.add_route(app)
    actor_handler.add_route(app)
    blockchain_handler.add_route(app)
    class_handler.add_route(app)
    record_handler.add_route(app)
    student_handler.add_route(app)
    voting_handler.add_route(app)
    job_handler.add_route(app)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    LOGGER.info('Starting B4E REST API on %s:%s', host, port)
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

        SawtoothConfig.REST_API = restapi

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
