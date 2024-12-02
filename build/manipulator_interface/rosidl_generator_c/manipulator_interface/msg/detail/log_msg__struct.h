// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from manipulator_interface:msg/LogMsg.idl
// generated code does not contain a copyright notice

#ifndef MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__STRUCT_H_
#define MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'log'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/LogMsg in the package manipulator_interface.
/**
  * msg
 */
typedef struct manipulator_interface__msg__LogMsg
{
  rosidl_runtime_c__String log;
} manipulator_interface__msg__LogMsg;

// Struct for a sequence of manipulator_interface__msg__LogMsg.
typedef struct manipulator_interface__msg__LogMsg__Sequence
{
  manipulator_interface__msg__LogMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} manipulator_interface__msg__LogMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__STRUCT_H_
