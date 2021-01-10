# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: payload.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='payload.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rpayload.proto\"\xb3\x06\n\nB4EPayload\x12\"\n\x06\x61\x63tion\x18\x01 \x01(\x0e\x32\x12.B4EPayload.Action\x12\x34\n\x12\x63reate_institution\x18\x02 \x01(\x0b\x32\x18.CreateInstitutionAction\x12,\n\x0e\x63reate_teacher\x18\x03 \x01(\x0b\x32\x14.CreateTeacherAction\x12\x33\n\x12\x63reate_edu_officer\x18\x04 \x01(\x0b\x32\x17.CreateEduOfficerAction\x12&\n\x0b\x63reate_vote\x18\x05 \x01(\x0b\x32\x11.CreateVoteAction\x12(\n\x0c\x63reate_class\x18\x06 \x01(\x0b\x32\x12.CreateClassAction\x12*\n\rcreate_record\x18\x07 \x01(\x0b\x32\x13.CreateRecordAction\x12&\n\x0b\x63reate_cert\x18\x08 \x01(\x0b\x32\x11.CreateCertAction\x12,\n\x0e\x63reate_subject\x18\t \x01(\x0b\x32\x14.CreateSubjectAction\x12*\n\rupdate_record\x18\n \x01(\x0b\x32\x13.UpdateRecordAction\x12\x31\n\x11update_actor_info\x18\x0b \x01(\x0b\x32\x16.UpdateActorInfoAction\x12\x35\n\x13set_b4e_environment\x18\x0c \x01(\x0b\x32\x18.SetB4EEnvironmentAction\x12\x11\n\ttimestamp\x18\r \x01(\x04\"\xea\x01\n\x06\x41\x63tion\x12\x16\n\x12\x43REATE_INSTITUTION\x10\x00\x12\x12\n\x0e\x43REATE_TEACHER\x10\x01\x12\x16\n\x12\x43REATE_EDU_OFFICER\x10\x02\x12\x0f\n\x0b\x43REATE_VOTE\x10\x03\x12\x10\n\x0c\x43REATE_CLASS\x10\x04\x12\x11\n\rCREATE_RECORD\x10\x06\x12\x0f\n\x0b\x43REATE_CERT\x10\x07\x12\x12\n\x0e\x43REATE_SUBJECT\x10\x08\x12\x11\n\rUPDATE_RECORD\x10\t\x12\x15\n\x11UPDATE_ACTOR_INFO\x10\n\x12\x17\n\x13SET_B4E_ENVIRONMENT\x10\x0b\"\x14\n\x04Info\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\":\n\x17\x43reateInstitutionAction\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x04info\x18\x03 \x01(\x0b\x32\x05.Info\"R\n\x13\x43reateTeacherAction\x12\n\n\x02id\x18\x01 \x01(\t\x12\x1a\n\x12teacher_public_key\x18\x02 \x01(\t\x12\x13\n\x04info\x18\x04 \x01(\x0b\x32\x05.Info\"Y\n\x16\x43reateEduOfficerAction\x12\n\n\x02id\x18\x01 \x01(\t\x12\x1e\n\x16\x65\x64u_officer_public_key\x18\x02 \x01(\t\x12\x13\n\x04info\x18\x04 \x01(\x0b\x32\x05.Info\"[\n\x10\x43reateVoteAction\x12\x19\n\x11issuer_public_key\x18\x01 \x01(\t\x12\x1a\n\x12\x65lector_public_key\x18\x02 \x01(\t\x12\x10\n\x08\x61\x63\x63\x65pted\x18\x03 \x01(\x08\"t\n\x11\x43reateClassAction\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\t\x12\x1a\n\x12teacher_public_key\x18\x02 \x01(\t\x12\x1e\n\x16\x65\x64u_officer_public_key\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\x04\"\xaf\x01\n\x12\x43reateRecordAction\x12\x18\n\x10owner_public_key\x18\x01 \x01(\t\x12\x1a\n\x12manager_public_key\x18\x02 \x01(\t\x12\x19\n\x11issuer_public_key\x18\x03 \x01(\t\x12\x11\n\trecord_id\x18\x04 \x01(\t\x12 \n\x0brecord_type\x18\x05 \x01(\x0e\x32\x0b.RecordType\x12\x13\n\x0brecord_data\x18\x06 \x01(\t\"\x8b\x01\n\x10\x43reateCertAction\x12\x18\n\x10owner_public_key\x18\x01 \x01(\t\x12\x1a\n\x12manager_public_key\x18\x02 \x01(\t\x12\x19\n\x11issuer_public_key\x18\x03 \x01(\t\x12\x11\n\trecord_id\x18\x04 \x01(\t\x12\x13\n\x0brecord_data\x18\x06 \x01(\t\"\x8e\x01\n\x13\x43reateSubjectAction\x12\x18\n\x10owner_public_key\x18\x01 \x01(\t\x12\x1a\n\x12manager_public_key\x18\x02 \x01(\t\x12\x19\n\x11issuer_public_key\x18\x03 \x01(\t\x12\x11\n\trecord_id\x18\x04 \x01(\t\x12\x13\n\x0brecord_data\x18\x06 \x01(\t\"\x82\x01\n\x12UpdateRecordAction\x12\x18\n\x10owner_public_key\x18\x01 \x01(\t\x12\x1a\n\x12manager_public_key\x18\x02 \x01(\t\x12\x11\n\trecord_id\x18\x03 \x01(\t\x12\x13\n\x0brecord_data\x18\x04 \x01(\t\x12\x0e\n\x06\x61\x63tive\x18\x05 \x01(\x08\",\n\x15UpdateActorInfoAction\x12\x13\n\x04info\x18\x03 \x01(\x0b\x32\x05.Info\",\n\x17SetB4EEnvironmentAction\x12\x11\n\ttimestamp\x18\x01 \x01(\x04**\n\nRecordType\x12\x0b\n\x07SUBJECT\x10\x00\x12\x0f\n\x0b\x43\x45RTIFICATE\x10\x01\x62\x06proto3')
)

