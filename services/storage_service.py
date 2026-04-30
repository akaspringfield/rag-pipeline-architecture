import shutil
from pathlib import Path
import os
import uuid

class StorageService:

    ORIGINAL_DIR = (
        Path("storage/originals")
    )

    def get_destination(self, file_path):
        original_name = Path(file_path).name
        unique_name = f"{uuid.uuid4()}_{original_name}"
        return Path("storage/originals") / unique_name

    def save(self, file_path):
        dst_path = self.get_destination(file_path)

        # Normalize paths
        src = os.path.abspath(file_path)
        dst = os.path.abspath(dst_path)

        if src == dst:
            return dst  # or just skip copying

        shutil.copy(src, dst)
        return dst

    # def save(
    #     self,
    #     source_file: str
    # ):

    #     self.ORIGINAL_DIR.mkdir(
    #         parents=True,
    #         exist_ok=True
    #     )

    #     source = Path(source_file)

    #     destination = (
    #         self.ORIGINAL_DIR /
    #         source.name
    #     )

    #     shutil.copy(
    #         source,
    #         destination
    #     )

    #     return str(destination)
    
    def delete(
        self,
        file_path: str
    ):

        if os.path.exists(file_path):

            os.remove(file_path)