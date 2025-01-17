import typing as t

from jinja2 import Environment, FileSystemLoader
# from pydantic import BaseSettings as Settings
# from pydantic import DirectoryPath, EmailStr, validator
from pydantic_settings import BaseSettings as Settings
from pydantic import EmailStr, field_validator, DirectoryPath


class ConnectionConfig(Settings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_BACKEND: t.Optional[str] = None
    MAIL_SERVER: str
    MAIL_PORT: int = 25
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = True
    MAIL_DEFAULT_SENDER: t.Optional[EmailStr] = None
    TEMPLATE_FOLDER: t.Optional[DirectoryPath] = None
    MAIL_SSL_KEYFILE: t.Optional[str] = None
    MAIL_SSL_CERTFILE: t.Optional[str] = None
    MAIL_USE_LOCALTIME: bool = False
    MAIL_FILE_PATH: t.Optional[str] = None
    MAIL_TIMEOUT: t.Optional[int] = None
    MAIL_DEFAULT_CHARSET: str = 'utf-8'

    def template_engine(self) -> Environment:
        """Return template environment."""
        folder = self.TEMPLATE_FOLDER
        if not folder:
            raise ValueError('Class initialization did not include a ``TEMPLATE_FOLDER`` ``PathLike`` object.')
        return Environment(loader=FileSystemLoader(folder))

    # @field_validator('MAIL_DEFAULT_SENDER')
    # @classmethod
    # def mail_default_sender(cls, v : str, *wargs, **kwargs):
    #     # if cls.MAIL_DEFAULT_SENDER is None:
    #         # return cls.MAIL_USERNAME

    #     return cls.MAIL_DEFAULT_SENDER or cls.MAIL_USERNAME

    @field_validator('MAIL_BACKEND')
    @classmethod
    def mail_backend(cls, v : str, *wargs, **kwargs):
        return v or 'smtp'
        if cls.MAIL_BACKEND is None:
            return 'smtp'

        return cls.MAIL_BACKEND