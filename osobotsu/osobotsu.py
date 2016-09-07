#!/usr/bin/env python
"""
osobotsu.py - A comic generator
"""

import os
import random
import argparse
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser(description='Hustle, hustle!  Muscle, muscle!')
parser.add_argument('-c', '--character', help='Specify a character name', required=False)
parser.add_argument('-l', '--list', help='List all character images', action='store_true', required=False)
parser.add_argument('-s', '--save', help='Generate and save an image', action='store_true', required=False)
args = parser.parse_args()

def comic():
    chars = ('ichimatsu', 'osomatsu')

    panels = []
    panel = []

    panel.append(('ichimatsu', 'knock knock'))
    panels.append(panel)
    panel = []

    panel.append(('osomatsu', 'who is there?'))
    panels.append(panel)
    panel = []

    panel.append(('ichimatsu', 'fuck you'))
    panels.append(panel)

    print(repr(chars))
    print(repr(panels))

    # Save the completed composition to a JPG on disk
    fname = ''.join([random.choice("fartpoo42069") for i in range(16)]) + ".jpg"
    make_comic(chars, panels).save(('output/' + fname), quality=85)

    # Return link to private URL location
    return 'output/' + fname

def wrap(st, font, draw, width):
    st = st.split()
    mw = 0
    mh = 0
    ret = []

    while len(st) > 0:
        s = 1
        while True and s < len(st):
            w, h = draw.textsize(" ".join(st[:s]), font=font)
            if w > width:
                s -= 1
                break
            else:
                s += 1

        if s == 0 and len(st) > 0:  # we've hit a case where the current line is wider than the screen
            s = 1

        w, h = draw.textsize(" ".join(st[:s]), font=font)
        mw = max(mw, w)
        mh += h
        ret.append(" ".join(st[:s]))
        st = st[s:]

    return ret, (mw, mh)


def rendertext(st, font, draw, pos):
    ch = pos[1]
    for s in st:
        w, h = draw.textsize(s, font=font)
        draw.text((pos[0], ch), s, font=font, fill=(0xff, 0xff, 0xff, 0xff))
        ch += h


def fitimg(img, width, height):
    scale1 = float(width) / img.size[0]
    scale2 = float(height) / img.size[1]

    l1 = (img.size[0] * scale1, img.size[1] * scale1)
    l2 = (img.size[0] * scale2, img.size[1] * scale2)

    if l1[0] > width or l1[1] > height:
        l = l2
    else:
        l = l1

    return img.resize((int(l[0]), int(l[1])), Image.ANTIALIAS)


def make_comic(chars, panels):
    panelheight = 720
    panelwidth = 1280

    chars = list(chars)
    filenames = list(('chars/ichimatsu.png', 'chars/osomatsu.png', 'chars/ichimatsu.png'))
    chars = zip(chars, filenames)
    charmap = dict()
    for ch, f in chars:
        charmap[ch] = Image.open(f)

    imgwidth = panelwidth
    imgheight = panelheight * len(panels)

    bg = Image.open('scenes/fishpond.jpg')

    im = Image.new("RGBA", (imgwidth, imgheight), (0xff, 0xff, 0xff, 0xff))
    font = ImageFont.truetype('fonts/ComicBD.ttf', 14)

    for i in range(len(panels)):
        pim = Image.new("RGBA", (panelwidth, panelheight), (0xff, 0xff, 0xff, 0xff))
        pim.paste(bg, (0, 0))
        draw = ImageDraw.Draw(pim)

        st1w = 0; st1h = 0; st2w = 0; st2h = 0
        (st1, (st1w, st1h)) = wrap(panels[i][0][1], font, draw, 2*panelwidth/3.0)
        rendertext(st1, font, draw, (10, 10))
        if len(panels[i]) == 2:
            (st2, (st2w, st2h)) = wrap(panels[i][1][1], font, draw, 2*panelwidth/3.0)
            rendertext(st2, font, draw, (panelwidth-10-st2w, st1h + 10))

        texth = st1h + 10
        if st2h > 0:
            texth += st2h + 10 + 5

        maxch = panelheight - texth
        im1 = fitimg(charmap[panels[i][0][0]], 2*panelwidth/5.0-10, maxch)
        pim.paste(im1, (10, panelheight-im1.size[1]), im1)

        if len(panels[i]) == 2:
            im2 = fitimg(charmap[panels[i][1][0]], 2*panelwidth/5.0-10, maxch)
            im2 = im2.transpose(Image.FLIP_LEFT_RIGHT)
            pim.paste(im2, (panelwidth-im2.size[0]-10, panelheight-im2.size[1]), im2)

        draw.line([(0, 0), (0, panelheight-1), (panelwidth-1, panelheight-1), (panelwidth-1, 0), (0, 0)], (0, 0, 0, 0xff))
        del draw
        im.paste(pim, (0, panelheight * i))

    return im



if args.character:
    print("Searching for character: ")
    if os.path.isfile("./chars/" + args.character + ".png"):
        character = "Found character " + args.character + ".png"
    else:
        character = "Sorry, could not find " + args.character
else:
    # pick a random character
    print("No character specified, choosing random: ")
    character = random.choice(os.listdir("chars/"))

print(character)

if args.list:
    for image in os.listdir("chars/"):
        im = Image.open("chars/" + image)
        print(im.size)

if args.save:
    print(comic())

#TODO normalize character images to identical dimensions
#TODO crop background out of character images