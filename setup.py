from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="picture2avatar",
    version="1.1.1",
    author="Thomas Cluzel",
    author_email="thomas.cluzel@etu.uca.fr",
    description="A small package to perform some image processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/ThomasCluzel/picture2avatar.git",
    project_urls={
        'Source': 'https://github.com/ThomasCluzel/picture2avatar.git'
    },
    py_modules=["picture2avatar"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="picture avatar image",
    install_requires=["pillow>=6.0.0"],
    python_requires='>=3',
    entry_points = {
        'gui_scripts': ['picture2avatar = guipicture2avatar:gui']
    },
    data_files=[('', ['guipicture2avatar.pyw'])]
)
