"""Username Generator.

At the start of the project, it loads adjectives and nouns from text files and stores them in tuples. When generate_username is called, it combines these words into a username with the addition of a short GUID.
"""

import os
import random
import uuid

from django.conf import settings

keywords_path = os.path.join(settings.BASE_DIR, "app", "fixtures", "username_keywords")
adjectives_path = os.path.join(keywords_path, "adjectives.txt")
nouns_path = os.path.join(keywords_path, "nouns.txt")

with open(adjectives_path, "r") as file_adjective:
    adjectives = tuple(line.strip() for line in file_adjective)

with open(nouns_path, "r") as file_noun:
    nouns = tuple(line.strip() for line in file_noun)


def generate_username() -> str:
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    short_uuid = str(uuid.uuid4())[:6]

    return f"{adjective}-{noun}-{short_uuid}"


__all__ = ["generate_username"]
