# NavRL: Learning Safe Flight in Dynamic Environments
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://docs.python.org/3/whatsnew/3.10.html)
[![ROS1](https://img.shields.io/badge/ROS1-Noetic-yellow.svg)](https://wiki.ros.org/noetic)
[![ROS2](https://img.shields.io/badge/ROS2-Humble-orange.svg)](https://docs.ros.org/en/humble/index.html)
[![IsaacSim](https://img.shields.io/badge/IsaacSim-NVIDIA-red.svg)](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html)
[![Linux platform](https://img.shields.io/badge/platform-Ubuntu--20.04-green.svg)](https://releases.ubuntu.com/20.04/)
[![Linux platform](https://img.shields.io/badge/platform-Ubuntu--22.04-purple.svg)](https://releases.ubuntu.com/22.04/)


Welcome to the NavRL repository! This repository provides the implementation of the [NavRL](https://arxiv.org/pdf/2409.15634) framework, designed to enable robots to safely navigate dynamic environments using Deep Reinforcement Learning. 

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/49467fe4-e1c5-4f6d-a619-6e2063f99c5b" alt="mill19 2nd - gif" style="width: 100%;"></td>
    <td><img src="https://github.com/user-attachments/assets/12a64125-169c-46a8-8a7c-bb4bbecade55f" alt="mill19 1st - gif" style="width: 100%;"></td>
    <td><img src="https://github.com/user-attachments/assets/22e6be11-9a8d-4207-b2ff-4cef3b601b41" alt="go2 navigation - gif" style="width: 100%;"></td>
  </tr>
</table>



The related paper can be found on:

**Zhefan Xu, Xinming Han, Haoyu Shen, Hanyu Jin, and Kenji Shimada, "NavRL: Learning Safe Flight in Dynamic Environments”, IEEE Robotics and Automation Letters (RA-L), 2025.** [\[paper\]](https://arxiv.org/pdf/2409.156346) [\[video\]](https://youtu.be/EbeJW8-YlvI).


## Table of Contents
 - [Training in NVIDIA Isaac Sim](#Training-in-NVIDIA-Isaac-Sim)
 - [NavRL ROS1 Deployment](#NavRL-ROS1-Deployment)
 - [NavRL ROS2 Deployment](#NavRL-ROS1-Deployment)


## Training in NVIDIA Isaac Sim
This section provides the steps for training your own RL agent with the NavRL framework in Isaac Sim.


### Isaac Sim Installation
This project was developed using **Isaac Sim version 2023.1.0-hotfix.1**, released in November 2023. **Please make sure you download and use this exact version, as using a different version may lead to errors due to version incompatibility.** Also, ensure that you have [conda](https://docs.anaconda.com/miniconda/) installed.

If you have already downloaded Isaac Sim version 2023.1.0-hotfix.1, you can skip the following steps. Otherwise, please follow the instructions below to download the legacy version of Isaac Sim, as the official installation does not support legacy version downloads. 

To download Isaac Sim version 2023.1.0-hotfix.1:

a. First, follow the steps on [this link](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_container.html) to complete the Docker Container Setup. 

b. Then, download the Isaac Sim to your docker container:
```
docker pull nvcr.io/nvidia/isaac-sim:2023.1.0-hotfix.1

docker run --name isaac-sim --entrypoint bash -it --runtime=nvidia --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
    -e "PRIVACY_CONSENT=Y" \
    -v ~/docker/isaac-sim/cache/kit:/isaac-sim/kit/cache:rw \
    -v ~/docker/isaac-sim/cache/ov:/root/.cache/ov:rw \
    -v ~/docker/isaac-sim/cache/pip:/root/.cache/pip:rw \
    -v ~/docker/isaac-sim/cache/glcache:/root/.cache/nvidia/GLCache:rw \
    -v ~/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
    -v ~/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
    -v ~/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
    -v ~/docker/isaac-sim/documents:/root/Documents:rw \
    nvcr.io/nvidia/isaac-sim:2023.1.0-hotfix.1
```
c. Move the downloaded Isaac Sim from the docker container to your local machine:
```
bash docker ps # check your container ID in another terminal

# Replace <id_container> with the output from the previous command
docker cp <id_container>:isaac-sim/. /path/to/local/folder # absolute path
```


Isaac Sim version 2023.1.0-hotfix.1 is now installed on your local machine.

### NavRL Training Setup
To set up the NavRL framework, clone the repository and follow these steps (this process may take several minutes):
```
# Set the ISAACSIM_PATH environment variable
echo 'export ISAACSIM_PATH="path/to/isaac_sim-2023.1.0-hotfix.1"' >> ~/.bashrc

cd NavRL/isaac-training
bash setup.sh
```
After the setup completes, you should have created a virtual environment named NavRL.

### Verify Installation and Run a Training Example
Use the default parameter to run a training example with 2 robots to verify installation.

```
# Activate NavRL virtual environment
conda activate NavRL

# Run a training example with default settings
python training/script/train.py
```
If the repo is installed correctly, you should be able to see the Isaac Sim window as shown below: 

![isaac-training-window](https://github.com/user-attachments/assets/14a4d8a8-e607-434f-af9d-42d0d945e8d7)


### Train your own RL agent
The training environment settings and hyerparameters can be found in ```NavRL/isaac-training/training/cfg```.

The following example demonstrates training with 1024 robots, 350 static obstacles, and 80 dynamic obstacles (an RTX 4090 is required). We recommend using [Wandb](https://wandb.ai/site/) to monitor your training and evaluation statistics.
```
python training/script/train.py headless=True env.num_envs=1024 env.num_obstacles=350 \
env_dyn.num_obstacles=80 wandb.mode=online
```
After training for a sufficient amount of time, you should observe the robots learning to avoid collisions:

https://github.com/user-attachments/assets/2294bd94-69b3-4ce8-8e91-0118cfae9bcd



## NavRL ROS1 Deployment
This section demonstrates an example of deploying NavRL with ROS1 and Gazebo using a quadcopter robot. Ensure that your system meets the following requirements:

- Ubuntu 20.04 LTS
- ROS1 Noetic

First, copy the ```ros1``` folder from this repository into your catkin workspace.
```
cp ros1 /path/to/catkin_ws/src
catkin_make
```
Then, set the environment vairable for Gazebo models.
```
echo 'source /path/to/ros1/uav_simulator/gazeboSetup.bash' >> ~/.bashrc
```
Finally, start the simulation and deploy NavRL navigation.
```
# Launch the gazebo simulator
roslaunch uav_simulator start.launch

# Start the perception and safety module
roslaunch navigation_runner safety_and_perception_sim.launch

# Run the navigation node
conda activate NavRL
rosrun navigation_runner navigation_node.py
```
A Gazebo window will display the environment while an RViz window presents the data. Use RViz's ```2D Nav Goal``` tool to set the navigation target, as shown in the video below (note: the default environment and settings might be different from the video):





https://github.com/user-attachments/assets/b7cc7e2e-c01d-4e44-87e3-97271a3aaa0f




To change the environment settings, review the launch file at ```ros1/uav_simulator/launch/start.launch```. The parameters for each module are located in ```ros1/navigation_runner/cfg/*.yaml``` configuration files.


## NavRL ROS2 Deployment











