import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="regolith-helpers", # Replace with your own name
    version="0.0.1",
    author="example author",
    author_email="sb2896@columbia.edu",
    description="A package of helper functions for adding to regolith databases "
                "and generating simple reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/billingegroup/regolith-helpers",
    packages=setuptools.find_packages(),
    package_dir={"regolith-helpers": "regolith-helpers"},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    entry_points={'console_scripts': [
            'regolith-helpers = regolith-helpers.main:main',],
        },
    data_files = [("", ["LICENSE.txt"])],
    python_requires='>=3.7',
    zip_safe=False,
)
