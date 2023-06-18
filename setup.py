from setuptools import setup
from start import __version__

with open('README.md') as desc:
   desc_md = desc.read()

setup(
        name='rupantar',
        version=__version__,
        description='Easily configurable static website generator with a focus on minimalism.',
        long_description=desc_md,
        long_description_content_type='text/markdown',
        author='bhodrolok',
        author_email='<korbolorbo1214@proton.me>',
        url='https://github.com/bhodrolok/rupantar',
        license='MIT',
        packages=['pidgey'],
        install_requires=[
            'markdown2', 'Jinja2', 'pyyaml',
            ],
        keywords=['python','jinja2','pyyam','markdown2','static','site', 'ssg','minimal'],
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Environment :: Console",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Topic :: Internet",
            "Topic :: Terminals"
            ],
        entry_points={
            'console_scripts': [
                'pidgey= pidgey.pidgey:main',
                ]
            },
)
