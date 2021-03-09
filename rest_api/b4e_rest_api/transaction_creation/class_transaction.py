from addressing.b4e_addressing import addresser
from config.config import SawtoothConfig
from protobuf.b4e_protobuf import payload_pb2
from rest_api.b4e_rest_api.transaction_creation.transaction_creation import _make_batch, _make_batch_multi_transactions, \
    slice_per


def make_create_class(transaction_signer,
                      batch_signer,
                      class_id,
                      subject_id,
                      credit,
                      teacher_public_key,
                      student_public_keys,
                      timestamp):
    institution_public_key = transaction_signer.get_public_key().as_hex()
    class_address = addresser.get_class_address(class_id, institution_public_key)
    teacher_address = addresser.get_actor_address(teacher_public_key)
    institution_address = addresser.get_actor_address(institution_public_key)

    inputs = [class_address, teacher_address, institution_address]

    outputs = [class_address]

    action = payload_pb2.CreateClassAction(class_id=class_id,
                                           subject_id=subject_id,
                                           credit=credit,
                                           teacher_public_key=teacher_public_key,
                                           student_public_keys=student_public_keys)

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.CREATE_CLASS,
        create_class=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_create_classes(transaction_signer,
                        batch_signer,
                        classes,
                        timestamp):
    institution_public_key = transaction_signer.get_public_key().as_hex()
    institution_address = addresser.get_actor_address(institution_public_key)

    list_classes = slice_per(classes, SawtoothConfig.MAX_BATCH_SIZE)
    list_batches = []
    for classes in list_classes:
        list_inputs = []
        list_outputs = []
        list_payload_bytes = []
        for class_ in classes:
            class_address = addresser.get_class_address(class_.get('classId'), institution_public_key)
            teacher_address = addresser.get_actor_address(class_.get('teacherPublicKey'))

            inputs = [class_address, teacher_address, institution_address]

            outputs = [class_address]

            action = payload_pb2.CreateClassAction(class_id=class_.get("classId"),
                                                   subject_id=class_.get("subjectId"),
                                                   credit=class_.get("credit"),
                                                   teacher_public_key=class_.get("teacherPublicKey"),
                                                   student_public_keys=class_.get("studentPublicKeys"))

            payload = payload_pb2.B4EPayload(
                action=payload_pb2.B4EPayload.CREATE_CLASS,
                create_class=action,
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
