from addressing.b4e_addressing import addresser

from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import b4e_environment_pb2
from protobuf.b4e_protobuf import class_pb2
from protobuf.b4e_protobuf import voting_pb2


def get_record(self, record_id, owner_public_key, manager_public_key):
    try:
        address = addresser.get_record_address(record_id, owner_public_key, manager_public_key)
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container = record_pb2.RecordContainer()
            container.ParseFromString(state_entries[0].data)
            for record in container.entries:
                if record.record_id == record_id and record.owner_public_key == owner_public_key and record.manager_public_key == manager_public_key:
                    return record

        return None
    except Exception as e:
        print("Err :", e)
        return None


def set_record(self, record):
    address = addresser.get_record_address(record.record_id, record.owner_public_key, record.manager_public_key)

    container = record_pb2.RecordContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)

    container.entries.extend([record])
    data = container.SerializeToString()

    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)


def update_record(self, record_id, owner_public_key,
                  manager_public_key, cipher, hash_data,
                  status, timestamp, transaction_id):
    address = addresser.get_record_address(record_id, owner_public_key, manager_public_key)
    container = record_pb2.RecordContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for record in container.entries:
            if record.record_id == record_id:
                pre_data = record.versions[-1]
                new_data = record_pb2.Record.RecordData(
                    protfolio_id=pre_data.portfolio,
                    cipher=cipher,
                    hash=hash_data,
                    record_status=status,
                    timestamp=timestamp,
                    transaction_id=transaction_id
                )
                record.versions.extend([new_data])

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)


def modify_record(self, record_id, owner_public_key,
                  manager_public_key, cipher, hash_data,
                  timestamp, transaction_id):
    address = addresser.get_record_address(record_id, owner_public_key, manager_public_key)
    container = record_pb2.RecordContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for record in container.entries:
            if record.record_id == record_id:
                pre_data = record.versions[-1]
                new_data = record_pb2.Record.RecordData(
                    portfolio_id=pre_data.portfolio_id,
                    cipher=cipher,
                    hash=hash_data,
                    record_status=pre_data.record_status,
                    timestamp=timestamp,
                    transaction_id=transaction_id
                )
                record.versions.extend([new_data])

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)


def update_status(self, record_id, owner_public_key,
                  manager_public_key, record_status,
                  timestamp, transaction_id):
    address = addresser.get_record_address(record_id, owner_public_key, manager_public_key)
    container = record_pb2.RecordContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for record in container.entries:
            if record.record_id == record_id:
                pre_data = record.versions[-1]
                new_data = record_pb2.Record.RecordData(
                    portfolio_id=pre_data.portfolio_id,
                    cipher=pre_data.cipher,
                    hash=pre_data.hash,
                    record_status=record_status,
                    timestamp=timestamp,
                    transaction_id=transaction_id
                )
                record.versions.extend([new_data])

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)
