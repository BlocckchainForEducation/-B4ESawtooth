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

import logging

import google
from pymongo import MongoClient
import datetime
import time
from config.config import MongoDBConfig

LOGGER = logging.getLogger(__name__)


class Database(object):
    """Simple object for managing a connection to a postgres database
    """

    def __init__(self):
        self.mongo = None
        self.b4e_db = None
        self.b4e_block_collection = None
        self.b4e_actor_collection = None
        self.b4e_portfolio_collection = None
        self.b4e_record_collection = None
        self.b4e_class_collection = None
        self.b4e_voting_collection = None

    def connect(self, host=MongoDBConfig.HOST, port=MongoDBConfig.PORT, user_name=MongoDBConfig.USER_NAME,
                password=MongoDBConfig.PASSWORD):
        if (user_name != "" and password != ""):
            url = f"mongodb://{user_name}:{password}@{host}:{port}"
            self.mongo = MongoClient(url)
        else:
            self.mongo = MongoClient(host=host, port=int(port))
        self.create_collections()

    def create_collections(self):
        self.b4e_db = self.mongo[MongoDBConfig.DATABASE]
        self.b4e_block_collection = self.b4e_db[MongoDBConfig.BLOCK_COLLECTION]
        self.b4e_actor_collection = self.b4e_db[MongoDBConfig.ACTOR_COLLECTION]
        self.b4e_class_collection = self.b4e_db[MongoDBConfig.CLASS_COLLECTION]
        self.b4e_portfolio_collection = self.b4e_db[MongoDBConfig.PORTFOLIO_COLLECTION]
        self.b4e_record_collection = self.b4e_db[MongoDBConfig.RECORD_COLLECTION]
        self.b4e_voting_collection = self.b4e_db[MongoDBConfig.VOTING_COLLECTION]

    def disconnect(self):
        self.mongo.close()

    def commit(self):
        pass

    def rollback(self):
        pass

    def drop_fork(self, block_num):
        """Deletes all resources from a particular block_num
                """
        delete = {"block_num": {"$gte": block_num}}

        try:
            self.b4e_block_collection.delete_many(delete)
            self.b4e_actor_collection.delte_many(delete)
            self.b4e_class_collection.delte_many(delete)
            self.b4e_portfolio_collection.delte_many(delete)
            self.b4e_record_collection.delte_many(delete)
            self.b4e_voting_collection.delte_many(delete)

        except Exception as e:
            print(e)

    def fetch_last_known_blocks(self, count):
        try:
            blocks = list(self.b4e_block_collection.find().sort("block_num", -1))
            return blocks[:count]
            # if not found res will not contain ['hits']['hits'][0]['_source']
        except IndexError:
            print("not found block")
            return None

    def fetch_block(self, block_num):
        if not block_num:
            return None

        query = {"block_num": block_num}
        try:
            block = self.b4e_block_collection.find_one(query)
            return block
        except Exception as e:
            print(e)
            return None

    def insert_block(self, block_dict):
        try:

            key = {'block_num': block_dict['block_num']}
            data = {"$set": block_dict}

            res = self.b4e_block_collection.update_one(key, data, upsert=True)
            return res
        except Exception as e:
            print(e)
            return None

    def insert_actor(self, actor_dict):
        try:
            key = {'actor_public_key': actor_dict['actor_public_key']}

            actor_profile = actor_dict['profile'][-1]
            actor_profile['block_num'] = actor_dict['block_num']
            old_actor = self.b4e_actor_collection.find_one(key)
            if old_actor:
                old_actor.get("profile").extend([actor_profile])
                actor_dict = old_actor
            data = {"$set": actor_dict}
            res = self.b4e_actor_collection.update_one(key, data, upsert=True)
            return res
        except Exception as e:
            LOGGER.error(e)
            print(e)
            return None

    def insert_record(self, record_dict):
        try:
            key = {'owner_public_key': record_dict['owner_public_key'],
                   'manager_public_key': record_dict['manager_public_key'],
                   'record_id': record_dict['record_id']}

            new_version = record_dict['versions'][-1]
            new_version['block_num'] = record_dict['block_num']
            old_record = self.b4e_record_collection.find_one(key)
            if old_record:
                old_record.get("versions").extend([new_version])
                record_dict = old_record
            data = {"$set": record_dict}
            res = self.b4e_record_collection.update_one(key, data, upsert=True)
            return
        except Exception as e:
            print(e)
            return None

    def insert_voting(self, voting_dict):
        try:
            key = {'elector_public_key': voting_dict['elector_public_key']}
            LOGGER.info("voting_dict")
            LOGGER.info(voting_dict)
            vote = voting_dict['vote'][-1]
            vote['block_num'] = voting_dict['block_num']
            old_voting = self.b4e_actor_collection.find_one(key)
            if old_voting:
                old_voting.get("vote").extend([vote])
                voting_dict = old_voting
            data = {"$set": voting_dict}
            res = self.b4e_voting_collection.update_one(key, data, upsert=True)
            return res
        except Exception as e:
            print(e)
            return None

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

    def insert_class(self, class_dict):
        try:
            key = {'class_id': class_dict['class_id'],
                   'institution_public_key': class_dict['institution_public_key']}
            # class_dict["student_public_keys"] = list(class_dict["student_public_keys"])
            data = {"$set": class_dict}
            res = self.b4e_class_collection.update_one(key, data, upsert=True)
            return res
        except Exception as e:
            print(e)
            LOGGER.warning(e)
            return None

    def insert_portfolio(self, portfolio_dict):
        try:
            key = {'owner_public_key': portfolio_dict['owner_public_key'],
                   'manager_public_key': portfolio_dict['manager_public_key'],
                   'id': portfolio_dict['id']}

            data = {"$set": portfolio_dict}
            res = self.b4e_portfolio_collection.update_one(key, data, upsert=True)
            return res
        except Exception as e:
            print(e)
            LOGGER.warning(e)
            return None


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def to_time_stamp(date_time):
    return datetime.datetime.timestamp(date_time)
