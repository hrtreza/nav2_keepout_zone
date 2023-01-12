# nav2-keepout-zone
## Introduction
Navigation in ROS2 with [Nav2](https://navigation.ros.org/) introduced a lot of new features and possibilities. The goal of this assignment is to explore and test the new feature of navigating in a known environment while avoiding user-defined “keep out areas”. 

This project was done in 4 steps
1. Creating a custom world .wbt file
2. Mapping the world with `slam_toolbox`
3. Creating a mask filter for the map
4. Using the nav2 package for navigation and path planning with keepout zones

### Package Contents
This package consists of the following directories and files:

```bash
├── launch
│   ├── nav_launch.py
│   └── slam_launch.py
├── package.xml
├── README.md
├── resource
│   ├── apartment_keepout_params.yaml
│   ├── apartment_map.pgm
│   ├── apartment_map.yaml
│   ├── apartment_mask.pgm
│   ├── apartment_mask.yaml
│   ├── apartment_nav2_params.yaml
│   ├── default.rviz
│   ├── factory_keepout_params2.yaml
│   ├── factory_keepout_params.yaml
│   ├── factory_map.pgm
│   ├── factory_map.yaml
│   ├── factory_mask2.pgm
│   ├── factory_mask2.yaml
│   ├── factory_mask.pgm
│   ├── factory_mask.yaml
│   ├── factory_nav2_params.yaml
│   ├── ros2_control.yml
│   ├── sofar_assignment
│   └── tiago_webots.urdf
├── setup.cfg
├── setup.py
├── sofar_assignment
│   └── __init__.py
├── test
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
└── worlds
    ├── apartment.wbt
    └── factory.wbt
```
To describe the above tree, there are 3 main directories:
1. **launch**: There are two launch files, one for mapping the environment `slam_launch.py`, and the other one is used for navigation and path planning `nav_launch.py`
2. **resource**: Each simulation enviroment has a `.yaml` file for its map, keepout filter mask, nav2 params, and keepout params, it has also a `.pgm` file for its map. There is a `.urdf` file containing the TIAGo robot information and a `.yml` file containing the control parameters for this robot.
3. **worlds**: The world files are placed in this directory which end with `.wbt`

and 2 main files:
1. **setup.py**: Every file of the package which is going to be compiled by the builder, has to be mentioned in this file
2. **package.xml**: Consists of the package dependencies 

## Installation
Install the Nav2 and slam packages using your operating system’s package manager:
```bashscript
sudo apt install ros-<ros2-distro>-navigation2
```
```bashscript
sudo apt install ros-<ros2-distro>-nav2-bringup
```
```bashscript
sudo apt install ros-<ros2-distro>-slam-toolbox
```
Add the following command in ~/.bashrc:
```bashscript
source /opt/ros/<ros2-distro>/setup.bash
```
In order to get and build the package use the following commands:
```bashscript
mkdir -p ~/colcon_ws/src
```
```bashscript
cd ~/colcon_ws/src
```
```bashscript
git clone https://github.com/aliy98/nav2_keepout_zone
```
```bashscript
cd ~/colcon_ws
```
```bashscript
colcon build --symlink-install 
```


## Simulation Environment
[Webots R2022a](https://cyberbotics.com/) is an open source robot simulator which is used in this project. There were two environments in which this project was done. The TIAGo robot could be imported into the world files corresponding to these environments by addin `TIAGo Iron` node, whereas customizing the `factory.wbt` world was done using the GUI of the software.
<p align="center">
<img src="https://user-images.githubusercontent.com/65722399/185466540-4e808171-3273-43c7-98ad-ed80c85e6acf.png" width="750" title="factory.wbt">
</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/65722399/185467440-e9446362-7fd0-46d7-b8d4-9022a7313659.png" width="750" title="apartment.wbt">
</p>


## Mapping
There is a launch file called `slam_launch.py` which uses the `online_async_launch.py` from `slam_toolbox` package for mapping the environment. Additionally, in order to improve the performance of the process and also controlling the robot in a more conveient way compared to `teleop_twist_keyboard` package, `navigation_launch.py` from the `nav2_bringup` package, can be used. This would make us able to choose a goal point for the robot while it is mapping the environment.

### Usage and Result
This launch file has also an input argument which is the name of the world `.wbt` file that we are going to create its map. The following commands show how to use this launch file for our custom world file `factory.wbt`.
```bashscript
source ~/colcon_ws/install/setup.bash
```
```bashscript
ros2 launch sofar_assignment slam_launch.py world:=factory.wbt
```
<p align="center">
<img src="https://user-images.githubusercontent.com/65722399/185742159-856566eb-a46c-446f-a68c-87acb6faf338.gif" width="750" title="slam_gif">
</p>

After the process is done, the resultant map can be saved using the following command:
```bashscript
ros2 run nav2_map_server map_saver_cli -f ~/map 
```
Here is the resultant `.pgm` map for `factory.wbt`, which has a corresponding `.yaml` file that contains the information regarding the dimensions and the origin point of mapping:

<p align="center">
<img src="https://user-images.githubusercontent.com/65722399/185742569-983f65d3-cf51-43d8-820e-2f316770a032.jpg" width="250" title="factory_map">
</p>

### Software Architecture for Mapping Part
UML component diagram for SLAM part software architecture can be represented as follows:
<p align="center">
<img src="https://user-images.githubusercontent.com/65722399/185459962-6020855d-06de-482f-91e0-96987bbad8e2.png" width="750" title="nav2_architecture">
</p>
Key: (a) Action - (svc) service - (/) topic

## Navigation and Path Planning
After creating the map of the environment, these filter masks `.pgm` files for keepout zones could be arbitrary created using [GIMP](https://www.gimp.org/) software.

<p align="center">
<img src="https://user-images.githubusercontent.com/65722399/185742840-1554ed47-76be-4f73-99f6-b5cf3bef897f.jpg" width="500" title="factory_map">
</p>

It can be seen that there are also some areas that are less occupied. This matter has been taken into account for providing a safe margin from the obstacles. Each mask `.pgm` file has also a `.yaml` file just like the one the original map `.pgm` has, with a slight difference in the mode of converting the darkness into `OccupancyGrid`. In order to have less occupied areas, the `scale` mode has been chosen which tries to linearly interpolate the darkness of each area into the nearest integer value between 0 and 100.

Each mask has a keepout params `.yaml` file which sets the ros parameters for `costmap_filter_info_server` and `filter_mask_server`. Furthurmore, there is also a nav2 params `.yaml` file for each map, that sets the ros paramters for other main servers of nav2 package such as `planner_server`, `controller_server`and so on. The slight difference in the nav2 params file for each map is in `map_server` ros params that is name if the `.yaml` file for each map. It has to be taken into account that to add `keepout_filter` in the `global_costmap` ros params with the desired values.


### Usage and Result
The launch file provided for this purpose is `nav_launch.py` which takes the following input arguments:
1. world.wbt
2. map.yaml
3. params_file.yaml
4. keepout_params_file.yaml
5. mask.yaml

for each input argument the complete path to the required file has to be decleared except the world.wbt file. An example command for launching the navigation and path planning in the customized `factory.wbt` file with the second keep out filter mask is shown bellow:

```bashscript
ros2 launch sofar_assignment nav_launch.py world:=factory.wbt map:=src/nav2_keepout_zone/resource/factory_map.yaml params_file:=src/nav2_keepout_zone/resource/factory_nav2_params.yaml keepout_params_file:=src/nav2_keepout_zone/resource/factory_keepout_params2.yaml mask:=src/nav2_keepout_zone/resource/factory_mask2.yaml
```

<p align="center">
<img src="https://user-images.githubusercontent.com/65722399/185760890-26d31804-23fd-4c2b-a14f-4066593a31ce.gif" width="750" title="nav_gif">
</p>


### Software Architecture for Navigation and Path Planning Part
UML component diagram for navigation and path planning part software architecture can be represented as follows:
<p align="center">
<img src="https://user-images.githubusercontent.com/65722399/185761739-66de7ca6-3c82-4506-8f13-d27a57394aee.png" width="750" title="nav2_architecture">
</p>
Key: (a) Action - (svc) service - (/) topic


## Resources
1. Mapping Tutorial: https://navigation.ros.org/tutorials/docs/navigation2_with_slam.html
2. Navigating with Keepout Zones Tutorial: https://navigation.ros.org/tutorials/docs/navigation2_with_keepout_filter.html
