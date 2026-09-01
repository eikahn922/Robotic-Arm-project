cmake_minimum_required(VERSION 3.8)
project(robot_arm_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    urdf
    STL
    launch
    rviz
    config
    test
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
