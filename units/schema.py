from units import __version__
from pydantic import BaseModel


class VersionResponse(BaseModel):
    """Version response object."""

    version: str = __version__
