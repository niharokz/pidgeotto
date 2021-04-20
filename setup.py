from setuptools import setup
from pidgey import __version__

with open('README.md') as desc:
   desc_md = desc.read()

setup(
        name='pidgeotto',
        version=__version__,
        description='Yet another static blog generator.',
        long_description=desc_md,
        long_description_content_type='text/markdown',
        author='nihar',
        author_email='mail@nihars.com',
        url='https://gitlab.com/niharokz/p',
        license='GPLv3+',
        packages=['pidgey'],
        install_requires=[
            'markdown2', 'Jinja2', 'pyyaml',
            ],
        entry_points={
            'console_scripts': [
                'pidgey= pidgey.pidgey:main',
                ]
            },
)
