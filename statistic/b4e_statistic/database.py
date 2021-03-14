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
# -----------------------------------------------------------------------------
import json
import logging

from pymongo import MongoClient
import datetime
import time

import psycopg2
from psycopg2.extras import RealDictCursor

from addressing.b4e_addressing import addresser
from config.config import MongoDBConfig

LOGGER = logging.getLogger(__name__)

CREATE_BLOCK_STMTS = """
CREATE TABLE IF NOT EXISTS blocks (
    block_num  bigint PRIMARY KEY,
    block_id   varchar
);
"""

ACTOR_STMTS = """
CREATE TABLE IF NOT EXISTS actors (
    actor_public_key   varchar PRIMARY KEY,
    manager_public_key varchar,
    id                 varchar,
    role               varchar,
    start_block_num    bigint,
    timestamp          date,
    transaction_id     varchar 
);
"""

CLASS_STMTS = """
CREATE TABLE IF NOT EXISTS classes (
    class_id                varchar PRIMARY KEY,
    institution_public_key  varchar PRIMARY KEY,
    subject_id              varchar,
    teacher_public_key      varchar,
    credit                  tinyint,
    student_public_keys     varchar,
    start_block_num         bigint,
    timestamp               date,
    transaction_id          varchar 
);
"""

EDU_PROGRAM_STMTS = """
CREATE TABLE IF NOT EXISTS edu_programs (
    owner_public_key    varchar PRIMARY KEY,
    manager_public_key  varchar PRIMARY KEY,
    id                  varchar PRIMARY KEY,
    name                varchar,
    total_credit        int,
    min_year            tinyint,
    max_year            tinyint,
    start_block_num     bigint,
    timestamp           date,
    transaction_id      varchar 
);
"""

RECORD_STMTS = """
CREATE TABLE IF NOT EXISTS records (
    owner_public_key    varchar PRIMARY KEY,
    issuer_public_key   varchar ,
    manager_public_key  varchar PRIMARY KEY,
    record_id           varchar PRIMARY KEY,
    portfolio_id        varchar,
    record_status        varchar,
    record_type         varchar,
    start_block_num     bigint,
    timestamp           date,
    transaction_id      varchar 
);
"""


