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


from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from addressing.b4e_addressing import addresser

from protobuf.b4e_protobuf import payload_pb2

from processor.b4e_tp.payload import B4EPayload
from processor.b4e_tp.state.state import B4EState

from processor.b4e_tp.handler import actor_handler, \
    class_handler, portfolio_handler, record_handler, \
    voting_handler, validator, b4e_environment_handler

import logging

SYNC_TOLERANCE = 60 * 5
LOGGER = logging.getLogger(__name__)


class B4EHandler(TransactionHandler):

    @property
    def family_name(self):
        return addresser.FAMILY_NAME

    @property
    def family_versions(self):
        return [addresser.FAMILY_VERSION]

    @property
    def namespaces(self):
        return [addresser.NAMESPACE]

    def apply(self, transaction, context):
        header = transaction.header
        payload = B4EPayload(transaction.payload)
        state = B4EState(context)

        validator.validate_timestamp(payload.timestamp)

        if payload.action == payload_pb2.B4EPayload.CREATE_ACTOR:
            actor_handler.create_actor(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.CREATE_INSTITUTION:
            actor_handler.create_institution(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.CREATE_TEACHER:
            actor_handler.create_teacher(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.CREATE_EDU_PROGRAM:
            portfolio_handler.create_edu_program(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.CREATE_CLASS:
            class_handler.create_class(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.CREATE_VOTING:
            voting_handler.create_voting(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.VOTE:
            voting_handler.vote(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.CREATE_RECORD:
            record_handler.create_record(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.CREATE_CERT:
            record_handler.create_cert(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.CREATE_SUBJECT:
            record_handler.create_subject(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.UPDATE_RECORD:
            record_handler.update_record(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.MODIFY_SUBJECT:
            record_handler.modify_subject(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.MODIFY_CERT:
            record_handler.modifiy_cert(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.REVOKE_CERT:
            record_handler.revoke_cert(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.REACTIVE_CERT:
            record_handler.reactive_cert(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.UPDATE_ACTOR_PROFILE:
            actor_handler.update_actor_profile(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.REJECT_INSTITUTION:
            actor_handler.reject_institution(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.ACTIVE_INSTITUTION:
            actor_handler.active_institution(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        elif payload.action == payload_pb2.B4EPayload.SET_B4E_ENVIRONMENT:
            b4e_environment_handler.set_b4e_environment(
                state=state,
                public_key=header.signer_public_key,
                transaction_id=transaction.signature,
                payload=payload)
        else:
            raise InvalidTransaction('Unhandled action')
