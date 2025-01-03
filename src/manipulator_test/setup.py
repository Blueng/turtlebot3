from setuptools import find_packages, setup

package_name = 'manipulator_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='phb',
    maintainer_email='bin000120@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtlebot3_controller = manipulator_test.turtlebot3_cnt_test:main',
            '2d_map = manipulator_test.2d_map:main',
            'aruco_tracking = manipulator_test.cnt_test:main',
        ],
    },
)
