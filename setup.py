import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="similarweb_scraper",
    version="0.0.3",
    author="Roy Lam",
    author_email="13032765d@connect.polyu.hk",
    description="Using proxycrawl api to scrape similarweb data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/wchan757/similarweb_scraper',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
    )
