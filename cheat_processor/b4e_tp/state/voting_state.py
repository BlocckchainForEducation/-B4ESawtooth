from addressing.b4e_addressing import addresser

from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import b4e_environment_pb2
from protobuf.b4e_protobuf import class_pb2
from protobuf.b4e_protobuf import voting_pb2


def get_voting(self, public_key):
    try:
        address = addresser.get_voting_address(public_key)
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        latest_voting = None
        timestamp = -1
        if state_entries:
            container = voting_pb2.VotingContainer()
            container.ParseFromString(state_entries[0].data)
            for voting in container.entries:
                if voting.elector_public_key == public_key:
                    if voting.timestamp > timestamp:
                        latest_voting = voting
                        timestamp = voting.timestamp

        return latest_voting
    except Exception as e:
        print("Err :", e)
        return None


def set_voting(self, voting, public_key):
    voting_address = addresser.get_voting_address(public_key)
    container = voting_pb2.VotingContainer()
    state_entries = self._context.get_state(
        addresses=[voting_address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)

    container.entries.extend([voting])
    data = container.SerializeToString()

    updated_state = {}
    updated_state[voting_address] = data
    self._context.set_state(updated_state, timeout=self._timeout)


def update_voting(self, elector_public_key, vote_result, vote, timestamp):
    address = addresser.get_voting_address(elector_public_key)
    container = voting_pb2.VotingContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for voting in container.entries:
            if voting.elector_public_key == elector_public_key:
                voting.vote.extend([vote])
                voting.close_vote_timestamp = timestamp
                voting.vote_result = vote_result

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)
