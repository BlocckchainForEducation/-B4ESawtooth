from addressing.b4e_addressing import addresser
from config.config import SawtoothConfig
from protobuf.b4e_protobuf import payload_pb2
from rest_api.b4e_rest_api.transaction_creation.transaction_creation import _make_batch, _make_batch_multi_transactions, \
    slice_per


def make_create_record(transaction_signer,
                       batch_signer,
                       owner_public_key,
                       manager_public_key,
                       record_id,
                       portfolio_id,
                       cipher,
                       record_hash,
                       timestamp):
    issuer_public_key = transaction_signer.get_public_key().as_hex()
    manager_address = addresser.get_actor_address(manager_public_key)
    issuer_address = addresser.get_actor_address(issuer_public_key)
    record_address = addresser.get_record_address(record_id, owner_public_key, manager_public_key)

    inputs = [manager_address, issuer_address, record_address]

    outputs = [record_address]

    record_type = payload_pb2.OTHER

    action = payload_pb2.CreateRecordAction(owner_public_key=owner_public_key,
                                            manager_public_key=manager_public_key,
                                            issuer_public_key=issuer_public_key,
                                            record_id=record_id,
                                            record_type=record_type,
                                            portfolio_id=portfolio_id,
                                            cipher=cipher,
                                            hash=record_hash)

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.CREATE_RECORD,
        create_record=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_create_subject(transaction_signer,
                        batch_signer,
                        owner_public_key,
                        manager_public_key,
                        record_id,
                        portfolio_id,
                        cipher,
                        record_hash,
                        timestamp):
    issuer_public_key = transaction_signer.get_public_key().as_hex()
    manager_address = addresser.get_actor_address(manager_public_key)
    issuer_address = addresser.get_actor_address(issuer_public_key)
    record_address = addresser.get_record_address(record_id, owner_public_key, manager_public_key)
    class_address = addresser.get_class_address(record_id, manager_public_key)

    inputs = [manager_address, issuer_address, record_address, class_address]

    outputs = [record_address]

    record_type = payload_pb2.SUBJECT
    action = payload_pb2.CreateRecordAction(owner_public_key=owner_public_key,
                                            manager_public_key=manager_public_key,
                                            issuer_public_key=issuer_public_key,
                                            record_id=record_id,
                                            record_type=record_type,
                                            portfolio_id=portfolio_id,
                                            cipher=cipher,
                                            hash=record_hash)

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.CREATE_SUBJECT,
        create_subject=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_create_subjects(transaction_signer,
                         batch_signer,
                         manager_public_key,
                         class_id,
                         list_subjects,
                         timestamp):
    issuer_public_key = transaction_signer.get_public_key().as_hex()
    manager_address = addresser.get_actor_address(manager_public_key)
    issuer_address = addresser.get_actor_address(issuer_public_key)
    class_address = addresser.get_class_address(class_id, manager_public_key)

    record_type = payload_pb2.SUBJECT

    list_subjects = slice_per(list_subjects, SawtoothConfig.MAX_BATCH_SIZE)
    list_batches = []
    for subjects in list_subjects:
        list_inputs = []
        list_outputs = []
        list_payload_bytes = []
        for subject in subjects:
            subject_address = addresser.get_record_address(class_id,
                                                           subject.get('studentPublicKey'),
                                                           manager_public_key)
            inputs = [manager_address, issuer_address, subject_address, class_address]

            outputs = [subject_address]

            action = payload_pb2.CreateRecordAction(owner_public_key=subject.get("studentPublicKey"),
                                                    manager_public_key=manager_public_key,
                                                    issuer_public_key=issuer_public_key,
                                                    record_id=class_id,
                                                    record_type=record_type,
                                                    portfolio_id=subject.get("eduProgramId"),
                                                    cipher=subject.get("cipher"),
                                                    hash=subject.get("hash"))

            payload = payload_pb2.B4EPayload(
                action=payload_pb2.B4EPayload.CREATE_SUBJECT,
                create_subject=action,
                timestamp=timestamp)

            payload_bytes = payload.SerializeToString()

            list_inputs.append(inputs)
            list_outputs.append(outputs)
            list_payload_bytes.append(payload_bytes)

        batch = _make_batch_multi_transactions(
            list_payload_bytes=list_payload_bytes,
            list_inputs=list_inputs,
            list_outputs=list_outputs,
            transaction_signer=transaction_signer,
            batch_signer=batch_signer)
        list_batches.append(batch)

    return list_batches


