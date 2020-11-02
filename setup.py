from setuptools import setup

setup(
   name='cofea',
   version='0.1',
   description='A conversion module',
   author='Slawomir Polanski',
   author_email='polanski.slawomir@gmail.com',
   packages=['cofea'],  #same as name
   install_requires=['collections', 'pickle', 'pprint'], #external packages as dependencies
)
