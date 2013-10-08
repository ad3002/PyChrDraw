#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

 import Image, ImageDraw, ImageFont

# fix for Windows-specific bug with png extension registering
from PIL.PngImagePlugin import _save, PngImageFile, _accept
Image.register_open("PNG", PngImageFile, _accept)
Image.register_save("PNG", _save)
Image.register_extension("PNG", ".png")
Image.register_mime("PNG", "image/png")