class Database(object):
    """Simple object for managing a connection to a postgres database
    """

    def __init__(self, dsn):
        self._dsn = dsn
        self._conn = None

    def connect(self, retries=5, initial_delay=1, backoff=2):
        """Initializes a connection to the database

        Args:
            retries (int): Number of times to retry the connection
            initial_delay (int): Number of seconds wait between reconnects
            backoff (int): Multiplies the delay after each retry
        """
        LOGGER.info('Connecting to database')

        delay = initial_delay
        for attempt in range(retries):
            try:
                self._conn = psycopg2.connect(self._dsn)
                LOGGER.info('Successfully connected to database')
                return

            except psycopg2.OperationalError:
                LOGGER.debug(
                    'Connection failed.'
                    ' Retrying connection (%s retries remaining)',
                    retries - attempt)
                time.sleep(delay)
                delay *= backoff

        self._conn = psycopg2.connect(self._dsn)
        LOGGER.info('Successfully connected to database')

    def create_tables(self):
        """Creates the Simple Supply tables
        """
        with self._conn.cursor() as cursor:
            LOGGER.debug('Creating table: blocks')
            cursor.execute(CREATE_BLOCK_STMTS)

            LOGGER.debug('Creating table: actors')
            cursor.execute(ACTOR_STMTS)

            LOGGER.debug('Creating table: classes')
            cursor.execute(CLASS_STMTS)

            LOGGER.debug('Creating table: portfolios')
            cursor.execute(EDU_PROGRAM_STMTS)

            LOGGER.debug('Creating table: records')
            cursor.execute(RECORD_STMTS)

        self._conn.commit()

    def disconnect(self):
        """Closes the connection to the database
        """
        LOGGER.info('Disconnecting from database')
        if self._conn is not None:
            self._conn.close()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def drop_fork(self, block_num):
        """Deletes all resources from a particular block_num
        """
        delete_actors = """
        DELETE FROM actors WHERE start_block_num >= {}
        """.format(block_num)

        delete_classes = """
                DELETE FROM classes WHERE start_block_num >= {}
                """.format(block_num)
        delete_portfolios = """
                DELETE FROM portfolios WHERE start_block_num >= {}
                """.format(block_num)
        delete_records = """
                DELETE FROM records WHERE start_block_num >= {}
                """.format(block_num)
        delete_voting = """
                DELETE FROM voting WHERE start_block_num >= {}
                """.format(block_num)

        delete_blocks = """
        DELETE FROM blocks WHERE block_num >= {}
        """.format(block_num)

        with self._conn.cursor() as cursor:
            cursor.execute(delete_actors)
            cursor.execute(delete_classes)
            cursor.execute(delete_portfolios)
            cursor.execute(delete_records)
            cursor.execute(delete_voting)
            cursor.execute(delete_blocks)

    def fetch_last_known_blocks(self, count):
        """Fetches the specified number of most recent blocks
        """
        fetch = """
        SELECT block_num, block_id FROM blocks
        ORDER BY block_num DESC LIMIT {}
        """.format(count)

        with self._conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(fetch)
            blocks = cursor.fetchall()

        return blocks

    def fetch_block(self, block_num):
        fetch = """
        SELECT block_num, block_id FROM blocks WHERE block_num = {}
        """.format(block_num)

        with self._conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(fetch)
            block = cursor.fetchone()

        return block

    def insert_block(self, block_dict):
        insert = """
        INSERT INTO blocks (
        block_num,
        block_id)
        VALUES ('{}', '{}');
        """.format(
            block_dict['block_num'],
            block_dict['block_id'])

        with self._conn.cursor() as cursor:
            cursor.execute(insert)

    def insert_actor(self, actor_dict):
        actor_dict['timestamp'] = timestamp_to_datetime(actor_dict['timestamp']).date()
        insert_ = """
                INSERT INTO agents (
                actor_public_key,
                manager_public_key,
                id,
                role,
                start_block_num,
                timestamp,
                transaction_id)
                VALUES ('{}', '{}', '{}', '{}', '{}');
                """.format(
            actor_dict['actor_public_key'],
            actor_dict['manager_public_key'],
            actor_dict['id'],
            actor_dict['role'],
            actor_dict['start_block_num'],
            actor_dict['timestamp'],
            actor_dict['transaction_id'],
        )

        with self._conn.cursor() as cursor:
            cursor.execute(insert_)

    def insert_class(self, class_dict):
        class_dict['timestamp'] = timestamp_to_datetime(class_dict['timestamp']).date()
        insert_ = """
                        INSERT INTO agents (
                        class_id,
                        institution_public_key,
                        subject_id,
                        teacher_public_key,
                        credit,
                        student_public_keys,
                        start_block_num,
                        timestamp,
                        transaction_id)
                        VALUES ('{}', '{}', '{}', '{}', '{}');
                        """.format(
            class_dict['class_id'],
            class_dict['institution_public_key'],
            class_dict['subject_id'],
            class_dict['teacher_public_key'],
            class_dict['credit'],
            class_dict['student_public_keys'],
            class_dict['start_block_num'],
            class_dict['timestamp'],
            class_dict['transaction_id'],
        )

        with self._conn.cursor() as cursor:
            cursor.execute(insert_)

    def insert_portfolio(self, portfolio_dict):
        if portfolio_dict['portfolio_data']["portfolio_type"] != "EDU_PROGRAM":
            return
        portfolio_dict['timestamp'] = timestamp_to_datetime(portfolio_dict['timestamp']).date()
        edu_program_data = json.loads(portfolio_dict["portfolio_data"][-1])

        insert_agent = """
                        INSERT INTO edu_programs (
                        owner_public_key,
                        manager_public_key,
                        id,
                        name,
                        total_credit,
                        min_year,
                        max_year,
                        start_block_num,
                        timestamp,
                        transaction_id)
                        VALUES ('{}', '{}', '{}', '{}', '{}');
                        """.format(
            portfolio_dict['owner_public_key'],
            portfolio_dict['manager_public_key'],
            portfolio_dict['id'],
            edu_program_data['name'],
            edu_program_data['totalCredit'],
            edu_program_data['minYear'],
            edu_program_data['maxYear'],
            portfolio_dict['start_block_num'],
            portfolio_dict['timestamp'],
            portfolio_dict['transaction_id'],
        )

        with self._conn.cursor() as cursor:
            cursor.execute(insert_agent)

    def insert_record(self, record_dict):
        record_dict['timestamp'] = timestamp_to_datetime(record_dict['timestamp']).date()
        insert_ = """
                        INSERT INTO records (
                        owner_public_key,
                        issuer_public_key,
                        manager_public_key,
                        record_id,
                        portfolio_id,
                        record_status,
                        record_type,
                        start_block_num,
                        timestamp,
                        transaction_id)
                        VALUES ('{}', '{}', '{}', '{}', '{}');
                        """.format(
            record_dict['owner_public_key'],
            record_dict['issuer_public_key'],
            record_dict['manager_public_key'],
            record_dict['record_id'],
            record_dict['record_type'],
            record_dict['versions'][-1]["portfolio_id"],
            record_dict['versions'][-1]["record_status"],
            record_dict['record_type'],
            record_dict['start_block_num'],
            record_dict['timestamp'],
            record_dict['transaction_id'],
        )

        with self._conn.cursor() as cursor:
            cursor.execute(insert_)

    def insert_voting(self, voting_dict):
        return

    def insert_vote(self, vote_dict):
        try:
            return
        except Exception as e:
            print(e)
            return None

    def insert_environment(self, environment_dict):
        try:
            return
        except Exception as e:
            print(e)
            return None

    def get_student_data(self, public_key):
        return ""

    def get_record_by_address(self, address):
        return ""


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def to_time_stamp(date_time):
    return datetime.datetime.timestamp(date_time)
