from src.gradientgenerators import *
from src.colorschemagenerators import *
from src.colormodels import *

rgb = RGB.random_rgb()
print(rgb.output())
print(rgb.to_lab().output())
