cmake_minimum_required(VERSION 3.5)
project(py_srvcli)

# Required dependencies for Python packages
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

# Install Python scripts
install(
    PROGRAMS
    scripts/client_member_function.py  # Your Python node
    DESTINATION lib/${PROJECT_NAME}
)

# Install resource files (e.g., the text file)
install(
    DIRECTORY resource/
    DESTINATION share/${PROJECT_NAME}/resource
)

# Package hooks (needed for Python)
ament_python_install_package(${PROJECT_NAME})

# Mark package for installation
ament_package()

