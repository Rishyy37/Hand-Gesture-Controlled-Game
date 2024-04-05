from setuptools import setup, find_packages

with open('requirements.txt','r') as f:
    requirements = f.read().splitlines()

setup(
    name='my_project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'run-game-server = Game.character:main',
            'run-hand-client = hand_control_client.hand_udp:main',
        ],
    },
)
