from setuptools import setup

setup(
    name='file-client',
    version='0.1',
    py_modules=['file_client'],
    entry_points={
        'console_scripts': [
            'file-client = file_client:main',
        ],
    },
)
