from distutils.core import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='boegel',
    version='0.0.4',
    author="Kenneth Hoste",
    author_email='kenneth.hoste@ugent.be',
    description="Python library to facilitate using GitHub Actions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/boegel/github-actions',
    packages=['actions'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)

