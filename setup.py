from setuptools import setup, find_packages

with open('trix/version.py') as f:
    code = compile(f.read(), "trix/version.py", 'exec')
    exec(code)

setup(
    name='trix',
    description='Next generation Trix. Detailed task control and statistics app for better'
    ' learning outcome.',
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
        'Django>=3.2.16, <4.0.0',
        'django-crispy-forms<=1.14, >=1.13',
        'Markdown>=3.4.1',
        'PyYAML>=6.0',
        'django-extensions',
        'dj-database-url>=0.5.0',
        'cradmin_legacy>=4.1.2',
        'gunicorn',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
