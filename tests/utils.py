import os
from .config import TEST_DATA_DIRECTORY
from uuid import UUID

def get_test_file_path(file_path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), TEST_DATA_DIRECTORY, file_path)

def is_valid_uuid(uuid_string):
    try:
        UUID(uuid_string, version=4)
        return True
    except ValueError:
        return False
