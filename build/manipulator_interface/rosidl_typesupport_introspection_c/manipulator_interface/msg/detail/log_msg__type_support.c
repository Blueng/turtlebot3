// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from manipulator_interface:msg/LogMsg.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "manipulator_interface/msg/detail/log_msg__rosidl_typesupport_introspection_c.h"
#include "manipulator_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "manipulator_interface/msg/detail/log_msg__functions.h"
#include "manipulator_interface/msg/detail/log_msg__struct.h"


// Include directives for member types
// Member `log`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  manipulator_interface__msg__LogMsg__init(message_memory);
}

void manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_fini_function(void * message_memory)
{
  manipulator_interface__msg__LogMsg__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_message_member_array[1] = {
  {
    "log",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(manipulator_interface__msg__LogMsg, log),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_message_members = {
  "manipulator_interface__msg",  // message namespace
  "LogMsg",  // message name
  1,  // number of fields
  sizeof(manipulator_interface__msg__LogMsg),
  manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_message_member_array,  // message members
  manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_init_function,  // function to initialize message memory (memory has to be allocated)
  manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_message_type_support_handle = {
  0,
  &manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_manipulator_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, manipulator_interface, msg, LogMsg)() {
  if (!manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_message_type_support_handle.typesupport_identifier) {
    manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &manipulator_interface__msg__LogMsg__rosidl_typesupport_introspection_c__LogMsg_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
