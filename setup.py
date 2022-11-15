# @Project: pyium
# @Author：Lucas Liu
# @Time: 2022/11/15 1:53 PM
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="package-name",
    version="1.0.0",
    author="lucas",
    author_email="ly_liubo@163.com",
    description="page factory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="<LINK_TO_YOUR_CODE_OR_PRODUCT>",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.5"
)
