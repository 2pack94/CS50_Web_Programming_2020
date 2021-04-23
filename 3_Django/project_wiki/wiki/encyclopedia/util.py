import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

ENTRIES_DIR = "entries"

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir(ENTRIES_DIR)
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def get_entry_name(title):
    """
    return the name of an encyclopedia entry if it matches "title" case insensitively
    else return None
    """
    entry_name = None
    _, filenames = default_storage.listdir(ENTRIES_DIR)
    for filename in filenames:
        if f"{title.lower()}.md" == filename.lower():
            entry_name = re.sub(r"\.md$", "", filename)
            break
    return entry_name

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    entry_name = get_entry_name(title)
    if entry_name:
        default_storage.delete(f"{ENTRIES_DIR}/{entry_name}.md")

    filename = f"{ENTRIES_DIR}/{title}.md"
    default_storage.save(filename, ContentFile(content))

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"{ENTRIES_DIR}/{get_entry_name(title)}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
