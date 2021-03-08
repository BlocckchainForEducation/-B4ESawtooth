from addressing.b4e_addressing import addresser

from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import b4e_environment_pb2
from protobuf.b4e_protobuf import class_pb2
from protobuf.b4e_protobuf import voting_pb2


def get(self):
    try:
        address = addresser.ENVIRONMENT_ADDRESS
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container = b4e_environment_pb2.B4EEnvironmentContainer()
            container.ParseFromString(state_entries[0].data)
            for environment in container.entries:
                return environment
        return None
    except Exception as e:
        print("Err :", e)
        return None


def create(self, transaction_id):
    environment = b4e_environment_pb2.B4EEnvironment(institution_number=0, transaction_id=transaction_id)
    environment_address = addresser.ENVIRONMENT_ADDRESS
    container = b4e_environment_pb2.B4EEnvironmentContainer()
    state_entries = self._context.get_state(
        addresses=[environment_address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)

    container.entries.extend([environment])
    data = container.SerializeToString()

    updated_state = {}
    updated_state[environment_address] = data
    response_address = self._context.set_state(updated_state, timeout=self._timeout)


def add_one(self, transaction_id):
    address = addresser.ENVIRONMENT_ADDRESS
    container = b4e_environment_pb2.B4EEnvironmentContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for env in container.entries:
            env.institution_number += 1
            env.transaction_id = transaction_id

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)
