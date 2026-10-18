from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from math import floor
b=Path(__file__).parent
out=b/'contest-entry';out.mkdir(exist_ok=True)
ORANGE='#FF6943'; YELLOW='#FFC83A'; DARK='#191A1C'; CREAM='#FFF8EE'; MUTED='#77736D'
FONT='/usr/share/fonts/truetype/lato/Lato-Black.ttf'
BOLD='/usr/share/fonts/truetype/lato/Lato-Bold.ttf'
REG='/usr/share/fonts/truetype/lato/Lato-Regular.ttf'

def font(sz,bold=True):return ImageFont.truetype(FONT if bold else REG,sz)
def txt(d,xy,t,sz,color=DARK,bold=True,spacing=0):
 d.text(xy,t,font=font(sz,bold),fill=color,spacing=spacing)

def load(s):return Image.open(b/s).convert('RGB')

def paste_frame(canvas,image,xy,width,r=20,shadow=True,border=True):
 image=load(image) if isinstance(image,str) else image
 image=image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
 x,y=xy;w,h=image.size
 if shadow:
  layer=Image.new('RGBA',canvas.size,(0,0,0,0));d=ImageDraw.Draw(layer)
  d.rounded_rectangle((x+12,y+15,x+w+12,y+h+15),radius=r,fill=(26,25,25,47))
  layer=layer.filter(ImageFilter.GaussianBlur(22))
  canvas.paste(layer,(0,0),layer)
 mask=Image.new('L',(w,h),0);ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=r,fill=255)
 canvas.paste(image,(x,y),mask)
 if border:ImageDraw.Draw(canvas).rounded_rectangle((x,y,x+w,y+h),radius=r,outline='#E0D7CB',width=2)
 return (x,y,w,h)

# 01 — Editorial cover: custom brand-specific concept, desktop + mobile hero
W,H=2200,1460
im=Image.new('RGB',(W,H),CREAM);d=ImageDraw.Draw(im)
d.rectangle((0,0,W,155),fill=DARK)
d.ellipse((65,46,124,105),fill=YELLOW,outline='#101011',width=5)
txt(d,(84,43),'a',47,DARK)
txt(d,(142,42),'advertising',52,'#FFFFFF')
txt(d,(382,43),'&',52,ORANGE)
txt(d,(421,43),'more',52,'#FFFFFF')
txt(d,(145,101),'THE EVERYTHING AGENCY.',16,'#BBBBB9')
txt(d,(1510,70),'A BESPOKE CAREERS EXPERIENCE',23,YELLOW)
txt(d,(68,194),'JOB VACANCY PAGE  /  HEADER & FOOTER REFINEMENT',24,ORANGE)
txt(d,(65,240),'MADE TO',76,DARK)
txt(d,(635,239),'ROCK!',77,ORANGE)
txt(d,(1270,279),'Original 3D artwork. Agency DNA. No templates.',24,MUTED,False)
paste_frame(im,'desktop-hero.png',(70,380),1440,24)
paste_frame(im,'mobile-hero.png',(1575,345),465,29)
d=ImageDraw.Draw(im)
d.rectangle((0,1345,W,H),fill=DARK)
notes=['3D COFFEE-THEMED ART','BRAND-MATCHED UX','DESKTOP + MOBILE','INTERACTIVE APPLICATION']
x=90
for i,n in enumerate(notes):
 d.ellipse((x,1383,x+14,1397),fill=ORANGE if i%2 else YELLOW)
 txt(d,(x+25,1378),n,22,'#FFFFFF')
 x += [480,465,480,470][i]
im.save(out/'01-custom-careers-concept.jpg',quality=95,subsampling=0)
im.save(out/'01-custom-careers-concept.png',optimize=True)

# 02 — Application form: explicit contest fields
W,H=2200,1600
im=Image.new('RGB',(W,H),'#F9F6F0');d=ImageDraw.Draw(im)
d.rectangle((0,0,W,176),fill=DARK)
txt(d,(85,32),'YOUR NEXT MOVE.',80,'#FFFFFF')
txt(d,(88,119),'VALIDATED APPLICATION FORM • IDENTIFICATION • CV UPLOAD • CALENDAR PICKER',22,YELLOW)
form=load('desktop-form.png')
paste_frame(im,form,(48,206),1360,20)
# Functional details to the right
x=1470
txt(d,(x,285),'MORE THAN',62,DARK)
txt(d,(x,352),'A PRETTY FORM.',62,ORANGE)
features=[('01','FULL IDENTITY DETAILS','Full name, DOB, phone and employer'),('02','FOREIGN APPLICANTS','Passport field appears conditionally'),('03','SMART DATE INPUTS','Native calendar and date validation'),('04','RESUME / CV UPLOAD','Drag & drop; PDF, DOC, DOCX up to 5MB'),('05','RESPONSIVE BY DESIGN','Clear, accessible fields at every size')]
y=520
for num,head,sub in features:
 d.ellipse((x,y+1,x+60,y+61),fill=YELLOW,outline=DARK,width=3)
 txt(d,(x+15,y+15),num,25,DARK)
 txt(d,(x+86,y),head,28,DARK)
 txt(d,(x+86,y+40),sub,19,MUTED,False)
 y+=170
im.save(out/'02-application-form.jpg',quality=94,subsampling=0)

# 03 — Responsive showcase collage
W,H=2130,1490
im=Image.new('RGB',(W,H),CREAM);d=ImageDraw.Draw(im)
d.rectangle((0,0,W,200),fill=YELLOW)
txt(d,(74,39),'ONE CAREERS EXPERIENCE.',78,DARK)
txt(d,(75,135),'BUILT FOR EVERY SCREEN.',36,DARK)
# montage of desktop hero + laptop panel, and mobile previews
paste_frame(im,'desktop-hero.png',(72,275),1170,23)
paste_frame(im,'mobile-hero.png',(1310,260),350,25)
paste_frame(im,'mobile-form.png',(1696,260),350,25)
d=ImageDraw.Draw(im)
d.rounded_rectangle((72,1115,1241,1370),radius=20,fill=DARK)
txt(d,(115,1150),'DESKTOP    →    TABLET    →    MOBILE',35,YELLOW)
txt(d,(115,1214),'Clear hierarchy, polished navigation, native date pickers,',27,'#FFFFFF',False)
txt(d,(115,1253),'and touch-friendly form fields — in the agency’s own style.',27,'#FFFFFF',False)
im.save(out/'03-responsive-design.jpg',quality=94,subsampling=0)

# 04, 05 — transparent full-page screenshots as ordinary jpg exports
load('desktop-full.png').save(out/'04-entire-desktop-page.jpg',quality=93,subsampling=0)
load('mobile-full.png').save(out/'05-entire-mobile-page.jpg',quality=93,subsampling=0)

for f in out.glob('*'):
 print(f.name, f.stat().st_size)