_RECORDTYPE = _descriptor.EnumDescriptor(
  name='RecordType',
  full_name='RecordType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUBJECT', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CERTIFICATE', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1997,
  serialized_end=2039,
)
_sym_db.RegisterEnumDescriptor(_RECORDTYPE)

RecordType = enum_type_wrapper.EnumTypeWrapper(_RECORDTYPE)
SUBJECT = 0
CERTIFICATE = 1


_B4EPAYLOAD_ACTION = _descriptor.EnumDescriptor(
  name='Action',
  full_name='B4EPayload.Action',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CREATE_INSTITUTION', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATE_TEACHER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATE_EDU_OFFICER', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATE_VOTE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATE_CLASS', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATE_RECORD', index=5, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATE_CERT', index=6, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATE_SUBJECT', index=7, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPDATE_RECORD', index=8, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPDATE_ACTOR_INFO', index=9, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SET_B4E_ENVIRONMENT', index=10, number=11,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=603,
  serialized_end=837,
)
_sym_db.RegisterEnumDescriptor(_B4EPAYLOAD_ACTION)


_B4EPAYLOAD = _descriptor.Descriptor(
  name='B4EPayload',
  full_name='B4EPayload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='action', full_name='B4EPayload.action', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_institution', full_name='B4EPayload.create_institution', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_teacher', full_name='B4EPayload.create_teacher', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_edu_officer', full_name='B4EPayload.create_edu_officer', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_vote', full_name='B4EPayload.create_vote', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_class', full_name='B4EPayload.create_class', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_record', full_name='B4EPayload.create_record', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_cert', full_name='B4EPayload.create_cert', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_subject', full_name='B4EPayload.create_subject', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_record', full_name='B4EPayload.update_record', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_actor_info', full_name='B4EPayload.update_actor_info', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_b4e_environment', full_name='B4EPayload.set_b4e_environment', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='B4EPayload.timestamp', index=12,
      number=13, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _B4EPAYLOAD_ACTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=837,
)


_INFO = _descriptor.Descriptor(
  name='Info',
  full_name='Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='Info.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=839,
  serialized_end=859,
)


_CREATEINSTITUTIONACTION = _descriptor.Descriptor(
  name='CreateInstitutionAction',
  full_name='CreateInstitutionAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='CreateInstitutionAction.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='info', full_name='CreateInstitutionAction.info', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=861,
  serialized_end=919,
)


_CREATETEACHERACTION = _descriptor.Descriptor(
  name='CreateTeacherAction',
  full_name='CreateTeacherAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='CreateTeacherAction.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='teacher_public_key', full_name='CreateTeacherAction.teacher_public_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='info', full_name='CreateTeacherAction.info', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=921,
  serialized_end=1003,
)


_CREATEEDUOFFICERACTION = _descriptor.Descriptor(
  name='CreateEduOfficerAction',
  full_name='CreateEduOfficerAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='CreateEduOfficerAction.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='edu_officer_public_key', full_name='CreateEduOfficerAction.edu_officer_public_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='info', full_name='CreateEduOfficerAction.info', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1005,
  serialized_end=1094,
)


_CREATEVOTEACTION = _descriptor.Descriptor(
  name='CreateVoteAction',
  full_name='CreateVoteAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='issuer_public_key', full_name='CreateVoteAction.issuer_public_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='elector_public_key', full_name='CreateVoteAction.elector_public_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='accepted', full_name='CreateVoteAction.accepted', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1096,
  serialized_end=1187,
)


