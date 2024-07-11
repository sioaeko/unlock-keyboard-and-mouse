#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# >>> TABLE OF CONTENTS:
# ------------------------------------------------------------------------------
# 1.0 Import modules
# 2.0 Utility functions
#   2.1 Lower camel case
#   2.2 Get list of files
#   2.3 Safe JSON operations
# 3.0 Localization operations
#   3.1 Add item
#   3.2 Remove item
#   3.3 Change key
#   3.4 Decode characters
# 4.0 Upgrade function
# 5.0 Main function
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1.0 IMPORT MODULES
# ------------------------------------------------------------------------------

import io
import json
import os
import pathlib
import re
import sys
from typing import List, Dict, Any

# ------------------------------------------------------------------------------
# 2.0 UTILITY FUNCTIONS
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2.1 LOWER CAMEL CASE
# ------------------------------------------------------------------------------

def lowerCamelCase(string: str) -> str:
    """
    Convert a string to lower camel case.
    
    Args:
        string (str): The input string to convert.
    
    Returns:
        str: The string in lower camel case format.
    """
    string = re.sub(r"(-|_)+", ' ', string).title()
    return ''.join(char.lower() if i == 0 else char for i, char in enumerate(string) if char.isalnum())

# ------------------------------------------------------------------------------
# 2.2 GET LIST OF FILES
# ------------------------------------------------------------------------------

def getListOfFiles(path: str) -> List[str]:
    """
    Recursively get a list of all files in a directory.
    
    Args:
        path (str): The directory path to search.
    
    Returns:
        List[str]: A list of file paths.
    """
    allFiles = []
    for root, _, files in os.walk(path):
        allFiles.extend(os.path.join(root, file) for file in files)
    return allFiles

# ------------------------------------------------------------------------------
# 2.3 SAFE JSON OPERATIONS
# ------------------------------------------------------------------------------

def safeJsonLoad(file_path: str) -> Dict[str, Any]:
    """
    Safely load a JSON file, handling potential errors.
    
    Args:
        file_path (str): The path to the JSON file.
    
    Returns:
        Dict[str, Any]: The loaded JSON data, or an empty dict if there was an error.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
        return {}

def safeJsonDump(data: Dict[str, Any], file_path: str) -> None:
    """
    Safely write data to a JSON file.
    
    Args:
        data (Dict[str, Any]): The data to write.
        file_path (str): The path to the JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4, sort_keys=True)

# ------------------------------------------------------------------------------
# 3.0 LOCALIZATION OPERATIONS
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3.1 ADD ITEM
# ------------------------------------------------------------------------------

def addItem(allFiles: List[str]) -> None:
    """
    Add a new localization item to all language files.
    
    Args:
        allFiles (List[str]): List of all localization file paths.
    """
    message = input('Enter your message: ')
    camelized_message = lowerCamelCase(message)

    for file_path in allFiles:
        data = safeJsonLoad(file_path)
        if camelized_message not in data:
            data[camelized_message] = {'message': message}
        safeJsonDump(data, file_path)

# ------------------------------------------------------------------------------
# 3.2 REMOVE ITEM
# ------------------------------------------------------------------------------

def removeItem(allFiles: List[str]) -> None:
    """
    Remove a localization item from all language files.
    
    Args:
        allFiles (List[str]): List of all localization file paths.
    """
    key = input('Enter your key (lowerCamelCase): ')
    for file_path in allFiles:
        data = safeJsonLoad(file_path)
        if key in data:
            del data[key]
            safeJsonDump(data, file_path)

# ------------------------------------------------------------------------------
# 3.3 CHANGE KEY
# ------------------------------------------------------------------------------

def changeKey(allFiles: List[str]) -> None:
    """
    Change a key in all localization files.
    
    Args:
        allFiles (List[str]): List of all localization file paths.
    """
    old_key = input('Enter key: ')
    new_key = input('Enter new key: ')
    for file_path in allFiles:
        data = safeJsonLoad(file_path)
        if old_key in data:
            data[new_key] = data.pop(old_key)
            safeJsonDump(data, file_path)

# ------------------------------------------------------------------------------
# 3.4 DECODE CHARACTERS
# ------------------------------------------------------------------------------

def decodeCharacters(allFiles: List[str]) -> None:
    """
    Decode characters in all localization files.
    
    Args:
        allFiles (List[str]): List of all localization file paths.
    """
    for file_path in allFiles:
        data = safeJsonLoad(file_path)
        safeJsonDump(data, file_path)

# ------------------------------------------------------------------------------
# 4.0 UPGRADE FUNCTION
# ------------------------------------------------------------------------------

def upgrade() -> None:
    """
    Upgrade localization files, ensuring all languages have all keys.
    """
    locales = ['am', 'ar', 'bg', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fil', 'fr', 'gu', 'he', 'hi', 'hin', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'ml', 'mr', 'ms', 'nb_NO', 'nl', 'no', 'pl', 'pt_BR', 'pt_PT', 'ro', 'ru', 'sk', 'sl', 'sr', 'sv', 'sw', 'ta', 'te', 'th', 'tr', 'uk', 'vi', 'zh_CN', 'zh_TW']

    default_locale_path = '../_locales/en/messages.json'
    default_locale = safeJsonLoad(default_locale_path) if os.path.exists(default_locale_path) else {}

    for locale in locales:
        path = f'../_locales/{locale}'
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        locale_file_path = f'{path}/messages.json'

        if not os.path.exists(locale_file_path):
            safeJsonDump(default_locale, locale_file_path)
        else:
            data = safeJsonLoad(locale_file_path)
            data.update({k: v for k, v in default_locale.items() if k not in data})
            safeJsonDump(data, locale_file_path)

# ------------------------------------------------------------------------------
# 5.0 MAIN FUNCTION
# ------------------------------------------------------------------------------

def main() -> None:
    """
    Main function to handle command-line arguments and execute corresponding actions.
    """
    if not os.path.exists('../_locales/'):
        pathlib.Path('../_locales/').mkdir(parents=True, exist_ok=True)

    allFiles = getListOfFiles('../_locales/')

    actions = {
        '-add': lambda: addItem(allFiles),
        '-remove': lambda: removeItem(allFiles),
        '-decode': lambda: decodeCharacters(allFiles),
        '-change-key': lambda: changeKey(allFiles),
        '-upgrade': upgrade
    }

    for arg in sys.argv[1:]:
        if arg in actions:
            actions[arg]()

if __name__ == "__main__":
    main()
