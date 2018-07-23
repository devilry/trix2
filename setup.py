from setuptools import setup, find_packages

execfile('trix/version.py')

setup(
    name='trix',
    description='Next generation Trix. Detailed task control and statistics app for better learning outcome.',
    version=__version__,   # noqa
    url='https://github.com/devilry/trix2',
    author='Tor Johansen, Espen Angell Kristiansen, Jonas Sandbekk',
    author_email='tor@appresso.no, espen@appresso.no, jonassandbekk@gmail.com',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Django>=1.11.0, <2.0.0',
        'django-crispy-forms>=1.7.2',
        'Markdown>=2.6.11',
        'PyYAML>=3.12',
        'django-extensions',
        'dj-database-url>=0.5.0',
        'cradmin_legacy>=1.3.0a0',
        # 'bleach>=2.1.3',
        'gunicorn',
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
