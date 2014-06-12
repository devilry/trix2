from setuptools import setup, find_packages

execfile('trix/version.py')

setup(
    name='trix2',
    description='Trix2.',
    version=__version__,
    url='https://gifthub.com/devilry/trix2',
    author='Tor Johansen, Espen Angell Kristiansen',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Django',
        'django-crispy-forms'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
