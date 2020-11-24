from setuptools import setup

setup(name='cofea',
      version='0.1',
      description="A CoFEA Initiative project",
      long_description="",
      author='Slawomir Polanski',
      author_email='polanski.slawomir@gmail.com',
      license='TODO',
      packages=['cofea'],
      zip_safe=False,
      install_requires=[
          'collections',
          'jinja2',
          'pprint',
          'pickle',
          'myst_nb',
          ],
      )