from setuptools import setup, find_packages

version = '0.0.1'


setup(
    name='singularity-monitor',
    version=version,
    description='Singularity Monitor',
    url='https://github.com/Nitro/singularity-monitor',
    packages=find_packages(),
    install_requires=["requests", "newrelic"],
    zip_safe=False,
    entry_points="""
    [console_scripts]
    singularity-monitor = sgmon.monitor:main
    """
)
