from setuptools import setup, find_packages

setup(
    name="disk_cache",
    version="0.1.0",
    description="A Python library for disk-based function caching",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Krzysztof Ostrowski",
    author_email="krzysztofostrowski2001@gmail.com",
    url="https://github.com/twoje-konto/disk_cache",
    license="MIT",
    packages=find_packages(),
    install_requires=["numpy", "pandas"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)