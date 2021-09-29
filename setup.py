import sys

from setuptools import setup, find_namespace_packages
from cloudrail.version import __version__

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

project_name = 'cloudrail-knowledge'
with open("README.md", "r") as fh:
    long_description = fh.read()
version = __version__

if "--version" in sys.argv:
    index = sys.argv.index('--version')
    version = sys.argv[index + 1]
    sys.argv.remove("--version")
    sys.argv.remove(version)

setup(
    name=project_name,
    description='Cloudrail\'s package for security rules',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    author='Indeni',
    author_email='engineering@indeni.com',
    url='https://github.com/indeni/cloudrail-knowledge',
    packages=find_namespace_packages(include=['cloudrail.*']),
    package_data={'': ['*.yaml',
                       '*.json']},
    include_package_data=True,
    keywords=['cloud', 'aws', 'azure', 'security', 'rules', 'checks'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Security',
        'Topic :: Software Development :: Build Tools'
    ],
)
