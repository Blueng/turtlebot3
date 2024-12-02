import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yoonkangrok/Turtlebot3_Manipulator/install/turtlebot3_manipulator'
