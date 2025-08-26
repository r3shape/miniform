import setuptools

version = [0, 1, 0]

setuptools.setup(
    name='miniform',
    version=f"{version[0]}.{version[1]}.{version[2]}",
    description='A neat little thing... with nightly updates',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Izaiyah Stokes',
    author_email='zafflins@gmail.com',
    url='https://github.com/r3shape/miniform',
    packages=setuptools.find_packages(),
    #entry_points={
    #    "console_scripts": []
    #},
    install_requires=[
        'pygame-ce'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ], include_package_data=True
)
