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

from addressing.b4e_addressing import addresser

from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import b4e_environment_pb2
from protobuf.b4e_protobuf import class_pb2
from protobuf.b4e_protobuf import voting_pb2

from processor.b4e_tp.state import b4e_environment_state, \
    actor_state, class_state, record_state, voting_state, \
    portfolio_state

import logging

LOGGER = logging.getLogger(__name__)


class B4EState(object):
    def __init__(self, context, timeout=10):
        self._context = context
        self._timeout = timeout

    def get_b4e_environment(self):
        return b4e_environment_state.get(self)

    def set_b4e_environment(self, transaction_id):
        b4e_environment_state.create(self, transaction_id)

    def add_one_b4e_environment(self, transaction_id):
        b4e_environment_state.add_one(self, transaction_id)

    def get_actor(self, public_key):
        return actor_state.get_actor(self, public_key)

    def set_actor(self, actor, public_key):
        actor_state.set_actor(self, actor, public_key)

    def set_active_actor(self, public_key, timestamp, transaction_id):
        actor_state.set_active_actor(self, public_key, timestamp, transaction_id)

    def set_reject_actor(self, public_key, timestamp, transaction_id):
        actor_state.set_reject_actor(self, public_key, timestamp, transaction_id)

    def update_actor_profile(self, actor_public_key, data, timestamp, transaction_id):
        actor_state.update_actor_profile(self, actor_public_key, data, timestamp, transaction_id)

    def get_voting(self, public_key):
        return voting_state.get_voting(self, public_key)

    def set_voting(self, voting, public_key):
        voting_state.set_voting(self, voting, public_key)

    def update_voting(self, public_key, vote_result, vote, timestamp):
        voting_state.update_voting(self, public_key, vote_result, vote, timestamp)

    def get_class(self, class_id, institution_public_key):
        return class_state.get_class(self, class_id, institution_public_key)

    def set_class(self, class_):
        class_state.set_class(self, class_)

    def get_record(self, record_id, owner_public_key, manager_public_key):
        return record_state.get_record(self, record_id, owner_public_key, manager_public_key)

    def set_record(self, record):
        record_state.set_record(self, record)

    def update_record(self, record_id, owner_public_key,
                      manager_public_key, cipher, hash_data,
                      status, timestamp, transaction_id):
        record_state.update_record(self, record_id, owner_public_key, manager_public_key,
                                   cipher, hash_data, status, timestamp, transaction_id)

    def modify_record(self, record_id, owner_public_key,
                      manager_public_key, cipher, hash_data,
                      timestamp, transaction_id):
        record_state.modify_record(self, record_id, owner_public_key,
                                   manager_public_key, cipher, hash_data,
                                   timestamp, transaction_id)

    def update_status_record(self, record_id, owner_public_key,
                             manager_public_key, record_status,
                             timestamp, transaction_id):
        record_state.update_status(self, record_id, owner_public_key,
                                   manager_public_key, record_status,
                                   timestamp, transaction_id)

    def get_portfolio(self, id, owner_public_key, manager_public_key):
        return portfolio_state.get_portfolio(self, id, owner_public_key, manager_public_key)

    def create_portfolio(self, portfolio):
        portfolio_state.create_edu_program(self, portfolio)

    def update_portfolio_data(self, id, owner_public_key, manager_public_key, data):
        portfolio_state.update_data(self, id, owner_public_key, manager_public_key)
