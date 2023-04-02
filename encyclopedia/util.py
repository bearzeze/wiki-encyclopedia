import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(word):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None. 
    UPDATE: It will try with the way user typed, capitalized, upper case search before returning None
    """
    for title in [word, word.capitalize(), word.upper()]:
        try:
            f = default_storage.open(f"entries/{title}.md")
            return (f.read().decode("utf-8"), title)
        except FileNotFoundError:
            continue
    else:
        return None, None


def delete_entry(title):
    filename = f"entries/{title}.md"
    default_storage.delete(filename)