def make_create_cert(transaction_signer,
                     batch_signer,
                     owner_public_key,
                     record_id,
                     portfolio_id,
                     cipher,
                     record_hash,
                     timestamp):
    issuer_public_key = transaction_signer.get_public_key().as_hex()
    manager_public_key = owner_public_key
    manager_address = addresser.get_actor_address(manager_public_key)
    issuer_address = addresser.get_actor_address(issuer_public_key)
    record_address = addresser.get_record_address(record_id, owner_public_key, manager_public_key)
    edu_program_address = addresser.get_portfolio_address(record_id, owner_public_key, manager_public_key)

    inputs = [manager_address, issuer_address, record_address, edu_program_address]

    outputs = [record_address]

    record_type = payload_pb2.CERTIFICATE
    action = payload_pb2.CreateRecordAction(owner_public_key=owner_public_key,
                                            manager_public_key=manager_public_key,
                                            issuer_public_key=issuer_public_key,
                                            record_id=record_id,
                                            record_type=record_type,
                                            portfolio_id=portfolio_id,
                                            cipher=cipher,
                                            hash=record_hash)

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.CREATE_CERT,
        create_cert=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_create_certs(transaction_signer,
                      batch_signer,
                      certs,
                      timestamp):
    manager_public_key = transaction_signer.get_public_key().as_hex()
    manager_address = addresser.get_actor_address(manager_public_key)
    record_type = payload_pb2.CERTIFICATE
    list_certs = slice_per(certs, SawtoothConfig.MAX_BATCH_SIZE)
    list_batches = []
    for certs in list_certs:
        list_inputs = []
        list_outputs = []
        list_payload_bytes = []
        for cert in certs:
            cert_id = cert.get('eduProgramId')
            owner_public_key = cert.get('studentPublicKey')
            edu_program_address = addresser.get_portfolio_address(cert_id, owner_public_key, manager_public_key)

            cert_address = addresser.get_record_address(cert_id,
                                                        owner_public_key,
                                                        manager_public_key)
            inputs = [manager_address, edu_program_address, cert_address]

            outputs = [cert_address]

            action = payload_pb2.CreateRecordAction(owner_public_key=cert.get("studentPublicKey"),
                                                    manager_public_key=manager_public_key,
                                                    issuer_public_key=manager_public_key,
                                                    record_id=cert.get("eduProgramId"),
                                                    record_type=record_type,
                                                    portfolio_id=cert.get("eduProgramId"),
                                                    cipher=cert.get("cipher"),
                                                    hash=cert.get("hash"))

            payload = payload_pb2.B4EPayload(
                action=payload_pb2.B4EPayload.CREATE_CERT,
                create_cert=action,
                timestamp=timestamp)

            payload_bytes = payload.SerializeToString()

            list_inputs.append(inputs)
            list_outputs.append(outputs)
            list_payload_bytes.append(payload_bytes)

        batch = _make_batch_multi_transactions(
            list_payload_bytes=list_payload_bytes,
            list_inputs=list_inputs,
            list_outputs=list_outputs,
            transaction_signer=transaction_signer,
            batch_signer=batch_signer)
        list_batches.append(batch)
    return list_batches


def _get_record_status(i):
    switch = {
        "CREATE": payload_pb2.CREATED,
        "REVOKED": payload_pb2.REVOKED,
        "REACTIVATED": payload_pb2.REACTIVATED
    }
    return switch.get(i)


def make_update_record(transaction_signer,
                       batch_signer,
                       owner_public_key,
                       record_id,
                       cipher,
                       record_hash,
                       status,
                       timestamp):
    manager_public_key = transaction_signer.get_public_key().as_hex()
    manager_address = addresser.get_actor_address(manager_public_key)
    record_address = addresser.get_record_address(record_id, owner_public_key, manager_public_key, )

    inputs = [manager_address, record_address]

    outputs = [record_address]
    action = payload_pb2.UpdateRecordAction(record_id=record_id,
                                            cipher=cipher,
                                            hash=record_hash,
                                            owner_public_key=owner_public_key,
                                            record_status=_get_record_status(status))

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.UPDATE_RECORD,
        update_record=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def _modify_record(transaction_signer,
                   batch_signer,
                   owner_public_key,
                   record_id,
                   cipher,
                   record_hash,
                   modify_action,
                   timestamp):
    manager_public_key = transaction_signer.get_public_key().as_hex()
    manager_address = addresser.get_actor_address(manager_public_key)
    record_address = addresser.get_record_address(record_id, owner_public_key, manager_public_key, )

    inputs = [manager_address, record_address]

    outputs = [record_address]
    action = payload_pb2.ModifyRecordAction(record_id=record_id,
                                            cipher=cipher,
                                            hash=record_hash,
                                            owner_public_key=owner_public_key)

    payload = payload_pb2.B4EPayload(
        action=modify_action,
        update_record=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_modify_subject(transaction_signer,
                        batch_signer,
                        owner_public_key,
                        record_id,
                        cipher,
                        record_hash,
                        timestamp):
    return _modify_record(transaction_signer, batch_signer,
                          owner_public_key, record_id, cipher,
                          record_hash, payload_pb2.B4EPayload.MODIFY_SUBJECT, timestamp)


def make_modify_cert(transaction_signer,
                     batch_signer,
                     owner_public_key,
                     record_id,
                     cipher,
                     record_hash,
                     timestamp):
    return _modify_record(transaction_signer, batch_signer,
                          owner_public_key, record_id, cipher,
                          record_hash, payload_pb2.B4EPayload.MODIFY_CERT, timestamp)


def _status_change(transaction_signer,
                   batch_signer,
                   owner_public_key,
                   record_id,
                   action_name,
                   timestamp):
    manager_public_key = transaction_signer.get_public_key().as_hex()
    manager_address = addresser.get_actor_address(manager_public_key)
    record_address = addresser.get_record_address(record_id, owner_public_key, manager_public_key, )

    inputs = [manager_address, record_address]

    outputs = [record_address]
    action = payload_pb2.RevokeCertAction(record_id=record_id,
                                          owner_public_key=owner_public_key)

    payload = payload_pb2.B4EPayload(
        action=action_name,
        update_record=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_revoke_cert(transaction_signer,
                     batch_signer,
                     owner_public_key,
                     record_id,
                     timestamp):
    return _status_change(transaction_signer,
                          batch_signer,
                          owner_public_key,
                          record_id,
                          payload_pb2.B4EPayload.REVOKE_CERT,
                          timestamp)


def make_reactive_cert(transaction_signer,
                       batch_signer,
                       owner_public_key,
                       record_id,
                       timestamp):
    return _status_change(transaction_signer,
                          batch_signer,
                          owner_public_key,
                          record_id,
                          payload_pb2.B4EPayload.REACTIVE_CERT,
                          timestamp)
