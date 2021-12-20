/* Generated by the protocol buffer compiler.  DO NOT EDIT! */
/* Generated from: proto/logging.proto */

/* Do not generate deprecated warnings for self */
#ifndef PROTOBUF_C__NO_DEPRECATED
#define PROTOBUF_C__NO_DEPRECATED
#endif

#include "proto/logging.pb-c.h"
void   dias__log_message__init
                     (Dias__LogMessage         *message)
{
  static const Dias__LogMessage init_value = DIAS__LOG_MESSAGE__INIT;
  *message = init_value;
}
size_t dias__log_message__get_packed_size
                     (const Dias__LogMessage *message)
{
  assert(message->base.descriptor == &dias__log_message__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t dias__log_message__pack
                     (const Dias__LogMessage *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &dias__log_message__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t dias__log_message__pack_to_buffer
                     (const Dias__LogMessage *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &dias__log_message__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
Dias__LogMessage *
       dias__log_message__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (Dias__LogMessage *)
     protobuf_c_message_unpack (&dias__log_message__descriptor,
                                allocator, len, data);
}
void   dias__log_message__free_unpacked
                     (Dias__LogMessage *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &dias__log_message__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
static const ProtobufCEnumValue dias__log_message__priority__enum_values_by_number[3] =
{
  { "HIGH", "DIAS__LOG_MESSAGE__PRIORITY__HIGH", 0 },
  { "MEDIUM", "DIAS__LOG_MESSAGE__PRIORITY__MEDIUM", 1 },
  { "LOW", "DIAS__LOG_MESSAGE__PRIORITY__LOW", 2 },
};
static const ProtobufCIntRange dias__log_message__priority__value_ranges[] = {
{0, 0},{0, 3}
};
static const ProtobufCEnumValueIndex dias__log_message__priority__enum_values_by_name[3] =
{
  { "HIGH", 0 },
  { "LOW", 2 },
  { "MEDIUM", 1 },
};
const ProtobufCEnumDescriptor dias__log_message__priority__descriptor =
{
  PROTOBUF_C__ENUM_DESCRIPTOR_MAGIC,
  "dias.LogMessage.Priority",
  "Priority",
  "Dias__LogMessage__Priority",
  "dias",
  3,
  dias__log_message__priority__enum_values_by_number,
  3,
  dias__log_message__priority__enum_values_by_name,
  1,
  dias__log_message__priority__value_ranges,
  NULL,NULL,NULL,NULL   /* reserved[1234] */
};
static const ProtobufCEnumValue dias__log_message__level__enum_values_by_number[5] =
{
  { "CRITICAL", "DIAS__LOG_MESSAGE__LEVEL__CRITICAL", 0 },
  { "ERROR", "DIAS__LOG_MESSAGE__LEVEL__ERROR", 1 },
  { "WARNING", "DIAS__LOG_MESSAGE__LEVEL__WARNING", 3 },
  { "INFO", "DIAS__LOG_MESSAGE__LEVEL__INFO", 4 },
  { "DEBUG", "DIAS__LOG_MESSAGE__LEVEL__DEBUG", 5 },
};
static const ProtobufCIntRange dias__log_message__level__value_ranges[] = {
{0, 0},{3, 2},{0, 5}
};
static const ProtobufCEnumValueIndex dias__log_message__level__enum_values_by_name[5] =
{
  { "CRITICAL", 0 },
  { "DEBUG", 4 },
  { "ERROR", 1 },
  { "INFO", 3 },
  { "WARNING", 2 },
};
const ProtobufCEnumDescriptor dias__log_message__level__descriptor =
{
  PROTOBUF_C__ENUM_DESCRIPTOR_MAGIC,
  "dias.LogMessage.Level",
  "Level",
  "Dias__LogMessage__Level",
  "dias",
  5,
  dias__log_message__level__enum_values_by_number,
  5,
  dias__log_message__level__enum_values_by_name,
  2,
  dias__log_message__level__value_ranges,
  NULL,NULL,NULL,NULL   /* reserved[1234] */
};
static const ProtobufCFieldDescriptor dias__log_message__field_descriptors[1] =
{
  {
    "message",
    1,
    PROTOBUF_C_LABEL_REQUIRED,
    PROTOBUF_C_TYPE_STRING,
    0,   /* quantifier_offset */
    offsetof(Dias__LogMessage, message),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned dias__log_message__field_indices_by_name[] = {
  0,   /* field[0] = message */
};
static const ProtobufCIntRange dias__log_message__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 1 }
};
const ProtobufCMessageDescriptor dias__log_message__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "dias.LogMessage",
  "LogMessage",
  "Dias__LogMessage",
  "dias",
  sizeof(Dias__LogMessage),
  1,
  dias__log_message__field_descriptors,
  dias__log_message__field_indices_by_name,
  1,  dias__log_message__number_ranges,
  (ProtobufCMessageInit) dias__log_message__init,
  NULL,NULL,NULL    /* reserved[123] */
};
