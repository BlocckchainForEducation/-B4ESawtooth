import datetime
import time

from addressing.b4e_addressing import addresser
from protobuf.b4e_protobuf import payload_pb2
from scripts.transaction_services import sent_tx, get_signer, get_public_key


def modify_record_payload(record_id, cipher, record_hash, owner_public_key, manager_public_key, modify_action,
                          timestamp=None):
    action = payload_pb2.ModifyRecordAction(record_id=record_id,
                                            cipher=cipher,
                                            hash=record_hash,
                                            owner_public_key=owner_public_key,
                                            manager_public_key=manager_public_key
                                            )

    if not timestamp:
        timestamp = get_time()
    payload = payload_pb2.B4EPayload(
        action=modify_action,
        modify_subject=action,
        timestamp=timestamp)

    return payload


def get_time():
    dts = datetime.datetime.utcnow()
    return round(time.mktime(dts.timetuple()) + dts.microsecond / 1e6)


def create_valid_record(record_id="record_id",
                        cipher="cipher",
                        record_hash="record_hash",
                        owner_public_key="owner_public_key",
                        manager_public_key="manager_public_key",
                        private_key="",
                        restapi="http://localhost:8005"):
    public_key = get_public_key(private_key)

    modify_action = payload_pb2.B4EPayload.MODIFY_CERT

    payload = modify_record_payload(record_id, cipher, record_hash, owner_public_key, manager_public_key, modify_action)

    modifier_address = addresser.get_actor_address(public_key)
    manager_address = addresser.get_actor_address(manager_public_key)
    class_address = addresser.get_class_address(record_id, manager_public_key)
    record_address = addresser.get_record_address(record_id, owner_public_key, manager_public_key, )

    inputs = [modifier_address, manager_address, class_address, record_address]

    outputs = [record_address]

    sent_tx(payload, private_key,
            family_name="b4e", family_version="1.2",
            inputs=inputs, outputs=outputs,
            restapi=restapi)


