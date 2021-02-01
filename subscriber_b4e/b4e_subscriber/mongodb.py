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
        self.b4e_university_profile_collection = None
        self.b4e_vote_request_collection = None

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
        self.b4e_university_profile_collection = self.b4e_db[MongoDBConfig.UNIVERSITY_PROFILE]
        self.b4e_vote_request_collection = self.b4e_db[MongoDBConfig.VOTE_REQUEST]

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
            self.b4e_university_profile_collection.delte_many(delete)
            self.b4e_vote_request_collection.delte_many(delete)

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
            key = {'pubkey': actor_dict['actor_public_key']}
            if actor_dict["role"] != "INSTITUTION":
                return

            university_profile = eval(actor_dict['info'][0]['data'])
            university_profile['pubkey'] = actor_dict['actor_public_key']
            if actor_dict["status"] == "WAITING":
                state = "voting"
            elif actor_dict["status"] == "ACTIVE":
                state = "accepted"
            elif actor_dict["status"] == "REJECT":
                state = "declined"

            university_profile['state'] = state
            university_profile['block_num'] = actor_dict['block_num']
            university_profile['end_block_num'] = actor_dict['end_block_num']
            old_actor = self.b4e_university_profile_collection.find_one(key)
            if old_actor:
                university_profile['end_block_num'] = actor_dict['block_num']
                university_profile['block_num'] = old_actor.get('block_num')
            data = {"$set": university_profile}
            res = self.b4e_university_profile_collection.update_one(key, data, upsert=True)
            return res
        except Exception as e:
            LOGGER.error(e)
            print(e)
            return None

    def insert_record(self, record_dict):
        try:
            return
        except Exception as e:
            print(e)
            return None

    def insert_voting(self, voting_dict):
        try:
            key = {'pubkey': voting_dict['elector_public_key']}

            try:

                voting_dict['vote'][-1]['block_num'] = voting_dict['block_num']
                voting_dict['vote'][-1]['elector_public_key'] = voting_dict['elector_public_key']
                LOGGER.warning("update voting")
                self.insert_vote(voting_dict['vote'][-1])
            except Exception as e:
                LOGGER.info("Create Voting")
                vote_request = eval(voting_dict["data"])
                vote_request['state'] = 'new'
                vote_request['block_num'] = voting_dict['block_num']
                data = {"$set": vote_request}
                res = self.b4e_vote_request_collection.update_one(key, data, upsert=True)

            close_timestamp = voting_dict['close_vote_timestamp']
            if close_timestamp > 0:
                data = {"$set": {"voteCloseDate": timestamp_to_datetime(close_timestamp)}}
                self.b4e_university_profile_collection.update_one(key, data, upsert=True)
        except Exception as e:
            print(e)
            return None

    def insert_vote(self, vote_dict):
        try:
            if vote_dict["accepted"]:
                decision = "accept"
            else:
                decision = "decline"

            key = {'pubkey': vote_dict['elector_public_key']}
            vote = {
                "publicKey": vote_dict['issuer_public_key'],
                "decision": decision,
                "time": timestamp_to_datetime(vote_dict['timestamp']),
                "blockNum": vote_dict['block_num']
            }

            data = {"$push": {'votes': vote}}
            res = self.b4e_university_profile_collection.update_one(key, data, upsert=True)
            return res
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
            return
        except Exception as e:
            print(e)
            LOGGER.warning(e)
            return None


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def to_time_stamp(date_time):
    return datetime.datetime.timestamp(date_time)
