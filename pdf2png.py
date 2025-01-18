#!/usr/bin/env python3

from pdf2image import convert_from_path
import sys
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = 1000000000

pages = convert_from_path(sys.argv[1], 1200)
chr = 1
for page in pages:
	page.save('%s/%s_chr%s.png' % (os.path.dirname(os.path.abspath(sys.argv[1])), 
	os.path.basename(sys.argv[1]).split(".")[0], chr))
	chr += 1
