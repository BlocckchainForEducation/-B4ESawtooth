from hashlib import sha512

import urllib.request
from urllib.error import HTTPError

from cbor import cbor
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader, Batch, BatchList
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction, TransactionList
from sawtooth_signing import create_context, CryptoFactory, secp256k1


def get_signer(private_key):
    context = create_context('secp256k1')
    signer = CryptoFactory(context).new_signer(secp256k1.Secp256k1PrivateKey.from_hex(private_key))
    return signer


def get_public_key(private_key):
    signer = get_signer(private_key)
    return signer.get_public_key().as_hex()


def sent_tx(payload, private_key,
            family_name="b4e", family_version="1.2",
            inputs=[], outputs=[],
            restapi="http://localhost:8005"):
    signer = get_signer(private_key)
    payload_bytes = cbor.dumps(payload)

    txn_header_bytes = TransactionHeader(
        family_name=family_name,
        family_version=family_version,
        inputs=inputs,
        outputs=outputs,
        signer_public_key=signer.get_public_key().as_hex(),
        # In this example, we're signing the batch with the same private key,
        # but the batch can be signed by another party, in which case, the
        # public key will need to be associated with that key.
        batcher_public_key=signer.get_public_key().as_hex(),
        # In this example, there are no dependencies.  This list should include
        # an previous transaction header signatures that must be applied for
        # this transaction to successfully commit.
        # For example,
        # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
        dependencies=[],
        payload_sha512=sha512(payload_bytes).hexdigest()
    ).SerializeToString()

    signature = signer.sign(txn_header_bytes)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload=payload_bytes
    )
    print(f"Create tx with tx_id :{signature}")

    txn_list_bytes = TransactionList(
        transactions=[txn]
    ).SerializeToString()

    # txn_bytes = txn.SerializeToString()

    txns = [txn]

    batch_header_bytes = BatchHeader(
        signer_public_key=signer.get_public_key().as_hex(),
        transaction_ids=[txn.header_signature for txn in txns],
    ).SerializeToString()

    signature = signer.sign(batch_header_bytes)

    batch = Batch(
        header=batch_header_bytes,
        header_signature=signature,
        transactions=txns
    )

    print(f"Create batch : {signature}")
    batch_list_bytes = BatchList(batches=[batch]).SerializeToString()

    try:
        request = urllib.request.Request(
            f'{restapi}/batches',
            batch_list_bytes,
            method='POST',
            headers={'Content-Type': 'application/octet-stream'})
        response = urllib.request.urlopen(request)

    except HTTPError as e:
        response = e.file
    print(response)
