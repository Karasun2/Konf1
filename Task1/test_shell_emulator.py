import pytest
import os
import tarfile
from io import BytesIO

@pytest.fixture
def create_tar():
    tar_buffer = BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
        test_file_1 = BytesIO(b"Line 1\n")
        test_file_2 = BytesIO(b"Content of file 2\n")
        tarinfo1 = tarfile.TarInfo(name='file1.txt')
        tarinfo1.size = len(test_file_1.getvalue())
        tar.addfile(tarinfo1, test_file_1)
        
        tarinfo2 = tarfile.TarInfo(name='dir/file2.txt')
        tarinfo2.size = len(test_file_2.getvalue())
        tar.addfile(tarinfo2, test_file_2)

    tar_buffer.seek(0)
    return tar_buffer.read()

def test_ls(create_tar):
    with open("test.tar", "wb") as f:
        f.write(create_tar)
    from shell_emulator import ShellEmulator
    emulator = ShellEmulator("testhost", "test.tar", "startup.sh")
    emulator.load_filesystem("test.tar")
    emulator.current_path = '/'
    emulator.ls()
    assert "file1.txt\n" in emulator.text_area.get("1.0", "end-1c")
    assert "dir" in emulator.text_area.get("1.0", "end-1c")

def test_cd(create_tar):
    with open("test.tar", "wb") as f:
        f.write(create_tar)
    from shell_emulator import ShellEmulator
    emulator = ShellEmulator("testhost", "test.tar", "startup.sh")
    emulator.load_filesystem("test.tar")
    emulator.current_path = '/'
    emulator.cd("cd dir")
    assert emulator.current_path == "dir"
    emulator.cd("")
    assert emulator.current_path == "/"

def test_head(create_tar):
    with open("test.tar", "wb") as f:
        f.write(create_tar)
    from shell_emulator import ShellEmulator
    emulator = ShellEmulator("testhost", "test.tar", "startup.sh")
    emulator.load_filesystem("test.tar")
    emulator.current_path = '/'
    emulator.head("head file1.txt")
    assert "Line 1" in emulator.text_area.get("1.0", "end-1c")

def test_find(create_tar):
    with open("test.tar", "wb") as f:
        f.write(create_tar)
    from shell_emulator import ShellEmulator
    emulator = ShellEmulator("testhost", "test.tar", "startup.sh")
    emulator.load_filesystem("test.tar")
    emulator.current_path = '/'
    emulator.find("find file1.txt")
    assert "file1.txt" in emulator.text_area.get("1.0", "end-1c")

#def test_exit(create_tar):
 #   with open("test.tar", "wb") as f:
  #      f.write(create_tar)
   # from shell_emulator import ShellEmulator
    #emulator = ShellEmulator("testhost", "test.tar", "startup.sh")
    #emulator.run()
