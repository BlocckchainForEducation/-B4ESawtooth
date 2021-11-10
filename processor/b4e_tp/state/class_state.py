from addressing.b4e_addressing import addresser

from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import b4e_environment_pb2
from protobuf.b4e_protobuf import class_pb2
from protobuf.b4e_protobuf import voting_pb2


def get_class(self, class_id, institution_public_key):
    try:
        print(f"Get class {class_id}")
        address = addresser.get_class_address(class_id, institution_public_key)
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container = class_pb2.ClassContainer()
            container.ParseFromString(state_entries[0].data)
            for class_ in container.entries:
                if class_.class_id == class_id:
                    return class_

        return None
    except Exception as e:
        print("Err :", e)
        return


def set_class(self, class_):
    class_address = addresser.get_class_address(class_.class_id, class_.institution_public_key)
    container = class_pb2.ClassContainer()
    print(f"Create class {class_.class_id}")
    state_entries = self._context.get_state(
        addresses=[class_address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)

    container.entries.extend([class_])
    data = container.SerializeToString()

    updated_state = {}
    updated_state[class_address] = data
    self._context.set_state(updated_state, timeout=self._timeout)
