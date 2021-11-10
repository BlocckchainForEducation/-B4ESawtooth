import secp256k1

key_handler = secp256k1.PrivateKey()
private_key_bytes = key_handler.private_key

public_key_bytes = key_handler.pubkey.serialize()

public_key_hex = public_key_bytes.hex()

import cbor

payload = {
    'Verb': 'set',
    'Name': 'foo',
    'Value': 42}

payload_bytes = cbor.dumps(payload)

from hashlib import sha512

payload_sha512 = sha512(payload_bytes).hexdigest()


from random import randint
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader

txn_header = TransactionHeader(
    batcher_public_key=public_key_hex,
    # If we had any dependencies, this is what it might look like:
    # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
    family_name='intkey',
    family_version='1.0',
    inputs=['1cf1266e282c41be5e4254d8820772c5518a2c5a8c0c7f7eda19594a7eb539453e1ed7'],
    nonce=str(randint(0, 1000000000)),
    outputs=['1cf1266e282c41be5e4254d8820772c5518a2c5a8c0c7f7eda19594a7eb539453e1ed7'],
    payload_sha512=payload_sha512,
    signer_public_key=public_key_hex)

txn_header_bytes = txn_header.SerializeToString()


key_handler = secp256k1.PrivateKey(private_key_bytes)

# ecdsa_sign automatically generates a SHA-256 hash of the header bytes
txn_signature = key_handler.ecdsa_sign(txn_header_bytes)
txn_signature_bytes = key_handler.ecdsa_serialize_compact(txn_signature)
txn_signature_hex = txn_signature_bytes.hex()


from sawtooth_sdk.protobuf.transaction_pb2 import Transaction

txn = Transaction(
    header=txn_header_bytes,
    header_signature=txn_signature_hex,
    payload=payload_bytes)


from sawtooth_sdk.protobuf.transaction_pb2 import TransactionList

txnList = TransactionList(transactions=[txn])
txnBytes = txnList.SerializeToString()


txnList = TransactionList()
txnList.ParseFromString(txnBytes)

txn = txnList.transactions[0]

from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader

batch_header = BatchHeader(
    signer_public_key=public_key_hex,
    transaction_ids=[txn.header_signature])

batch_header_bytes = batch_header.SerializeToString()


batch_signature = key_handler.ecdsa_sign(batch_header_bytes)

batch_signature_bytes = key_handler.ecdsa_serialize_compact(batch_signature)

batch_signature_hex = batch_signature_bytes.hex()

from sawtooth_sdk.protobuf.batch_pb2 import Batch

batch = Batch(
    header=batch_header_bytes,
    header_signature=batch_signature_hex,
    transactions=[txn])


from sawtooth_sdk.protobuf.batch_pb2 import BatchList

batch_list = BatchList(batches=[batch])
batch_list_bytes = batch_list.SerializeToString()

import urllib.request
from urllib.error import HTTPError

try:
    request = urllib.request.Request(
        'http://localhost:8008/batches',
        batch_list_bytes,
        method='POST',
        headers={'Content-Type': 'application/octet-stream'})
    response = urllib.request.urlopen(request)

except HTTPError as e:
    response = e.file


output = open('intkey.batches', 'wb')
output.write(batch_list_bytes)