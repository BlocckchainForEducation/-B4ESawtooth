from addressing.b4e_addressing import addresser
from protobuf.b4e_protobuf import payload_pb2
from rest_api.b4e_rest_api.transaction_creation.transaction_creation import _make_batch


def make_set_b4e_environment(signer, timestamp):
    environment_address = addresser.ENVIRONMENT_ADDRESS
    inputs = [environment_address]
    outputs = [environment_address]

    action = payload_pb2.SetB4EEnvironmentAction(timestamp=timestamp)

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.SET_B4E_ENVIRONMENT,
        set_b4e_environment=action,
        timestamp=timestamp
    )

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=signer,
        batch_signer=signer)