_CREATECLASSACTION = _descriptor.Descriptor(
  name='CreateClassAction',
  full_name='CreateClassAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='class_id', full_name='CreateClassAction.class_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='teacher_public_key', full_name='CreateClassAction.teacher_public_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='edu_officer_public_key', full_name='CreateClassAction.edu_officer_public_key', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='CreateClassAction.timestamp', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1189,
  serialized_end=1305,
)


_CREATERECORDACTION = _descriptor.Descriptor(
  name='CreateRecordAction',
  full_name='CreateRecordAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='owner_public_key', full_name='CreateRecordAction.owner_public_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='manager_public_key', full_name='CreateRecordAction.manager_public_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issuer_public_key', full_name='CreateRecordAction.issuer_public_key', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='record_id', full_name='CreateRecordAction.record_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='record_type', full_name='CreateRecordAction.record_type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='record_data', full_name='CreateRecordAction.record_data', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1308,
  serialized_end=1483,
)


_CREATECERTACTION = _descriptor.Descriptor(
  name='CreateCertAction',
  full_name='CreateCertAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='owner_public_key', full_name='CreateCertAction.owner_public_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='manager_public_key', full_name='CreateCertAction.manager_public_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issuer_public_key', full_name='CreateCertAction.issuer_public_key', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='record_id', full_name='CreateCertAction.record_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='record_data', full_name='CreateCertAction.record_data', index=4,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1486,
  serialized_end=1625,
)


_CREATESUBJECTACTION = _descriptor.Descriptor(
  name='CreateSubjectAction',
  full_name='CreateSubjectAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='owner_public_key', full_name='CreateSubjectAction.owner_public_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='manager_public_key', full_name='CreateSubjectAction.manager_public_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issuer_public_key', full_name='CreateSubjectAction.issuer_public_key', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='record_id', full_name='CreateSubjectAction.record_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='record_data', full_name='CreateSubjectAction.record_data', index=4,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1628,
  serialized_end=1770,
)


_UPDATERECORDACTION = _descriptor.Descriptor(
  name='UpdateRecordAction',
  full_name='UpdateRecordAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='owner_public_key', full_name='UpdateRecordAction.owner_public_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='manager_public_key', full_name='UpdateRecordAction.manager_public_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='record_id', full_name='UpdateRecordAction.record_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='record_data', full_name='UpdateRecordAction.record_data', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='active', full_name='UpdateRecordAction.active', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1773,
  serialized_end=1903,
)


_UPDATEACTORINFOACTION = _descriptor.Descriptor(
  name='UpdateActorInfoAction',
  full_name='UpdateActorInfoAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='UpdateActorInfoAction.info', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1905,
  serialized_end=1949,
)


_SETB4EENVIRONMENTACTION = _descriptor.Descriptor(
  name='SetB4EEnvironmentAction',
  full_name='SetB4EEnvironmentAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='SetB4EEnvironmentAction.timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1951,
  serialized_end=1995,
)

_B4EPAYLOAD.fields_by_name['action'].enum_type = _B4EPAYLOAD_ACTION
_B4EPAYLOAD.fields_by_name['create_institution'].message_type = _CREATEINSTITUTIONACTION
_B4EPAYLOAD.fields_by_name['create_teacher'].message_type = _CREATETEACHERACTION
_B4EPAYLOAD.fields_by_name['create_edu_officer'].message_type = _CREATEEDUOFFICERACTION
_B4EPAYLOAD.fields_by_name['create_vote'].message_type = _CREATEVOTEACTION
_B4EPAYLOAD.fields_by_name['create_class'].message_type = _CREATECLASSACTION
_B4EPAYLOAD.fields_by_name['create_record'].message_type = _CREATERECORDACTION
_B4EPAYLOAD.fields_by_name['create_cert'].message_type = _CREATECERTACTION
_B4EPAYLOAD.fields_by_name['create_subject'].message_type = _CREATESUBJECTACTION
_B4EPAYLOAD.fields_by_name['update_record'].message_type = _UPDATERECORDACTION
_B4EPAYLOAD.fields_by_name['update_actor_info'].message_type = _UPDATEACTORINFOACTION
_B4EPAYLOAD.fields_by_name['set_b4e_environment'].message_type = _SETB4EENVIRONMENTACTION
_B4EPAYLOAD_ACTION.containing_type = _B4EPAYLOAD
_CREATEINSTITUTIONACTION.fields_by_name['info'].message_type = _INFO
_CREATETEACHERACTION.fields_by_name['info'].message_type = _INFO
_CREATEEDUOFFICERACTION.fields_by_name['info'].message_type = _INFO
_CREATERECORDACTION.fields_by_name['record_type'].enum_type = _RECORDTYPE
_UPDATEACTORINFOACTION.fields_by_name['info'].message_type = _INFO
DESCRIPTOR.message_types_by_name['B4EPayload'] = _B4EPAYLOAD
DESCRIPTOR.message_types_by_name['Info'] = _INFO
DESCRIPTOR.message_types_by_name['CreateInstitutionAction'] = _CREATEINSTITUTIONACTION
DESCRIPTOR.message_types_by_name['CreateTeacherAction'] = _CREATETEACHERACTION
DESCRIPTOR.message_types_by_name['CreateEduOfficerAction'] = _CREATEEDUOFFICERACTION
DESCRIPTOR.message_types_by_name['CreateVoteAction'] = _CREATEVOTEACTION
DESCRIPTOR.message_types_by_name['CreateClassAction'] = _CREATECLASSACTION
DESCRIPTOR.message_types_by_name['CreateRecordAction'] = _CREATERECORDACTION
DESCRIPTOR.message_types_by_name['CreateCertAction'] = _CREATECERTACTION
DESCRIPTOR.message_types_by_name['CreateSubjectAction'] = _CREATESUBJECTACTION
DESCRIPTOR.message_types_by_name['UpdateRecordAction'] = _UPDATERECORDACTION
DESCRIPTOR.message_types_by_name['UpdateActorInfoAction'] = _UPDATEACTORINFOACTION
DESCRIPTOR.message_types_by_name['SetB4EEnvironmentAction'] = _SETB4EENVIRONMENTACTION
DESCRIPTOR.enum_types_by_name['RecordType'] = _RECORDTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

