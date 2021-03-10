from addressing.b4e_addressing import addresser

from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import b4e_environment_pb2
from protobuf.b4e_protobuf import class_pb2
from protobuf.b4e_protobuf import voting_pb2
from protobuf.b4e_protobuf import portfolio_pb2


def get_portfolio(self, id, owner_public_key, manager_public_key):
    try:
        address = addresser.get_portfolio_address(id, owner_public_key, manager_public_key)
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container = portfolio_pb2.PortfolioContainer()
            container.ParseFromString(state_entries[0].data)
            for portfolio in container.entries:
                if portfolio.id == id and portfolio.owner_public_key == owner_public_key \
                        and portfolio.manager_public_key == manager_public_key:
                    return portfolio

        return None
    except Exception as e:
        print("Err :", e)
        return None


def create_edu_program(self, portfolio):
    address = addresser.get_record_address(portfolio.id, portfolio.owner_public_key, portfolio.manager_public_key)

    container = portfolio_pb2.PortfolioContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)

    container.entries.extend([portfolio])
    data = container.SerializeToString()

    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)


def update_data(self, id, owner_public_key,
                manager_public_key, new_data):
    address = addresser.get_portfolio_address(id, owner_public_key, manager_public_key)
    container = portfolio_pb2.PortfolioContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for portfolio in container.entries:
            if portfolio.id == id \
                    and portfolio.owner_public_key == owner_public_key \
                    and portfolio.manager_public_key == manager_public_key:
                portfolio_data = portfolio.portfolio_data[-1]
                portfolio_data.data = new_data

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)
