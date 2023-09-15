from setuptools import setup

setup(
    name='DigiDuckBook',
    version='0.0.14',
    packages=[
        "DigiDuckBook", 
        "DigiDuckBook.contacts", 
        "DigiDuckBook.goose_game", 
        "DigiDuckBook.note_book", 
        "DigiDuckBook.sort_folder",
        "DigiDuckBook.utils",
        ],
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
    install_requires=[
        'prompt-toolkit==3.0.39',
        'pygame==2.5.1',
        'wcwidth==0.2.6',
    ],
    include_package_data=True,
    entry_points={'console_scripts': ['duck = DigiDuckBook.main_bot:main_digi_duck']},
)