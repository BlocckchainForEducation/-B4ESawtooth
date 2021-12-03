import logging

from addressing.b4e_addressing import addresser

from protobuf.b4e_protobuf import actor_pb2

logger = logging.getLogger("Actor state")


def get_actor(self, public_key):
    try:
        logger.info(f"Get actor info with pubkey:{public_key}")
        address = addresser.get_actor_address(public_key)
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container = actor_pb2.ActorContainer()
            container.ParseFromString(state_entries[0].data)
            for actor in container.entries:
                if actor.actor_public_key == public_key:
                    return actor

        return None
    except Exception as e:
        print("Err :", e)
        return None


def set_actor(self, actor, public_key):
    actor_address = addresser.get_actor_address(public_key)
    container = actor_pb2.ActorContainer()
    state_entries = self._context.get_state(
        addresses=[actor_address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)

    container.entries.extend([actor])
    data = container.SerializeToString()

    updated_state = {}
    updated_state[actor_address] = data
    self._context.set_state(updated_state, timeout=self._timeout)


def set_active_actor(self, public_key, timestamp, transaction_id):
    address = addresser.get_actor_address(public_key)
    container = actor_pb2.ActorContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for actor in container.entries:
            if actor.actor_public_key == public_key:
                pre_profile = actor.profile[-1]
                new_profile = actor_pb2.Actor.Profile(data=pre_profile.data,
                                                      status=actor_pb2.Actor.ACTIVE,
                                                      timestamp=timestamp,
                                                      transaction_id=transaction_id)
                actor.profile.extend([new_profile])

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)


def set_reject_actor(self, public_key, timestamp, transaction_id):
    address = addresser.get_actor_address(public_key)
    container = actor_pb2.ActorContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for actor in container.entries:
            if actor.actor_public_key == public_key:
                pre_profile = actor.profile[-1]
                new_profile = actor_pb2.Actor.Profile(data=pre_profile.data,
                                                      status=actor_pb2.Actor.REJECT,
                                                      timestamp=timestamp,
                                                      transaction_id=transaction_id)
                actor.profile.extend([new_profile])

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)


def update_actor_profile(self, actor_public_key, data, timestamp, transaction_id):
    address = addresser.get_actor_address(actor_public_key)
    container = actor_pb2.ActorContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for actor in container.entries:
            if actor.actor_public_key == actor_public_key:
                pre_profile = actor.profile[-1]
                new_profile = actor_pb2.Actor.Profile(data=data,
                                                      status=pre_profile.status,
                                                      timestamp=timestamp,
                                                      transaction_id=transaction_id)
                actor.profile.extend([new_profile])

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)
