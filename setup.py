from setuptools import setup

setup(name='aio-dot-proxy',
      version='0.0.1',
      description='A DNS to DNS-over-TLS Proxy',
      url='https://github.com/gilgamezh/aio-dot-proxy',
      author='Gilgamezh',
      author_email='mail@gilgamezh.me',
      license='MIT',
      packages=['aio_dot_proxy'],
      scripts=["bin/dot_proxy"],
      zip_safe=False)
