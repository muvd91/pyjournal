import subprocess
import tempfile

class Editor:
    def __init__(self, editor):
        self.editor = editor
        self.file_mode = 'r+'
        self.file_suffix = '.tmp'
        self.file_encoding = 'utf-8'
        self.file = None
        self.args = None
    def execute(self):
        self.file = tempfile.NamedTemporaryFile(mode='r+', suffix=".tmp", encoding="utf-8")
        subprocess.call([self.editor, self.file.name])
        self.file.seek(0)

