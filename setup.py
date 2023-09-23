import os
from setuptools import setup

def readme():
    with open('README.txt') as f:
        return f.read()

def data_files():
    data_files = [('', [])]
    for directories in ('images', 'soundeffects', 'data', 'music', 'maps', 'fonts'):
        for directory, _, files in os.walk(directories):
            data_files.append((directory, [os.path.join(directory, filename) for filename in files]))
    return map(lambda (directory, files): (os.path.join('share/lostsky', directory), files), data_files)

setup(name='lostsky',
      version='1.1',
      description='Strategy RPG set in the Touhou universe',
      long_description=readme(),
      url='http://www.featheredmelody.com/',
      author='Fawkes',
      author_email='fawkes@featheredmelody.com',
      license='BSD',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment :: Turn Based Strategy',
      ],
      keywords='lostsky touhou ',
      packages=[
        'lostsky',
        'lostsky.battle',
        'lostsky.bullet_scripts',
        'lostsky.core',
        'lostsky.missions',
        'lostsky.worldmap'
      ],
      data_files=data_files(),
      install_requires=['pygame'],
      scripts=['srpg.py'],
      zip_safe=False)
