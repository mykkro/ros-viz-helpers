import os, json, re, yaml, sys
import unicodedata
import datetime
import random 
import shutil
from itertools import takewhile



# a pure python shingling function that will be used in comparing
# LSH to true Jaccard similarities
def get_shingles(text, char_ngram=5):
    """Create a set of overlapping character n-grams.
    
    Only full length character n-grams are created, that is the first character
    n-gram is the first `char_ngram` characters from text, no padding is applied.

    Each n-gram is spaced exactly one character apart.

    Parameters
    ----------

    text: str
        The string from which the character n-grams are created.

    char_ngram: int (default 5)
        Length of each character n-gram.
    """
    return set(text[head:head + char_ngram] for head in range(0, len(text) - char_ngram))


def jaccard(set_a, set_b):
    """Jaccard similarity of two sets.
    
    The Jaccard similarity is defined as the size of the intersection divided by
    the size of the union of the two sets.

    Parameters
    ---------
    set_a: set
        Set of arbitrary objects.

    set_b: set
        Set of arbitrary objects.
    """
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def flatten(lines):
    """
    Tages a list of lists as input. 
    Returns a flattened list.
    """
    return [item for sublist in lines for item in sublist]




def pick_n(list, n):
    """
    Returns n randomly picked elements from a given list.

    Args:
        list (list): A list of elements from which to randomly choose.
        n (int): The number of elements to pick from the list.

    Returns:
        (list): A list of n randomly selected elements from the input list.
    """
    return [random.choice(list) for i in range(n)]


def get_file_mod_datetime(file):
    """
    Returns the last modification datetime of a file.

    Args:
        file (str): The file path to get the modification datetime of.

    Returns:
        (datetime.datetime): A datetime.datetime object representing the last modification datetime of the input file.
    """
    return datetime.datetime.fromtimestamp(os.path.getmtime(file))
    

def get_file_size(path):
    """
    Returns the size of a file in bytes.

    Args:
        file (str): The file path to get its size of.

    Returns:
        (int): File size,. in bytes.
    """
    file_stats = os.stat(path)
    return file_stats.st_size


def ensure_dir(d):
    """
    Ensures that a given directory exists, creating it if it does not.

    Args:
        d (str): The directory path to ensure exists.

    Returns:
        None
    """
    if not os.path.exists(d):
        os.makedirs(d)


