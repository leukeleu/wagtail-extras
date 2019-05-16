import io

from setuptools import find_packages, setup

setup(
    name='wagtail-extras',
    version='0.2.5',
    description='A collection of tools one might use to make wagtail even better',
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    keywords=['wagtail', 'extra',],
    author='Ramon de Jezus (Leukeleu)',
    author_email='rdejezus@leukeleu.nl',
    maintainer='Leukeleu',
    maintainer_email='info@leukeleu.nl',
    url='https://github.com/leukeleu/wagtail-extras',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='MIT',
    install_requires=[
        'wagtail',
    ],
    include_package_data=True,
    zip_safe=False
)
