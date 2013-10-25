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
from PyChrDraw.colors import *

if __name__ == '__main__':

    with open("human_chrs.yaml") as fh:
        settings = yaml.load(fh)

    chrs = settings["chromosome_sizes"]
    width = settings["canvas"]["width"]
    height = settings["canvas"]["height"]
    im = Image.new("RGBA", (width, height), "#ffffff")
    draw = ImageDraw.Draw(im)


    files = settings["orphans"]
    name2chr = settings["ncbi_names"]
    data_chrs = []
    max_value = 0.
    print "Load files..."
    for file_name in files:
        print "Load", file_name
        chr2bands, _max_value = load_bands_from_bed(file_name, last_column_color=True)
        if _max_value > max_value:
            max_value = float(_max_value)
        new_chr2bands = {}
        for key in chr2bands:
            new_key = key.split("|")[3]
            if new_key in name2chr:
                new_key = name2chr[new_key]
                # print key, "-->", new_key, "Size:", len(bands2chr[key])
                new_chr2bands[new_key] = chr2bands[key]
            else:
                pass
                # print "No key", new_key, "Size", len(bands2chr[key])
        data_chrs.append(new_chr2bands)
        

    x = settings["canvas"]["left_corner"]
    y = settings["canvas"]["top_corner"]
    keys = settings["chromosome_order"]
    real_chr_size = settings["canvas"]["real_chr_size"]
    space_between_chr = settings["canvas"]["space_between_chr"]
    chr_width = settings["canvas"]["chr_width"]

    print "Compute colors..."
    draw_data = []
    for i, chr2bands in enumerate(data_chrs):
        for key in chr2bands:
            for i, (start, length, color, border_color) in enumerate(chr2bands[key]):
                c = get_color_by_map(color/max_value)
                chr2bands[key][i] = (start, length, c, c)
        ready_chrs, chr2bands = normalize_chromosome_sizes(chrs, real_chr_size, bands=chr2bands)
        draw_data.append((ready_chrs, chr2bands))
    

    for i, (ready_chrs, chr2bands) in enumerate(draw_data):
        x = settings["canvas"]["left_corner"]
        y = settings["canvas"]["top_corner"]
        for key in keys:
            length = ready_chrs[key]
            draw_horizontal_chromosome(draw, x, y, length, bands=chr2bands[key], chr_width=chr_width, name=key, scale=1, stars=None)
            y += 75
        im.save("output_file_%s.png" % i)