"""
Configurations for the editor.
"""

from dataclasses import dataclass


@dataclass
class FontConfig:
    """
    Configuration for the font of the editor.
    """
    FONT_SIZE = [8, 34]
    FONT_FAMILY = ['Courier',
                   'Inconsolata', 
                   'Ubuntu Mono']

    family: str
    size: int


@dataclass
class ModeConfig:
    """
    Configuration for the mode of the editor.
    """
    name: str
    bg: str
    fg: str
    font_config: FontConfig

    @classmethod
    def light_mode(cls) -> "ModeConfig":
        """
        Returns a light mode configuration
        """
        return cls('Light',
                   'white', 
                   'black',  
                    FontConfig('Inconsolata', 16))

    @classmethod
    def dark_mode(cls) -> "ModeConfig":
        """
        Returns a dark mode configuration
        """
        return cls('Dark',
                   'black', 
                   'spring green', 
                    FontConfig('Courier', 16))

    @classmethod
    def sh_bish_mode(cls) -> "ModeConfig":
        """
        Returns a swish bish mode configuration
        """
        return cls('Swish Bish',
                   'light yellow',
                   'purple',
                    FontConfig('Courier', 16))
