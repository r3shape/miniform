import setuptools

version = [2025, 0, 4]
setuptools.setup(
    name='NIGHTBOX',
    version=f'{version[0]}.{version[1]}.{version[2]}',
    description='Reach Inside The Box...',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Izaiyah Stokes',
    author_email='d34d0s.dev@gmail.com',
    url='https://github.com/r3shape/BLAKBOX',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame-ce'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ]
)