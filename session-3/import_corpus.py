import json
import os
import re
from nltk.tokenize import wordpunct_tokenize

def import_corpus(corpus_path = 'texts', manifest_file = 'manifest.json'):
    """
    Imports a corpus of texts and prepares them for text analysis.

    params:
        corpus_path: a file path to a folder of .txt files with a .json manifest
        manifest_file: the path of the .json manifest file

    returns:
        novels: a list of dicts, each of which represents a novel
    """

    # Import manifest file
    with open(corpus_path + "/" + manifest_file, 'r') as file:
        manifest = json.load(file)

    # Create list of all files other than the manifest file
    file_list = os.listdir(corpus_path)
    file_list = [file for file in file_list if file != manifest_file]

    # Create useful regular expressions
    header_regex = re.compile('\A.+\*{3} {0,2}START OF.{,200}\*{3}', flags = re.DOTALL)
    licence_regex = re.compile('\*{3} {0,2}END OF.+', flags = re.DOTALL)

    # Instantiate novel list
    novels = []

    # Loop over files, import and tokenise novels
    for file in file_list:

        # Initialise novel dict
        novel = {}

        # Fetch metadata from manifest
        novel['title'] = manifest[file]['title']
        novel['author'] = manifest[file]['author']

        # Construct full path
        full_path = corpus_path + '/' + file

        # Load text
        with open(full_path, 'r') as file:
            text = file.read()

        # Extract header, footer
        novel['header'] = header_regex.search(text).group()
        novel['licence'] = licence_regex.search(text).group()

        # Delete header and licence, then add text body to novel dict
        text = header_regex.sub('', text)
        text = licence_regex.sub('', text)
        novel['body'] = text

        # Tokenise text
        tokens = wordpunct_tokenize(text) # apply tokeniser
        # strip out punctuation and single-character strings other than 'a','A','i' or 'I':
        tokens = [token for token in tokens if re.match('^\w{2,}$|^[aAiI0-9]$', token)] 
        novel['tokens'] = tokens

        # Output message
        print(f'{novel["title"]}, by {novel["author"]} successfully imported.')

        # Add to master list
        novels.append(novel)

    return novels
