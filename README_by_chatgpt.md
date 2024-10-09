# PWImageDataset 

## Overview 
`PWImageDataset` is a Python project designed to handle image datasets, including functionality for compressing them into password-protected archives. This project simplifies creating secure datasets, archiving them in both `.zip` and `.7z` formats, and offers additional utilities to interact with and test image datasets.
## Features 
 
- **Password-protected archiving** : Automatically compress images into either `.zip` or `.7z` formats with a specified password.
 
- **Image management** : Organize and handle image datasets programmatically.
 
- **Customizable** : Easily modify or extend the provided scripts for specific dataset management needs.

## Project Structure 
 
- **`pw_imagedataset.py`** : Core Python script that contains the logic for handling image datasets and archiving them securely.
 
- **`sample_pw_imagedataset.py`** : A sample script demonstrating how to use the `pw_imagedataset.py` module.
 
- **`tests/`** : Unit tests for ensuring the functionality of the project.
 
- **`images/`** : Placeholder folder for storing images. You can add your own dataset here.
 
- **`.gitignore`** : Specifies files and directories that should be ignored by Git.
 
- **`README.md`** : Project documentation.

## Usage 

### 1. Archiving Images with a Password 
To create a password-protected archive of the `images/` directory, you can use the following commands:
#### ZIP Archive 


```bash
zip -e --password=YOUR_PASSWORD images.zip images/*
```

#### 7Z Archive 


```bash
7z a -mx=1 -pYOUR_PASSWORD images.7z images/*
```
Replace `YOUR_PASSWORD` with the desired password.
### 2. Sample Script 
The `sample_pw_imagedataset.py` provides an example of how to use the core functions from `pw_imagedataset.py`. You can modify it to fit your specific needs. To run the script:

```bash
python sample_pw_imagedataset.py
```

### 3. Running Tests 

Ensure that your environment is set up correctly before running tests. You can execute the tests using:


```bash
python -m unittest discover tests
```
This will automatically discover and run all unit tests within the `tests/` directory.
## Requirements 

- Python 3.x
 
- Required Python packages are listed in `requirements.txt` (if available). You can install them with:


```bash
pip install -r requirements.txt
```

## Contributing 

Feel free to contribute to this project by forking the repository, creating a new branch, and submitting a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License 
This project is licensed under the MIT License. See the `LICENSE` file for details.

