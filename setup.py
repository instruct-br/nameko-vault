import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nameko-vault",
    version="0.0.1",
    author="Instruct Developers",
    author_email="contato@instruct.com.br",
    description="A Nameko extension to provide connection with Vault",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/instruct-br/nameko-vault",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "hvac>=0.10.3",
        "nameko>=2.2"
    ],
)
