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
from PyChrDraw.annotation import *
from PyChrDraw.colors import *

if __name__ == '__main__':

    with open("cats_chrs.yaml") as fh:
        settings = yaml.load(fh)

    cat_chrs = settings["chromosome_sizes"]
    cheetah_chrs = settings["cheetah_chrs"]
    cheetah_to_cat = settings["cheetah_to_cat"]
    
    width = settings["canvas"]["width"]
    height = settings["canvas"]["height"]

    cat_snips_file = settings["cat_snips_file"]
    cheetah_snips_file = settings["cheetah_snips_file"]
    wild_cat_snipts_file = settings["wild_cat_snipts_file"]

    cat_to_cheetah = settings["cat_to_cheetah"]

    data_chrs = []
    max_value = 0.
    
    print "Load cats SNPs..."
    cat_chr2bands = load_snips_from_bed(cat_snips_file)
    cheetah_chr2bands = load_snips_from_bed(cheetah_snips_file)
    wild_chr2bands = load_snips_from_bed(wild_cat_snipts_file)
    
    print "Cat..."
    cat_chr2pos2freq, distribution = compute_interval_freq(cat_chr2bands, cat_chrs, bp_per_pixel=100000)
    cat_chr2pos2freq = normalize_interval_freq(cat_chr2pos2freq, distribution, max_cutoff=70)
    cat_bands = freqs_to_bands(cat_chr2pos2freq)

    print "Cheetah"
    ch_chr2pos2freq, distribution = compute_interval_freq(cheetah_chr2bands, cheetah_chrs, bp_per_pixel=100000)
    ch_chr2pos2freq = normalize_interval_freq(ch_chr2pos2freq, distribution, max_cutoff=70)
    ch_bands = freqs_to_bands(ch_chr2pos2freq)

    wild_chr2pos2freq, distribution = compute_interval_freq(wild_chr2bands, cat_chrs, bp_per_pixel=100000)
    wild_chr2pos2freq = normalize_interval_freq(wild_chr2pos2freq, distribution, max_cutoff=70)
    wild_bands = freqs_to_bands(wild_chr2pos2freq)

    x = settings["canvas"]["left_corner"]
    y = settings["canvas"]["top_corner"]
    keys = settings["chromosome_order"]
    real_chr_size = settings["canvas"]["real_chr_size"]
    space_between_chr = settings["canvas"]["space_between_chr"]
    chr_width = settings["canvas"]["chr_width"]

    im = Image.new("RGBA", (width, height), "#ffffff")
    draw = ImageDraw.Draw(im)
    x = settings["canvas"]["left_corner"]
    y = settings["canvas"]["top_corner"]

    cat_ready_chrs, cat_chr2bands = normalize_chromosome_sizes(cat_chrs, real_chr_size, bands=cat_bands)
    ch_ready_chrs, ch_chr2bands = normalize_chromosome_sizes(cheetah_chrs, real_chr_size, bands=ch_bands)
    w_ready_chrs, w_chr2bands = normalize_chromosome_sizes(cat_chrs, real_chr_size, bands=wild_bands)

    for key in keys:
            print key
            length = cat_ready_chrs[key]
            draw_horizontal_chromosome(draw, x, y, length, bands=cat_chr2bands[key], chr_width=chr_width, name=key, scale=1, stars=None)
            y += space_between_chr 

            k = cat_to_cheetah[key]
            length =ch_ready_chrs[k]
            draw_horizontal_chromosome(draw, x, y, length, bands=ch_chr2bands[k], chr_width=chr_width, name=key, scale=1, stars=None)
        
            y += space_between_chr 

            length = cat_ready_chrs[key]
            draw_horizontal_chromosome(draw, x, y, length, bands=w_chr2bands[key], chr_width=chr_width, name=key, scale=1, stars=None)
    

            y += space_between_chr + 20

    im.save("cat_output_file.png")