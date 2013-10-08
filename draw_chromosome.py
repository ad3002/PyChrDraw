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

def draw_chromosome(draw, x, y, length, bands=None, chr_width=100, name=None, scale=1, stars=None):
    '''
    Draw chromosome
    @param draw: ImageDraw object
    @param x: x coordinate of left top corner
    @param y: y coordinate of left top corner
    @param length: chromosome length
    @param bands: bands list of ideograms
    @param chr_width: chromosome width in px
    @param name: chromosome name
    @param scale: scaling, default value - 1
    @param stars: list of star positions
    '''
    arcbbox = (x, y, x + chr_width, y + chr_width)
    draw.arc(arcbbox, 180, 0, fill='#000000')
    y += chr_width/2
    arcbbox = (x, y + length-chr_width/2, x+chr_width, y + length+chr_width/2)
    draw.arc(arcbbox, 0, 180, fill='#000000')
    rectbbox = [x, y, x + chr_width, y + length]
    draw.rectangle(rectbbox, fill="#ffffff", outline="#000000")
    draw.line((x,y, x+chr_width, y), fill="#ffffff")
    draw.line((x,y + length, x+chr_width, y + length), fill="#ffffff")
    
    if name:
        draw_legend(draw, name, x, y+length+chr_width/2+25, chr_width)
    for band in bands:
        y, length, color, outline = band
        y += chr_width/2
        rectbbox = [x+1, y, x + chr_width-1, y + length]
        draw.rectangle(rectbbox, fill=color, outline=outline)
    if stars:
        for y in stars:
            y += chr_width/2
            draw_legend(draw, "*", x+chr_width+10, y, None, font_size=35)
