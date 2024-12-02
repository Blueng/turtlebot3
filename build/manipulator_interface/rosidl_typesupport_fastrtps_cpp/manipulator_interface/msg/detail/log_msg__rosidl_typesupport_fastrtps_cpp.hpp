// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from manipulator_interface:msg/LogMsg.idl
// generated code does not contain a copyright notice

#ifndef MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "manipulator_interface/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "manipulator_interface/msg/detail/log_msg__struct.hpp"

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

#include "fastcdr/Cdr.h"

namespace manipulator_interface
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_manipulator_interface
cdr_serialize(
  const manipulator_interface::msg::LogMsg & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_manipulator_interface
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  manipulator_interface::msg::LogMsg & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_manipulator_interface
get_serialized_size(
  const manipulator_interface::msg::LogMsg & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_manipulator_interface
max_serialized_size_LogMsg(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace manipulator_interface

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_manipulator_interface
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, manipulator_interface, msg, LogMsg)();

#ifdef __cplusplus
}
#endif

#endif  // MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
