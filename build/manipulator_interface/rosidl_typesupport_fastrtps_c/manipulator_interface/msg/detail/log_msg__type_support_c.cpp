// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from manipulator_interface:msg/LogMsg.idl
// generated code does not contain a copyright notice
#include "manipulator_interface/msg/detail/log_msg__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "manipulator_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "manipulator_interface/msg/detail/log_msg__struct.h"
#include "manipulator_interface/msg/detail/log_msg__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // log
#include "rosidl_runtime_c/string_functions.h"  // log

// forward declare type support functions


using _LogMsg__ros_msg_type = manipulator_interface__msg__LogMsg;

static bool _LogMsg__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _LogMsg__ros_msg_type * ros_message = static_cast<const _LogMsg__ros_msg_type *>(untyped_ros_message);
  // Field name: log
  {
    const rosidl_runtime_c__String * str = &ros_message->log;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _LogMsg__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _LogMsg__ros_msg_type * ros_message = static_cast<_LogMsg__ros_msg_type *>(untyped_ros_message);
  // Field name: log
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->log.data) {
      rosidl_runtime_c__String__init(&ros_message->log);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->log,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'log'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_manipulator_interface
size_t get_serialized_size_manipulator_interface__msg__LogMsg(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _LogMsg__ros_msg_type * ros_message = static_cast<const _LogMsg__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name log
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->log.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _LogMsg__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_manipulator_interface__msg__LogMsg(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_manipulator_interface
size_t max_serialized_size_manipulator_interface__msg__LogMsg(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: log
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = manipulator_interface__msg__LogMsg;
    is_plain =
      (
      offsetof(DataType, log) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _LogMsg__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_manipulator_interface__msg__LogMsg(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_LogMsg = {
  "manipulator_interface::msg",
  "LogMsg",
  _LogMsg__cdr_serialize,
  _LogMsg__cdr_deserialize,
  _LogMsg__get_serialized_size,
  _LogMsg__max_serialized_size
};

static rosidl_message_type_support_t _LogMsg__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_LogMsg,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, manipulator_interface, msg, LogMsg)() {
  return &_LogMsg__type_support;
}

#if defined(__cplusplus)
}
#endif
