#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 28-04-2025
#       SOURCE [setup.py] LAST MODIFIED ON 28-04-2025.
#

from setuptools import setup
from rynz import __version__

with open('README.md', encoding='utf-8') as desc:
    desc_md = desc.read()

setup(
    name='rynz',
    version=__version__,
    description='A minimal, fast static site generator built for Markdown lovers.',
    long_description=desc_md,
    long_description_content_type='text/markdown',
    author='Nihar',
    author_email='hi@nihars.com', 
    url='https://gitlab.com/niharokz/rynz',
    license='MIT',
    packages=['rynz'],
    install_requires=[
        'markdown2', 'Jinja2', 'pyyaml', 'rich',
    ],
    keywords=['python', 'static site generator', 'markdown', 'Jinja2', 'pyyaml'],
    classifiers=[
        "Development Status :: 5 - Production/Stable", 
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'rynz = rynz.rynz:main',
        ],
    },
)
