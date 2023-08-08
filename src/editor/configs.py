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

    @staticmethod
    def light_mode():
        """
        Returns a light mode configuration
        """
        return ModeConfig('Light',
                          'white', 
                          'black',  
                           FontConfig('Inconsolata', 16))

    @staticmethod
    def dark_mode():
        """
        Returns a dark mode configuration
        """
        return ModeConfig('Dark',
                          'black', 
                          'green', 
                           FontConfig('Courier', 16))

    @staticmethod
    def sh_bish_mode():
        """
        Returns a swish bish mode configuration
        """
        return ModeConfig('Swish Bish',
                          'light yellow',
                          'purple',
                           FontConfig('Courier', 16))
