from dataclasses import dataclass


@dataclass
class FontConfig:
    FONT_SIZE = [8, 34]
    FONT_FAMILY = ['Courier', 
                   'Inconsolata', 
                   'Ubuntu Mono']

    family: str
    size: int


@dataclass
class ModeConfig:
    name: str
    bg: str 
    fg: str
    font_config: FontConfig

    @staticmethod
    def LightMode():
        return ModeConfig('Light', 
                          'white', 
                          'black',  
                           FontConfig('Inconsolata', 16))

    @staticmethod
    def DarkMode():
        return ModeConfig('Dark', 
                          'black', 
                          'green', 
                           FontConfig('Courier', 16))

    @staticmethod
    def ShBishMode():
        return ModeConfig('Swish Bish',  
                          'light yellow',
                          'purple',
                           FontConfig('Courier', 16))
