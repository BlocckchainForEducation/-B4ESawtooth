from addressing.b4e_addressing import addresser
from protobuf.b4e_protobuf import payload_pb2
from rest_api.b4e_rest_api.transaction_creation.transaction_creation import _make_batch


def make_create_vote(transaction_signer,
                     batch_signer,
                     elector_public_key,
                     accepted,
                     timestamp):
    issuer_public_key = transaction_signer.get_public_key().as_hex()
    environment_address = addresser.ENVIRONMENT_ADDRESS
    voting_address = addresser.get_voting_address(elector_public_key)
    issuer_vote_address = addresser.get_actor_address(issuer_public_key)
    elector_address = addresser.get_actor_address(elector_public_key)

    inputs = [environment_address, voting_address, issuer_vote_address, elector_address]

    outputs = [voting_address, elector_address, environment_address]

    action = payload_pb2.VoteAction(elector_public_key=elector_public_key,
                                    accepted=accepted)

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.VOTE,
        create_vote=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def _get_vote_type(i):
    switch = {
        "ACTIVE": payload_pb2.ACTIVE,
        "REJECT": payload_pb2.REJECT
    }
    return switch.get(i)


def make_create_voting(transaction_signer,
                       batch_signer,
                       elector_public_key,
                       vote_type,
                       timestamp):
    issuer_public_key = transaction_signer.get_public_key().as_hex()
    issuer_address = addresser.get_actor_address(issuer_public_key)
    elector_address = addresser.get_actor_address(elector_public_key)
    voting_address = addresser.get_voting_address(elector_public_key)
    inputs = [issuer_address, elector_address, voting_address]

    outputs = [voting_address]

    action = payload_pb2.CreateVotingAction(elector_public_key=elector_public_key,
                                            accepted=_get_vote_type(vote_type))

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.CREATE_VOTING,
        create_vote=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)
