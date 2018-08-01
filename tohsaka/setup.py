import setuptools

with open("..\README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tohsaka",
    version="0.1.0",
    author="Calvin Zhang",
    author_email="ye111111ow@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ye11ow/tohsaka",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        tohsaka=cli:cli
    ''',
)