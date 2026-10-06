from dataclasses import dataclass
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Final


""" A constant for the localhost IP address """
LOCAL_HOST_IP: Final = "127.0.0.1"

""" A constant for the ALL IP address """
ALL_IP: Final = "0.0.0.0"

class CameraType(Enum):
    """The types of camera applications that could be used."""

    TEST = 1
    OPENCV = 2

    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str):
            return cls.__members__.get(value.upper())
        return None


@dataclass
class CameraConfig:
    camera_type: CameraType
    """ Which camera is being used. """

    camera_name: str
    """ The name of the camera to give to OpenCV. This could be a camera index or a network camera URL. """
    
    local_display: bool = False
    """ Should the video stream be displayed locally for testing """

    last_detection_valid_secs: float = 30.0
    """ How long should the last detected item be ignored? Effectively a debounce from triggering on the same item for 30 seconds """

@dataclass
class HomeAssistantConfig:
    """ Configurations values for home assistant """
    
    token: str
    """ The long lived token assigned to this application """

    url: str
    """ The URL of the home assistant instance. """

class Settings(BaseSettings):
    """ The application settings object """

    accept_external_traffic: bool
    """ Accept external traffic or rather which IP address the application should listen on. """

    port: int
    """ The port to listen on """

    camera_config: CameraConfig
    """ Configuration values for the camera system """

    ha_config: HomeAssistantConfig
    """ Configuration values for interacting with Home Assistant """

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")