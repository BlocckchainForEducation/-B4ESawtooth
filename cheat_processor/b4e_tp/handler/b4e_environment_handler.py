from sawtooth_sdk.processor.exceptions import InvalidTransaction


def set_b4e_environment(state, public_key, transaction_id, payload):
    if not state.get_b4e_environment():
        state.set_b4e_environment(transaction_id)

    else:
        raise InvalidTransaction("Environment just set once time!")
