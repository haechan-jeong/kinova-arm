# Kinova-arm
Code created for various manipulation tasks using the 6 Degree of Freedom Kinova Gen3.
Maintained by the Özay group at the University of Michigan.

This code is based upon the work done by Kwesi Rutledge in the repository
https://github.com/kwesiRutledge/OzayGroupExploration.git
To pull changes from this repository, you can add it as remote location with
    
    git remote add upstream https://github.com/kwesiRutledge/OzayGroupExploration.git

Then when you want to pull changes:

    git pull upstream main
    
If unwanted files are added when merging with upstream, then you will have to remove them. This workflow is flawed, but will work for now.

## Getting Started

There are two possible methods for getting started with `kinova-arm`.
1. Docker
2. Local Install

The Docker method for getting started appears to be more robust (won't break as often), but
it is not necessary if you are working on the lab laptop.

### Docker

In this section we will discuss how to: build the Drake-Kinova Docker Image and run a container with it.

In order to control the 6 Degree of Freedom Kinova Gen3 in the Özay group, [Drake](https://drake.mit.edu/) is used along with the [Kinova Kortex API](https://github.com/Kinovarobotics/kortex) and [kinova_drake](https://github.com/vincekurtz/kinova_drake) (a library built by Vince Kurtz).

If you are interested in getting set up with all of the software that you need to control our robot, do the following:
1. Pull this git repository.
2. From the repository's main directory, run a shell script to create the docker image: `./shell-scripts/create-drake-v2-docker-image.sh`.
3. Start the docker container: `./shell-scripts/run-drake-v2-docker-container.sh`

### Local Install

For a local install, we will simply create a local environment
from inside of `kinova-arm` and import everything there.

```shell
python3.10 -m venv kinova-arm-venv
kinova-arm-venv/bin/pip install --upgrade pip
kinova-arm-venv/bin/pip install -r requirements.txt
kinova-arm-venv/bin/pip install -e .
source kinova-arm-venv/bin/activate
```

### Developing Code for Kinova

Make sure that the container named drake-container is running, use an editor like VS Code to begin developing.

In VS Code, you can attach your application to the running container, giving you access to all of the libraries installed in the container after you built it.

## Additional Info

- [Hardware Instructions](./doc/kinova-hardware-instructions.md)