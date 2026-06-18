from setuptools import find_packages, setup

package_name = 'pick_place_cell_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/moveit_joint_goal_demo.launch.py', 'launch/pick_place_demo.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmet',
    maintainer_email='280829604+AhmetEsme@users.noreply.github.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
   entry_points={
    'console_scripts': [
        'moveit_joint_goal_demo = pick_place_cell_demo.moveit_joint_goal_demo:main',
        'pick_place_demo = pick_place_cell_demo.pick_place_demo:main',
    ],
},
)