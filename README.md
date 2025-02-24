# About this repository

This repository provides a sample setup for creating and running a Docker container with a TwinCAT 3.1 XAR environment.
The repository includes all necessary files to build the Docker image and run it using Docker Compose.

# How to get support

Should you have any questions regarding the provided sample code, please contact your local Beckhoff support team. Contact information can be found on the official Beckhoff website at https://www.beckhoff.com/contact/.

# Using the sample

To use the sample, simply follow these steps:

1. Inform yourself about TwinCAT for Linux® via your local Beckhoff support team.
2. Ensure to have a supported Beckhoff IPC with the latest version of the Beckhoff Real-Time Linux® Distribution installed.
3. Follow the instructions on [Docker Engine on Debian](https://docs.docker.com/engine/install/debian/#install-using-the-repository) to install Docker as container management software
4. [Build the container image](#building-the-docker-image) via `sudo make build-image`
5. [Create firewall rules](#firewall-rules-for-mqtt-connections) to allow [connections via ADS over MQTT](#connection-via-ads-over-mqtt)
6. [Create and run the container setup](#running-the-container) via `sudo make run-containers`
7. On your TwinCAT Engineering station, adjust your ADS-Routes to [establish a connection between TwinCAT XAR and the container](#establish-a-ads-over-mqtt-connection-between-twincat-xae-and-xar)
8. Configure the network interfaces [for real-time Ethernet communication](#configure-the-host-for-real-time-ethernet-communication)

## Detailed information about the sample

### Repository structure

The repository is organized as follows:

- `docker-compose.yaml`: Sample to define the run configuration for the containers
- `Makefile`: Used to simplify and automate common Docker tasks.
- `simple-mosquitto.conf`: Simple configuration file for Mosquitto MQTT broker used for ADS over MQTT
- `tc31-xar-base/`: Contains all required files to build a Docker image for a TwinCAT 3.1 XAR environment
    - `Dockerfile`: Defines the instructions to build the Docker image.
    - `TwinCAT/`
        - `StaticRoutes.xml`: Sample configuration to use ADS over MQTT
        - `TcRegistry.xml`: Sample set of TwinCAT XAR configuration
    - `apt-config/`
        - `bhf.conf`: Template for authentication against beckhoff.com package server
        - `bhf.list`: apt source list sample for Beckhoff package repo
        - `debian.sources.list`: apt source list for Beckhoff Debian mirror
    - `entrypoint.sh`: Script used as entrypoint to start TcSystemServiceUm on container start

### Makefile Summary

The `Makefile` in this repository is used to simplify and automate common Docker tasks in this sample.
It includes the following targets:

- `build-image`: Builds the Docker image using the Dockerfile located in the `tc31-xar-base` directory.
- `push-image`: Pushes the built Docker image to a specified Docker registry.
- `run-containers`: Starts the containers defined in the `docker-compose.yaml` file.
- `list-containers`: Lists the running containers managed by Docker Compose.
- `stop-and-remove-containers`: Stops and removes all containers defined in the `docker-compose.yaml` file.
- `container-logs`: Displays the logs of the running containers.

The `Makefile` uses variables to define the image name, tag, and registry, allowing for easy customization.

You can install `make` on your host via:

```
sudo apt install make
```

## Building the Docker Image

During the image build process TwinCAT for Linux® will be loaded as package from `https://deb.beckhoff.com`.

Before you build the image, ensure to insert valid mybeckhoff credentials by replacing `<mybeckhoff-mail>` and `<mybeckhoff-password>` inside `./tc31-xar-base/apt-config/bhf.conf`.

Afterwards you can use the `Makefile` for building the image.

```
sudo make build-image
```

Alternatively, navigate to `tc31-xar-base` of the repository and run the following command:

```sh
sudo docker build --network host -t tc31-xar-base .
```

The `tc31-xar-base` subfolder contains all the necessary files and configurations required to build a Docker image for a TwinCAT 3.1 XAR environment.
The intention of this subfolder is to provide a self-contained build context for creating a Docker image that can run TwinCAT applications.