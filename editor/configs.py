from dataclasses import dataclass


@dataclass
class FontConfig:
    FONT_SIZE = [8, 34]
    FONT_FAMILY = ['Courier', 'Inconsolata', 'Ubuntu Mono']

    def __init__(self, family, size):
        self.family = family
        self.size = size


@dataclass
class ModeConfig:
    def __init__(self, bg, fg, 
                 font_config, name):
        self.name = name
        self.bg = bg
        self.fg = fg
        self.font_config = font_config

    @staticmethod
    def LightMode():
        return ModeConfig('white', 
                          'black', 
                          FontConfig('Inconsolata', 16), 
                          'Light')

    @staticmethod
    def DarkMode():
        return ModeConfig('black', 
                          'green', 
                          FontConfig('Courier', 16), 
                          'Dark')

    @staticmethod
    def ShBishMode():
        return ModeConfig('light yellow', 
                          'purple', 
                          FontConfig('Courier', 16), 
                          'Swish Bish')
