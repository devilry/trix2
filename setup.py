from setuptools import setup, find_packages

execfile('trix/version.py')

setup(
    name='trix',
    description='Trix.',
    version=__version__,   # noqa
    url='https://gifthub.com/devilry/trix2',
    author='Tor Johansen, Espen Angell Kristiansen',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Django>=1.6.5, <1.7.0',
        'django-crispy-forms>=1.4.0',
        'Markdown>=2.4',
        'PyYAML>=3.11',
        'django-extensions',
        'South>=0.8.4',
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
