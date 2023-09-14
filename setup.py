from setuptools import setup, find_namespace_packages, find_namespace_packages

setup(
    name='DigiDuckBook',
    version='0.0.4',
    packages=find_namespace_packages(),
    package_data={
        'DigiDuckBook.gose_game': ['image/*'],
    },
    description='console bot for contacts book, notes and folder sorting by categories',
    url='https://github.com/SergiyBagmet/DigiDuckBook',
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
    install_requires=[
        'prompt-toolkit==3.0.39',
        'pygame==2.5.1',
        'wcwidth==0.2.6',
    ],
    include_package_data=True,
    entry_points={'console_scripts': ['duck = DigiDuckBook.main_bot:main_digi_duck']},
)