def empty_dir(folder):
    """
    Deletes all files and sub-directories within a given directory.

    Args:
        folder (str): The directory path to empty.

    Returns:
        None
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def save_text(path, txt):
    """
    Writes a given string to a file at the specified path.

    Args:
        path (str): The file path to write the text to.
        txt (str): The text to be written to the file.
    Returns:
        None
    """
    with open(path, "w", encoding="utf-8") as outfile:
        outfile.write(txt)


def load_text(path):
    """
    Loads the contents of a file at the specified path as a string.

    Args:
        path (str): The file path to load the text from.

    Returns:
        (str): The contents of the file as a string.
    """
    with open(path, "r", encoding="utf-8") as infile:
        txt = infile.read()
    return txt


def load_yaml(yaml_path):
    """
    Loads a YAML file from the specified path.

    Args:
        yaml_path (str): The file path to load the YAML file from.

    Returns:
        (dict): A dictionary representing the loaded YAML data.
    """
    with open(yaml_path, "r", encoding="utf-8") as infile:
        return yaml.load(infile, Loader=yaml.FullLoader)


def load_json(path):
    """
    Loads a JSON file from the specified path.

    Args:
        path (str): The file path to load the JSON file from.

    Returns:
        (dict): A dictionary representing the loaded JSON data.
    """
    with open(path, "r", encoding="utf-8") as infile:
        data = json.load(infile)
    return data


def save_json(path, data, ensure_ascii=False, cls=None):
    """
    Writes a given dictionary to a file as JSON at the specified path.

    Args:
        path (str): The file path to write the JSON data to.
        data (dict): The dictionary containing the data to be written as JSON.
        ensure_ascii (bool): If True, all non-ASCII characters in the JSON data will be escaped. Defaults to False.
        cls (Encoder): An optional json.JSONEncoder subclass that will be used to serialize the data. Defaults to None.

    Returns:
        None
    """
    with open(path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=ensure_ascii, cls=cls)


def save_yaml(path, data):
    """
    Writes a given dictionary to a file as YAML at the specified path.

    Args:
        path (str): The file path to write the YAML data to.
        data (dict): The dictionary containing the data to be written as YAML.

    Returns:
        None
    """
    with open(path, 'w', encoding="utf-8") as file:
        yaml.dump(data, file, allow_unicode=True)


def load_cfg(path):
    """
    Loads a configuration file from the specified path, either as JSON or YAML.

    Args:
        path (str): The file path to load the configuration from.

    Returns:
        (dict): A dictionary representing the loaded configuration data.
    
    Raises:
        Exception: If the file format is not supported.
    """
    if path.endswith(".json"):
        return load_json(path)
    elif path.endswith(".yaml"):
        return load_yaml(path)
    else:
        raise Exception(f"Unsupported config format: {path}")


def save_cfg(path, data):
    """
    Writes a given dictionary to a configuration file at the specified path, either as JSON or YAML.

    Args:
        path (str): The file path to write the configuration data to.
        data (dict): The dictionary containing the configuration data to be written.
    """
    if path.endswith(".json"):
        save_json(path, data)
    elif path.endswith(".yaml"):
        save_yaml(path, data)
    else:
        raise Exception(f"Unsupported config format: {path}")


def environ_or_required(key):
    """
    Returns a dictionary with either the default value of an environment variable or a flag indicating it is required.

    Args:
        key (str): The name of the environment variable to check.

    Returns:
        (dict) A dictionary with the 'default' key set to the value of the environment variable, if present,
        otherwise a dictionary with the 'required' key set to True.
    """    
    return (
        {'default': os.environ.get(key)} if os.environ.get(key)
        else {'required': True}
    )


def remove_accents(input_str):
    """
    Removes accents from a string.

    Args:
        input_str (str): The string to remove accents from.

    Returns: 
        (str) A new string with all accents removed.
    """
    nkfd_form = unicodedata.normalize('NFKD', str(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


def get_trailing_number(s):
    """
    Returns the trailing number of a string.

    Args:
        s (str): The string to extract the trailing number from.

    Returns: 
        (int) The trailing number of the input string, or None if there is no trailing number.
    """
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None



def list_replace(arr, fname, fields):
    """
    Replaces an element in the list with the given fields.

    Args:
    - arr: A list of strings.
    - fname: A string indicating the name of the element to be replaced.
    - fields: A list of strings representing the fields to replace the element with.

    Returns:
    - A new list with the specified element replaced by the new fields.
    
    Raises:
    - Exception: If the specified element is not found in the list.
    """
    if fname in arr:
        index = arr.index(fname)
        return arr[:index] + fields + arr[index+1:]
    else:
        raise Exception("Field not found in the array!")


def list_insert_after(arr, fname, fields):
    """
    Inserts a new element into the list after the specified element.

    Args:
    - arr: A list of strings.
    - fname: A string indicating the name of the element after which the new fields are to be inserted.
    - fields: A list of strings representing the new fields to be inserted.

    Returns:
    - A new list with the new fields inserted after the specified element, or the original list if the element is not found.
    """
    if fname in arr:
        index = arr.index(fname)
        return arr[:index+1] + fields + arr[index+1:]
    else:
        return arr + fields


def list_remove(arr, fields):
    """
    Removes the specified elements from the list.

    Args:
    - arr: A list of strings.
    - fields: A list of strings representing the fields to be removed from the list.

    Returns:
    - A new list with the specified fields removed.
    """
    return [x for x in arr if x not in fields]


def parse_date(dt, format="%Y-%m-%d"):
    """
    Parses a string representing a date into a datetime object.

    Args:
    - dt: A string representing the date to be parsed.
    - format: A string representing the expected format of the date string. Default: "%Y-%m-%d"

    Returns:
    - A datetime object representing the parsed date, or None if the input string is empty.
    """
    return datetime.datetime.strptime(dt, format) if dt else None


def format_date(dt, format="%Y-%m-%d"):
    """
    Formats a datetime object into a string.

    Args:
    - dt: A datetime object representing the date to be formatted.
    - format: A string representing the desired format of the output string. Default: "%Y-%m-%d"

    Returns:
    - A string representing the formatted date, or None if the input datetime object is None.
    """
    return datetime.datetime.strftime(dt, format) if dt else None


def endswith_any(txt, suffixes):
    """
    Checks if the input string ends with any of the specified suffixes.

    Args:
    - txt: A string to be checked.
    - suffixes: A list of strings representing the suffixes to be checked against.

    Returns:
    - True if the input string ends with any of the specified suffixes, False otherwise.
    """    
    for suff in suffixes:
        if txt.endswith(suff):
            return True
    return False


def startswith_any(txt, prefixes):
    """
    Checks if the input string starts with any of the specified prefixes.

    Args:
    - txt: A string to be checked.
    - prefixes: A list of strings representing the prefixes to be checked against.

    Returns:
    - True if the input string starts with any of the specified prefixes, False otherwise.
    """
    for pref in prefixes:
        if txt.startswith(pref):
            return True
    return False


def longest_common_prefix(str1, str2):
    """
    Finds the longest common prefix between two strings.

    Args:
    - str1: A string to be compared.
    - str2: A string to be compared.

    Returns:
    - A string representing the longest common prefix between the two input strings.
    """
    return os.path.commonprefix([str1, str2])


# https://stackoverflow.com/questions/6718196/determine-prefix-from-a-set-of-similar-strings
def common_prefix(strings):
    """
    Finds the common prefix among a list of strings.

    Args:
    - strings: A list of strings to be compared.

    Returns:
    - A string representing the common prefix among the input
    """    
    return ''.join(c[0] for c in takewhile(lambda x: all(x[0] == y for y in x), zip(*strings)))


def gen_chunks(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]



def remove_digits(s):
    """
    Takes a string as input.
    Removes digits in a string.
    Returns a string.
    >>> remove_digits('2 recruitment consultants')
    ' recruitment consultants'
    """
    result = ''.join(i for i in s if not i.isdigit())
    return result


select_punct = set('!\'°"#$%&§\()*+,-–./:;<=>?@[\\]^_`{|}~') 

def replace_punctuation(s):
    """
    Takes string as input.
    Removes punctuation from a string if the character is in select_punct.
    Returns a string.
   >>> replace_punctuation('sales executives/ - london')
   'sales executives   london'
    """
    for i in set(select_punct):
        if i in s:
            s = s.replace(i, ' ')
    return s


def split_to_paragraphs(text, breaks_to_split=3):
    """
    Splits the input text into paragraphs based on a specified number of consecutive empty lines.

    Args:
        text (str): The text to be split into paragraphs.
        breaks_to_split (int): The minimum number of consecutive empty lines required to split the text into paragraphs. Default is 3.

    Returns:
        List[str]: A list of paragraphs extracted from the input text.
    """
    out = []
    lines = [l.strip() for l in text.split("\n")]
    # 3 or more spaces(newlines) - new paragraph
    buff = []
    spaces = 0
    for l in lines:
        if l == '': # spaces are
            spaces += 1
        else:
            if spaces >= breaks_to_split:
                out.append("\n".join(buff))
                buff = []
                spaces = 0
            buff.append(l)
    if len(buff) > 0:
        out.append("\n".join(buff))
    return out


def compact_spaces(s):
    """
    Returns a copy of the input string with all consecutive whitespace characters (spaces, tabs, newlines, etc.) replaced by a single space character.

    Args:
        s (str): The input string to be compacted.

    Returns:
        str: The input string with consecutive whitespace characters replaced by a single space character.
    """
    return re.sub('\s+',' ', s)