B4EPayload = _reflection.GeneratedProtocolMessageType('B4EPayload', (_message.Message,), dict(
  DESCRIPTOR = _B4EPAYLOAD,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:B4EPayload)
  ))
_sym_db.RegisterMessage(B4EPayload)

Info = _reflection.GeneratedProtocolMessageType('Info', (_message.Message,), dict(
  DESCRIPTOR = _INFO,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:Info)
  ))
_sym_db.RegisterMessage(Info)

CreateInstitutionAction = _reflection.GeneratedProtocolMessageType('CreateInstitutionAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATEINSTITUTIONACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateInstitutionAction)
  ))
_sym_db.RegisterMessage(CreateInstitutionAction)

CreateTeacherAction = _reflection.GeneratedProtocolMessageType('CreateTeacherAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATETEACHERACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateTeacherAction)
  ))
_sym_db.RegisterMessage(CreateTeacherAction)

CreateEduOfficerAction = _reflection.GeneratedProtocolMessageType('CreateEduOfficerAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATEEDUOFFICERACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateEduOfficerAction)
  ))
_sym_db.RegisterMessage(CreateEduOfficerAction)

CreateVoteAction = _reflection.GeneratedProtocolMessageType('CreateVoteAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATEVOTEACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateVoteAction)
  ))
_sym_db.RegisterMessage(CreateVoteAction)

CreateClassAction = _reflection.GeneratedProtocolMessageType('CreateClassAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATECLASSACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateClassAction)
  ))
_sym_db.RegisterMessage(CreateClassAction)

CreateRecordAction = _reflection.GeneratedProtocolMessageType('CreateRecordAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATERECORDACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateRecordAction)
  ))
_sym_db.RegisterMessage(CreateRecordAction)

CreateCertAction = _reflection.GeneratedProtocolMessageType('CreateCertAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATECERTACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateCertAction)
  ))
_sym_db.RegisterMessage(CreateCertAction)

CreateSubjectAction = _reflection.GeneratedProtocolMessageType('CreateSubjectAction', (_message.Message,), dict(
  DESCRIPTOR = _CREATESUBJECTACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:CreateSubjectAction)
  ))
_sym_db.RegisterMessage(CreateSubjectAction)

UpdateRecordAction = _reflection.GeneratedProtocolMessageType('UpdateRecordAction', (_message.Message,), dict(
  DESCRIPTOR = _UPDATERECORDACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:UpdateRecordAction)
  ))
_sym_db.RegisterMessage(UpdateRecordAction)

UpdateActorInfoAction = _reflection.GeneratedProtocolMessageType('UpdateActorInfoAction', (_message.Message,), dict(
  DESCRIPTOR = _UPDATEACTORINFOACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:UpdateActorInfoAction)
  ))
_sym_db.RegisterMessage(UpdateActorInfoAction)

SetB4EEnvironmentAction = _reflection.GeneratedProtocolMessageType('SetB4EEnvironmentAction', (_message.Message,), dict(
  DESCRIPTOR = _SETB4EENVIRONMENTACTION,
  __module__ = 'payload_pb2'
  # @@protoc_insertion_point(class_scope:SetB4EEnvironmentAction)
  ))
_sym_db.RegisterMessage(SetB4EEnvironmentAction)


# @@protoc_insertion_point(module_scope)
