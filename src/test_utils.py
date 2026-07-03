import os
import tempfile
import unittest
from pathlib import Path

from utils import traverse_dir_and_copy_content


class TestTraverseDirAndCopyContent(unittest.TestCase):
    def test_copies_file_from_root(self):
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dest:
            Path(src, "hello.txt").write_text("hello")

            traverse_dir_and_copy_content(src, dest, [])

            self.assertTrue(Path(dest, "hello.txt").exists())
            self.assertEqual(Path(dest, "hello.txt").read_text(), "hello")

    def test_copies_nested_files(self):
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dest:
            os.makedirs(Path(src, "nested", "deep"))
            Path(src, "nested", "a.txt").write_text("a")
            Path(src, "nested", "deep", "b.txt").write_text("b")

            traverse_dir_and_copy_content(src, dest, [])

            self.assertEqual(Path(dest, "nested", "a.txt").read_text(), "a")
            self.assertEqual(Path(dest, "nested", "deep", "b.txt").read_text(), "b")

    def test_skips_directory_symlinks(self):
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dest:
            real_dir = Path(src, "real")
            real_dir.mkdir()
            Path(real_dir, "file.txt").write_text("inside")

            link_dir = Path(src, "link")
            link_dir.symlink_to(real_dir, target_is_directory=True)

            traverse_dir_and_copy_content(src, dest, [])

            self.assertTrue(Path(dest, "real", "file.txt").exists())
            self.assertFalse(Path(dest, "link").exists())
