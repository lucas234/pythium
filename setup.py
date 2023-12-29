# @Project: pythium
# @Author：Lucas Liu
# @Time: 2022/11/15 1:53 PM
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pythium",
    version="1.1.3",
    author="lucas",
    author_email="ly_liubo@163.com",
    description="Python based Page Factory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucas234/pythium",
    zip_safe=False,
    license='MIT',
    install_requires=[
        'selenium==4.1',
        'Appium-Python-Client==2.7.1',
        'retrying==1.3.4',
        'requests==2.31.0',
        'allure-python-commons==2.9.43',
        'loguru==0.5.3',
        'webdriver-manager==4.0.0'
    ],
    packages=['pythium'],
    python_requires=">=3",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Software Development :: Testing',
    ],
)
