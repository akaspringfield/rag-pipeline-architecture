import hashlib

class FileHashService:

    def generate(
        self,
        file_path
    ):

        sha = hashlib.sha256()

        with open(
            file_path,
            "rb"
        ) as f:

            while chunk := f.read(
                8192
            ):
                sha.update(chunk)

        return sha.hexdigest()