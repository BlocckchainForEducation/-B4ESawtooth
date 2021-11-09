from cheat_processor.b4e_tp.handler.actor_handler import _create_actor
from protobuf.b4e_protobuf import actor_pb2


def create_company(state, public_key, transaction_id, payload):
    _create_actor(state=state,
                  public_key=public_key,
                  transaction_id=transaction_id,
                  manager_public_key=public_key,
                  status=actor_pb2.Actor.ACTIVE,
                  payload=payload,
                  role=actor_pb2.Actor.COMPANY)
