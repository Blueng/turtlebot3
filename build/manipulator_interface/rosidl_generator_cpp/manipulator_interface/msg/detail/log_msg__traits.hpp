// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from manipulator_interface:msg/LogMsg.idl
// generated code does not contain a copyright notice

#ifndef MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__TRAITS_HPP_
#define MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "manipulator_interface/msg/detail/log_msg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace manipulator_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const LogMsg & msg,
  std::ostream & out)
{
  out << "{";
  // member: log
  {
    out << "log: ";
    rosidl_generator_traits::value_to_yaml(msg.log, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LogMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: log
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "log: ";
    rosidl_generator_traits::value_to_yaml(msg.log, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LogMsg & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace manipulator_interface

namespace rosidl_generator_traits
{

[[deprecated("use manipulator_interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const manipulator_interface::msg::LogMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  manipulator_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use manipulator_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const manipulator_interface::msg::LogMsg & msg)
{
  return manipulator_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<manipulator_interface::msg::LogMsg>()
{
  return "manipulator_interface::msg::LogMsg";
}

template<>
inline const char * name<manipulator_interface::msg::LogMsg>()
{
  return "manipulator_interface/msg/LogMsg";
}

template<>
struct has_fixed_size<manipulator_interface::msg::LogMsg>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<manipulator_interface::msg::LogMsg>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<manipulator_interface::msg::LogMsg>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__TRAITS_HPP_
