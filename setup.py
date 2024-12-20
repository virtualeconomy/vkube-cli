from setuptools import setup,find_packages
setup(
    name = "vkube-cli",
    version = "0.0.1",
    description='Vkube-Cli User-End',
    long_description=README,
    author='certram',
    author_email='@v.systems',
    install_requires = ['Click']
    license='MIT',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3,6'
)