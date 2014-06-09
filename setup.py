from setuptools import setup, find_packages
from pip.req import parse_requirements

setup(name='amqping',
      version=0.2,
      description=('simple package/command for tesitng if an amqp instance is'
                   ' responding'),
      author='Hugh Saunders',
      author_email='hugh@wherenow.org',
      license='MIT',
      packages=find_packages(),
      keywords="amqp rabbitmq ping",
      url="https://github.com/hughsaunders/amqping",
      entry_points={
          'console_scripts': [
              'amqping = amqping:main'
          ]
      },
      install_requires=['pika']
)
