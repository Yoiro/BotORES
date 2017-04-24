from setuptools import setup

setup(
    name='oresbot',
    version='1.0',
    description='Téléchargement auto depuis le site d\'ORES',
    author='Simon De Greve',
    packages=['webdriver'],
    install_requires=[
        'selenium',
    ]
)