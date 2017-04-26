from setuptools import setup, find_packages

setup(
    name='oresbot',
    version='1.0',
    description='Téléchargement auto depuis le site d\'ORES',
    author='Simon De Greve',
    packages = find_packages(),
    scripts = ['oresbot/download_ores.py'],
    install_requires = [
        'appdirs>=1.4.3',
        'distlib>=0.2.4',
        'future>=0.16.0',
        'packaging>=16.8',
        'pyparsing>=2.2.0', 
        'pypiwin32>=220',
        'selenium>=3.3.3',
        'six>=1.10.0',
    ],
    package_data={
        '':['*.tar.gz'],
        'oresbot':['*.json'],
    }
)