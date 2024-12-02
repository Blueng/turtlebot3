// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from manipulator_interface:msg/LogMsg.idl
// generated code does not contain a copyright notice

#ifndef MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__BUILDER_HPP_
#define MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "manipulator_interface/msg/detail/log_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace manipulator_interface
{

namespace msg
{

namespace builder
{

class Init_LogMsg_log
{
public:
  Init_LogMsg_log()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::manipulator_interface::msg::LogMsg log(::manipulator_interface::msg::LogMsg::_log_type arg)
  {
    msg_.log = std::move(arg);
    return std::move(msg_);
  }

private:
  ::manipulator_interface::msg::LogMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::manipulator_interface::msg::LogMsg>()
{
  return manipulator_interface::msg::builder::Init_LogMsg_log();
}

}  // namespace manipulator_interface

#endif  // MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__BUILDER_HPP_
