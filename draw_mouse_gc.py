#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
sys.path.append("c:/Users/Master/Dropbox/workspace")
sys.path.append("/Users/akomissarov/Dropbox/workspace")
import Image, ImageDraw, ImageFont
import yaml

# fix for Windows-specific bug with png extension registering
from PIL.PngImagePlugin import _save, PngImageFile, _accept
Image.register_open("PNG", PngImageFile, _accept)
Image.register_save("PNG", _save)
Image.register_extension("PNG", ".png")
Image.register_mime("PNG", "image/png")

from PyChrDraw.draw_chromosome import *

if __name__ == '__main__':

	with open("mouse_chrs.yaml") as fh:
		settings = yaml.load(fh)

	mouse_chrs = settings["chromosome_sizes"]
	width = settings["canvas"]["width"]
	height = settings["canvas"]["height"]
	im = Image.new("RGBA", (width, height), "#ffffff")
	draw = ImageDraw.Draw(im)


	file_name = '/Users/akomissarov/Downloads/polyG_Mus.bed'
	bands2chr = load_bands_from_bed(file_name)

	
	x = settings["canvas"]["left_corner"]
	y = settings["canvas"]["top_corner"]
	keys = settings["chromosome_order"]
	real_chr_size = settings["canvas"]["real_chr_size"]
	space_between_chr = settings["canvas"]["space_between_chr"]
	chr_width = settings["canvas"]["chr_width"]

	mouse_chrs, bands2chr = normalize_chromosome_sizes(mouse_chrs, real_chr_size, bands=bands2chr)

	for key in keys:
		length = mouse_chrs[key]
		draw_horizontal_chromosome(draw, x, y, length, bands=bands2chr[key], chr_width=chr_width, name=key, scale=1, stars=None)
		y += space_between_chr
	im.save("output_file.png")