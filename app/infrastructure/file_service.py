import os
from uuid import uuid4
from fastapi import UploadFile
import shutil


class UserFileService:
    def __init__(self, base_path: str = "app/infrastructure/storage/avatars"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    async def save_temp_avatar(self, avatar: UploadFile) -> str:
        """
        Guarda el archivo temporalmente con un nombre único.
        """
        ext = os.path.splitext(avatar.filename)[1] or ".jpg"
        filename = f"temp_{uuid4()}{ext}"
        temp_path = os.path.join(self.base_path, filename)

        # Guardar archivo temporalmente
        with open(temp_path, "wb") as f:
            content = await avatar.read()
            f.write(content)

        return temp_path

    async def commit_avatar(self, temp_path: str) -> str:
        """
        Mueve el archivo temporal al nombre final definitivo y devuelve solo el nombre del archivo.
        """
        if not os.path.exists(temp_path):
            raise FileNotFoundError("Archivo temporal no existe")

        ext = os.path.splitext(temp_path)[1]
        final_filename = f"{uuid4()}{ext}"
        final_path = os.path.join(self.base_path, final_filename)

        try:
            shutil.move(temp_path, final_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return final_filename

    async def delete_temp(self, temp_path: str):
        """
        Elimina un archivo temporal si ocurre un error.
        """
        if os.path.exists(temp_path):
            os.remove(temp_path)


class ChampionshipFileService:
    def __init__(self, base_path: str = "app/infrastructure/storage/championships"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    async def save_temp_logo(self, logo: UploadFile) -> str:
        """
        Guarda el archivo temporalmente con un nombre único.
        """
        ext = os.path.splitext(logo.filename)[1] or ".jpg"
        filename = f"temp_{uuid4()}{ext}"
        temp_path = os.path.join(self.base_path, filename)

        with open(temp_path, "wb") as f:
            content = await logo.read()
            f.write(content)

        return temp_path

    async def commit_logo(self, temp_path: str) -> str:
        """
        Mueve el archivo temporal a su ubicación final y devuelve el nombre del archivo.
        """
        if not os.path.exists(temp_path):
            raise FileNotFoundError("Archivo temporal no existe")

        ext = os.path.splitext(temp_path)[1]
        final_filename = f"{uuid4()}{ext}"
        final_path = os.path.join(self.base_path, final_filename)

        try:
            shutil.move(temp_path, final_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return final_filename

    async def delete_temp(self, temp_path: str):
        """
        Elimina un archivo temporal si ocurre un error.
        """
        if os.path.exists(temp_path):
            os.remove(temp_path)


class TeamFileService:
    def __init__(self, base_path: str = "app/infrastructure/storage/teams"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    async def save_temp_logo(self, logo: UploadFile) -> str:
        """
        Guarda el archivo temporalmente con un nombre único.
        """
        ext = os.path.splitext(logo.filename)[1] or ".jpg"
        filename = f"temp_{uuid4()}{ext}"
        temp_path = os.path.join(self.base_path, filename)

        with open(temp_path, "wb") as f:
            content = await logo.read()
            f.write(content)

        return temp_path

    async def commit_logo(self, temp_path: str) -> str:
        """
        Mueve el archivo temporal a su ubicación final y devuelve el nombre del archivo.
        """
        if not os.path.exists(temp_path):
            raise FileNotFoundError("Archivo temporal no existe")

        ext = os.path.splitext(temp_path)[1]
        final_filename = f"{uuid4()}{ext}"
        final_path = os.path.join(self.base_path, final_filename)

        try:
            shutil.move(temp_path, final_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return final_filename

    async def delete_temp(self, temp_path: str):
        """
        Elimina un archivo temporal si ocurre un error.
        """
        if os.path.exists(temp_path):
            os.remove(temp_path)