from setuptools import setup, find_namespace_packages

setup(
    name='DigiDuck',
    version='0.0.1',
    description='console bot for contacts book, notes and folder sorting by categories',
    #url='https://github.com/SergiyBagmet/Superior_Contact_Crafterl',
    author='Sergey Bagmet',
    author_email='sergey94bagmet@gmail.com',
    license='MIT',
    readme = "README.md",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    install_requires=['markdown'],
    entry_points={'console_scripts': ['duck = DigiDuck.main_bot:main_digi_duck']},
)