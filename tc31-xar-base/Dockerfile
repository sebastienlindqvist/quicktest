FROM osrf/ros:humble-desktop-full

# Install curl and ca-certificates to load bhf.asc signing file from beckhoff.com during build
RUN apt-get update \
    && apt-get install --yes \
    curl \
    ca-certificates \
    python3 \
    python3-pip

RUN pip3 install pyads && \
    pip3 install PyYAML && \
    pip3 install termcolor

RUN sudo apt install ros-humble-turtlesim
RUN sudo apt install ros-humble-rqt
RUN sudo apt install python3-rosdep

#RUN pip3 install pyads

RUN apt install python3-colcon-common-extensions
RUN apt install python3-colcon-mixin
#RUN colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml
RUN colcon mixin update default
RUN apt install python3-vcstool

RUN mkdir -p ~/ros2_ws/src
RUN cd ~/ros2_ws/src && \
git clone https://github.com/ros2/examples -b humble && \
git clone https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4.git && \
git clone https://github.com/sebastienlindqvist/py_srvcli.git

RUN mkdir -p ~/ws_moveit2/src
RUN cd ~/ws_moveit2/src && \
git clone --branch humble https://github.com/ros-planning/moveit2_tutorials &&\
vcs import < moveit2_tutorials/moveit2_tutorials.repos

RUN cd ~/ros2_ws && \
. /opt/ros/$ROS_DISTRO/setup.sh && \
    colcon build --symlink-install

#RUN cd ~/ws_moveit2 &&\
#colcon build --mixin release 

RUN echo "export DOBOT_TYPE=cr3" >> ~/.bashrc
RUN echo "export IP_address=192.168.5.1" >> ~/.bashrc



# Use login information in the bhf.conf file to authenticate against deb*.beckhoff.com
# See https://manpages.debian.org/testing/apt/apt_auth.conf.5.en.html for more information
RUN --mount=type=secret,id=apt \
    curl --fail --netrc-file "/run/secrets/apt" \
    -o /usr/share/keyrings/bhf.asc \
    https://deb.beckhoff.com/repo.pub
    



# Replace default debian.org package sources via deb*.bechoff.com
# From here on, all packages will be loaded 
#RUN rm /etc/apt/sources.list.d/debian.sources
COPY ./apt-config/bhf.list ./apt-config/debian.sources.list /etc/apt/sources.list.d/



#RUN --mount=type=secret,id=apt \
#    apt-get -o "Dir::Etc::netrc=/run/secrets/apt" update \
#    && apt-get -o "Dir::Etc::netrc=/run/secrets/apt" install --yes \
#    tc31-xar-um \
#    libtcrte \
#    && rm -rf /var/lib/apt/lists/*

# As an example, copy basic TwinCAT runtime configurations files
#ARG TC3_DIR=/etc/TwinCAT/3.1
#COPY TwinCAT/StaticRoutes.xml $TC3_DIR/Target/
#COPY TwinCAT/TcRegistry.xml $TC3_DIR/

#EXPOSE 8016/tcp
#EXPOSE 48898/tcp
#EXPOSE 48899/udp

WORKDIR /app
COPY entrypoint.sh /app/

CMD [ "/bin/sh", "/app/entrypoint.sh"]
