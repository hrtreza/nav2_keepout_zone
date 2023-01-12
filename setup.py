from setuptools import setup

package_name = 'sofar_assignment'
data_files = []
data_files.append(
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]))
data_files.append(('share/' + package_name + '/launch', [
    'launch/nav_launch.py',
    'launch/slam_launch.py',
    ]))
data_files.append(('share/' + package_name + '/resource', [
    'resource/tiago_webots.urdf',
    'resource/ros2_control.yml',
    'resource/default.rviz',
    'resource/apartment_nav2_params.yaml',
    'resource/apartment_map.pgm',
    'resource/apartment_map.yaml',
    'resource/apartment_keepout_params.yaml',
    'resource/apartment_mask.pgm',
    'resource/apartment_mask.yaml',
    'resource/factory_nav2_params.yaml',
    'resource/factory_map.pgm',
    'resource/factory_map.yaml',
    'resource/factory_keepout_params.yaml',
    'resource/factory_mask.pgm',
    'resource/factory_mask.yaml',
    'resource/factory_keepout_params2.yaml',
    'resource/factory_mask2.pgm',
    'resource/factory_mask2.yaml',
]))
data_files.append(('share/' + package_name, ['package.xml']))
data_files.append(('share/' + package_name + '/worlds', [
    'worlds/apartment.wbt',
    'worlds/factory.wbt'
]))

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ali',
    maintainer_email='aliyousefi98@outlook.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
