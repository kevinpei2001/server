# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: smuTags_path_query.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='smuTags_path_query.proto',
  package='smuTags_path_query',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18smuTags_path_query.proto\x12\x12smuTags_path_query\"\'\n\x0esmuTagsRequest\x12\x15\n\rdevice_string\x18\x01 \x01(\t\"%\n\x0fsmuTagsResponse\x12\x12\n\nreturnPath\x18\x01 \x03(\t2\x81\x01\n\x1asmuTags_path_query_Service\x12\x63\n\x16smuTags_path_query_rpc\x12\".smuTags_path_query.smuTagsRequest\x1a#.smuTags_path_query.smuTagsResponse\"\x00\x62\x06proto3'
)




_SMUTAGSREQUEST = _descriptor.Descriptor(
  name='smuTagsRequest',
  full_name='smuTags_path_query.smuTagsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_string', full_name='smuTags_path_query.smuTagsRequest.device_string', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=48,
  serialized_end=87,
)


_SMUTAGSRESPONSE = _descriptor.Descriptor(
  name='smuTagsResponse',
  full_name='smuTags_path_query.smuTagsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='returnPath', full_name='smuTags_path_query.smuTagsResponse.returnPath', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=89,
  serialized_end=126,
)

DESCRIPTOR.message_types_by_name['smuTagsRequest'] = _SMUTAGSREQUEST
DESCRIPTOR.message_types_by_name['smuTagsResponse'] = _SMUTAGSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

smuTagsRequest = _reflection.GeneratedProtocolMessageType('smuTagsRequest', (_message.Message,), {
  'DESCRIPTOR' : _SMUTAGSREQUEST,
  '__module__' : 'smuTags_path_query_pb2'
  # @@protoc_insertion_point(class_scope:smuTags_path_query.smuTagsRequest)
  })
_sym_db.RegisterMessage(smuTagsRequest)

smuTagsResponse = _reflection.GeneratedProtocolMessageType('smuTagsResponse', (_message.Message,), {
  'DESCRIPTOR' : _SMUTAGSRESPONSE,
  '__module__' : 'smuTags_path_query_pb2'
  # @@protoc_insertion_point(class_scope:smuTags_path_query.smuTagsResponse)
  })
_sym_db.RegisterMessage(smuTagsResponse)



_SMUTAGS_PATH_QUERY_SERVICE = _descriptor.ServiceDescriptor(
  name='smuTags_path_query_Service',
  full_name='smuTags_path_query.smuTags_path_query_Service',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=129,
  serialized_end=258,
  methods=[
  _descriptor.MethodDescriptor(
    name='smuTags_path_query_rpc',
    full_name='smuTags_path_query.smuTags_path_query_Service.smuTags_path_query_rpc',
    index=0,
    containing_service=None,
    input_type=_SMUTAGSREQUEST,
    output_type=_SMUTAGSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SMUTAGS_PATH_QUERY_SERVICE)

DESCRIPTOR.services_by_name['smuTags_path_query_Service'] = _SMUTAGS_PATH_QUERY_SERVICE

# @@protoc_insertion_point(module_scope)