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
    url="https://github.com/lucas234/pyium",
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X'
    ],
    install_requires=[
        'selenium==3.141.0',
        'Appium-Python-Client==2.7.1',
    ],
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    python_requires=">=3"
)
