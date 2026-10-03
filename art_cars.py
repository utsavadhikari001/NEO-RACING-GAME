"""Optional asset generator: regenerate the six antialiased rear-view car PNGs (Pillow)."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).parent
S=3

def xy(box):
    return tuple(int(v*S) for v in box)

def poly(draw,points,**kwargs):
    draw.polygon([(int(x*S),int(y*S)) for x,y in points],**kwargs)

for index,car in enumerate(json.loads((ROOT/'cars.json').read_text())):
    c=tuple(car['color'])
    light=tuple(min(255,int(v*.65+115)) for v in c)
    dark=tuple(max(0,int(v*.46)) for v in c)
    im=Image.new('RGBA',(240*S,180*S),(0,0,0,0))
    d=ImageDraw.Draw(im)
    # Four heavy tires and an angular underbody.
    for x in (29,179):
        d.rounded_rectangle(xy((x,83,x+31,161)),radius=9*S,fill=(2,6,13,255),outline=(36,91,127,255),width=3*S)
        for y in (94,108,122,136):
            d.line(xy((x+4,y,x+28,y)),fill=(16,26,41),width=2*S)
    poly(d,[(52,40),(188,40),(209,104),(193,153),(167,169),(73,169),(47,153),(31,104)],fill=(5,15,31),outline=(4,32,51),width=3*S)
    # Layered bodywork makes different zones readable at racing-game scale.
    poly(d,[(50,60),(70,38),(170,38),(190,60),(199,114),(184,154),(164,164),(76,164),(56,154),(41,114)],fill=dark,outline=light,width=3*S)
    poly(d,[(57,61),(71,49),(169,49),(183,61),(188,106),(173,129),(67,129),(52,106)],fill=c,outline=light,width=2*S)
    poly(d,[(70,56),(81,41),(159,41),(170,56),(157,98),(83,98)],fill=(6,24,43),outline=(64,165,209),width=3*S)
    poly(d,[(80,54),(102,47),(114,47),(91,91),(76,91)],fill=(35,98,147))
    # Sculpted ventilation and racing stripes vary by model.
    for j in range(3):
        y=101+j*7
        d.line(xy((89,y,151,y)),fill=(3,24,41),width=3*S)
    if index%2==0:
        poly(d,[(112,41),(122,41),(130,97),(110,97)],fill=light)
    else:
        poly(d,[(91,115),(99,115),(83,146),(75,146)],fill=light)
        poly(d,[(141,115),(149,115),(165,146),(157,146)],fill=light)
    # Wide spoiler and support pillars.
    d.line(xy((66,54,66,33)),fill=(12,21,37),width=5*S)
    d.line(xy((174,54,174,33)),fill=(12,21,37),width=5*S)
    poly(d,[(20,31),(220,31),(211,47),(29,47)],fill=(8,25,45),outline=light,width=3*S)
    d.line(xy((35,35,205,35)),fill=(170,232,254),width=2*S)
    # Rear fascia and lightbars.
    d.rounded_rectangle(xy((49,115,191,153)),radius=10*S,fill=(6,18,34),outline=light,width=3*S)
    for x in (55,151):
        d.rounded_rectangle(xy((x,121,x+34,134)),radius=3*S,fill=(217,25,64),outline=(255,91,115),width=2*S)
        d.line(xy((x+5,124,x+29,124)),fill=(255,175,185),width=2*S)
    d.rounded_rectangle(xy((96,123,144,129)),radius=2*S,fill=(110,219,252))
    d.rounded_rectangle(xy((79,143,161,159)),radius=5*S,fill=(3,9,18),outline=(47,137,201),width=2*S)
    for x in (80,160):
        d.ellipse(xy((x-12,147,x+12,170)),fill=(5,47,96),outline=(74,201,249),width=3*S)
        d.ellipse(xy((x-4,154,x+4,163)),fill=(169,243,255))
    d.line(xy((54,155,70,165)),fill=light,width=3*S)
    d.line(xy((186,155,170,165)),fill=light,width=3*S)
    im.resize((240,180),Image.Resampling.LANCZOS).save(ROOT/car['sprite'])
