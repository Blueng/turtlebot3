// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from manipulator_interface:msg/LogMsg.idl
// generated code does not contain a copyright notice

#ifndef MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__STRUCT_HPP_
#define MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__manipulator_interface__msg__LogMsg __attribute__((deprecated))
#else
# define DEPRECATED__manipulator_interface__msg__LogMsg __declspec(deprecated)
#endif

namespace manipulator_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct LogMsg_
{
  using Type = LogMsg_<ContainerAllocator>;

  explicit LogMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->log = "";
    }
  }

  explicit LogMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : log(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->log = "";
    }
  }

  // field types and members
  using _log_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _log_type log;

  // setters for named parameter idiom
  Type & set__log(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->log = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    manipulator_interface::msg::LogMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const manipulator_interface::msg::LogMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<manipulator_interface::msg::LogMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<manipulator_interface::msg::LogMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      manipulator_interface::msg::LogMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<manipulator_interface::msg::LogMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      manipulator_interface::msg::LogMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<manipulator_interface::msg::LogMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<manipulator_interface::msg::LogMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<manipulator_interface::msg::LogMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__manipulator_interface__msg__LogMsg
    std::shared_ptr<manipulator_interface::msg::LogMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__manipulator_interface__msg__LogMsg
    std::shared_ptr<manipulator_interface::msg::LogMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LogMsg_ & other) const
  {
    if (this->log != other.log) {
      return false;
    }
    return true;
  }
  bool operator!=(const LogMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LogMsg_

// alias to use template instance with default allocator
using LogMsg =
  manipulator_interface::msg::LogMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace manipulator_interface

#endif  // MANIPULATOR_INTERFACE__MSG__DETAIL__LOG_MSG__STRUCT_HPP_
