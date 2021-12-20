/* Generated by the protocol buffer compiler.  DO NOT EDIT! */
/* Generated from: proto/base.proto */

#ifndef PROTOBUF_C_proto_2fbase_2eproto__INCLUDED
#define PROTOBUF_C_proto_2fbase_2eproto__INCLUDED

#include <protobuf-c/protobuf-c.h>

PROTOBUF_C__BEGIN_DECLS

#if PROTOBUF_C_VERSION_NUMBER < 1000000
# error This file was generated by a newer version of protoc-c which is incompatible with your libprotobuf-c headers. Please update your headers.
#elif 1003003 < PROTOBUF_C_MIN_COMPILER_VERSION
# error This file was generated by an older version of protoc-c which is incompatible with your libprotobuf-c headers. Please regenerate this file with a newer version of protoc-c.
#endif


typedef struct _Dias__RequestHeader Dias__RequestHeader;
typedef struct _Dias__ReplyHeader Dias__ReplyHeader;


/* --- enums --- */


/* --- messages --- */

struct  _Dias__RequestHeader
{
  ProtobufCMessage base;
  uint64_t id;
  char *name;
};
#define DIAS__REQUEST_HEADER__INIT \
 { PROTOBUF_C_MESSAGE_INIT (&dias__request_header__descriptor) \
    , 0, NULL }


struct  _Dias__ReplyHeader
{
  ProtobufCMessage base;
  uint64_t id;
};
#define DIAS__REPLY_HEADER__INIT \
 { PROTOBUF_C_MESSAGE_INIT (&dias__reply_header__descriptor) \
    , 0 }


/* Dias__RequestHeader methods */
void   dias__request_header__init
                     (Dias__RequestHeader         *message);
size_t dias__request_header__get_packed_size
                     (const Dias__RequestHeader   *message);
size_t dias__request_header__pack
                     (const Dias__RequestHeader   *message,
                      uint8_t             *out);
size_t dias__request_header__pack_to_buffer
                     (const Dias__RequestHeader   *message,
                      ProtobufCBuffer     *buffer);
Dias__RequestHeader *
       dias__request_header__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data);
void   dias__request_header__free_unpacked
                     (Dias__RequestHeader *message,
                      ProtobufCAllocator *allocator);
/* Dias__ReplyHeader methods */
void   dias__reply_header__init
                     (Dias__ReplyHeader         *message);
size_t dias__reply_header__get_packed_size
                     (const Dias__ReplyHeader   *message);
size_t dias__reply_header__pack
                     (const Dias__ReplyHeader   *message,
                      uint8_t             *out);
size_t dias__reply_header__pack_to_buffer
                     (const Dias__ReplyHeader   *message,
                      ProtobufCBuffer     *buffer);
Dias__ReplyHeader *
       dias__reply_header__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data);
void   dias__reply_header__free_unpacked
                     (Dias__ReplyHeader *message,
                      ProtobufCAllocator *allocator);
/* --- per-message closures --- */

typedef void (*Dias__RequestHeader_Closure)
                 (const Dias__RequestHeader *message,
                  void *closure_data);
typedef void (*Dias__ReplyHeader_Closure)
                 (const Dias__ReplyHeader *message,
                  void *closure_data);

/* --- services --- */


/* --- descriptors --- */

extern const ProtobufCMessageDescriptor dias__request_header__descriptor;
extern const ProtobufCMessageDescriptor dias__reply_header__descriptor;

PROTOBUF_C__END_DECLS


#endif  /* PROTOBUF_C_proto_2fbase_2eproto__INCLUDED */
