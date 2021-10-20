import os
import shutil
import tempfile
import unittest
import uuid

from cloudrail.knowledge.utils.file_utils import split, join


class TestFileSplitUtils(unittest.TestCase):

    def test_split_file(self):
        dir_name = f'/tmp/test_split_file_{str(uuid.uuid4())}'
        file_to_split = _create_tmp_file_with_size(30)

        split(file_to_split, dir_name, 10)

        self.assertEqual(len(os.listdir(dir_name)), 3)
        files = sorted(os.listdir(dir_name))
        for file in files:
            self.assertEqual(os.path.getsize(os.path.join(dir_name, file)), 10)

        shutil.rmtree(dir_name)
        os.remove(file_to_split)

    def test_split_file_with_remainder(self):
        dir_name = f'/tmp/test_split_file_{str(uuid.uuid4())}'
        file_to_split = _create_tmp_file_with_size(35)

        split(file_to_split, dir_name, 10)

        self.assertEqual(len(os.listdir(dir_name)), 4)
        files = sorted(os.listdir(dir_name))
        for file in files[:3]:
            self.assertEqual(os.path.getsize(os.path.join(dir_name, file)), 10)
        self.assertEqual(os.path.getsize(os.path.join(dir_name, files[-1])), 5)

        shutil.rmtree(dir_name)
        os.remove(file_to_split)

    def test_join_file(self):
        dir_name = f'/tmp/test_split_files_{str(uuid.uuid4())}'
        file_to_split = _create_tmp_file_with_size(30)
        joined_file = f'/tmp/merged_file_{str(uuid.uuid4())}'
        split(file_to_split, dir_name, 10)

        join(dir_name, joined_file, 10)

        self.assertEqual(os.path.getsize(os.path.join(file_to_split)), os.path.getsize(os.path.join(joined_file)))
        self.assertEqual(_get_file_content(file_to_split), _get_file_content(joined_file))

        shutil.rmtree(dir_name)
        os.remove(file_to_split)
        os.remove(joined_file)


def _create_tmp_file_with_size(size_in_bytes: int) -> str:
    tmp_file = tempfile.mkstemp()
    with open(tmp_file[1], 'wb') as file:
        file.write(b'0' * size_in_bytes)
    return tmp_file[1]


def _get_file_content(file_path: str):
    with open(file_path, 'rb') as file:
        return file.readlines()
