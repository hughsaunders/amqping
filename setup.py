from setuptools import setup, find_packages
from pip.req import parse_requirements

setup(name='amqping',
      version=0.4,
      description=('simple package/command for tesitng if an amqp instance is'
                   ' responding'),
      author='Hugh Saunders',
      author_email='hugh@wherenow.org',
      license='Apache',
      packages=find_packages(),
      keywords="amqp rabbitmq ping",
      url="https://github.com/hughsaunders/amqping",
      install_requires=[
          'Click',
          'pika',
      ],
      entry_points={
          'console_scripts': [
              'amqping = amqping:cli'
          ]
      },
)
