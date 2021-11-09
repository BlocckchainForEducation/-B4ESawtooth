from sawtooth_sdk.processor.exceptions import InvalidTransaction

from cheat_processor.b4e_tp.handler.actor_handler import _check_is_valid_actor

from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import payload_pb2
from protobuf.b4e_protobuf import voting_pb2
from protobuf.b4e_protobuf import class_pb2


def create_class(state, public_key, transaction_id, payload):
    institution = state.get_actor(public_key)
    _check_is_valid_actor(institution)

    if institution.role != actor_pb2.Actor.INSTITUTION:
        raise InvalidTransaction("Just institution can create class")

    if state.get_class(payload.data.class_id, public_key):
        raise InvalidTransaction("Class existed!")

    class_ = class_pb2.Class(class_id=payload.data.class_id,
                             subject_id=payload.data.subject_id,
                             credit=payload.data.credit,
                             teacher_public_key=payload.data.teacher_public_key,
                             institution_public_key=public_key,
                             student_public_keys=payload.data.student_public_keys,
                             timestamp=payload.timestamp,
                             transaction_id=transaction_id)

    state.set_class(class_)
