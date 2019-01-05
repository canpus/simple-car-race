#coding:utf-8
import random,time,pygame
from pygame.locals import *


pygame.init()
font=pygame.font.SysFont("Serif",40)
fonte=pygame.font.SysFont("Serif",20)
tex,tey=1000,750

afffps=True

clt=(0,0,0)

nbv=5 #(en plus du joueur)
cam=[0,0]
voitures=[]

bots=[]

finits=[]

trcvs=[]

cltrc1=(5,15,5) #herbe
cltrc2=(15,15,15) #frein

encour=True

####

taille_circuit=random.randint(4000,26000) #(px)

maps=["mp_1.png","mp_1.png"]
imgmape=pygame.transform.scale(pygame.image.load("images/"+random.choice(maps)),[tex,taille_circuit+tey*4])

voits=[]
voits.append( ["Pierson v1",100,20,200,50,"v1.png",1000,10] )
voits.append( ["chagear",150,10,150,60,"v2.png",1000,10] )
voits.append( ["camior",80,5,100,70,"v3.png",800,3] )
voits.append( ["formoula2",250,35,50,70,"v4.png",8000,1] )

vcts=[]

for vc in voits:
    for x in range(vc[7]): vcts.append( voits.index(vc) )

#0=nom 1=vit_max(px/s) 2=acc(px/s en + par sec) 3=man(px/s de droite-gauche) 4=frein(en px/s) 5=img 6=prix ( en neuros ) 7=chance de l'avoir (1-10 )

####


class Voiture:
    def __init__(self,x,y,tp):
        self.tp=tp
        vv=voits[tp]
        self.nom=vv[0]
        self.vit_max=float(vv[1])
        self.vit=0.0
        self.acc=float(vv[2])
        self.man=vv[3]
        self.frein=vv[4]
        self.px=x
        self.py=y
        self.tx=100
        self.ty=100
        self.img=pygame.transform.scale(pygame.image.load("images/"+vv[5]),[self.tx,self.ty])
        self.dac=time.time()
        self.dbg=time.time()
        self.dfr=time.time()
        self.az=10
        self.finit=False
        self.pos=None
        self.dts=time.time()
        self.dist=0 #en px
    def accel(self):
        if time.time()-self.dac >= 1/self.az:
            self.dac=time.time()
            self.vit+=self.acc/self.az
    def tourner(self,aa):
        if time.time()-self.dbg >= 1/self.az:
            self.dbg=time.time()
            if aa==1: self.px+=self.man/self.az
            else: self.px-=self.man/self.az
    def freine(self):
        if time.time()-self.dfr > 1/self.az:
            self.dfr=time.time()
            self.vit-=self.frein/self.az
            if self.vit <=0:
                self.vit = 0
    def ts(self):
        if time.time()-self.dts > 1/self.az:
            self.py-=self.vit/self.az
            self.dist+=self.vit/self.az
            ee=0.01
            if self.vit > self.vit_max: self.vit=self.vit_max
            if self.vit > 0:
                self.vit-=ee
            elif self.vit < 0:
                self.vit+=ee

class Player():
    def __init__(self):
        self.nom=""
        self.age=0
        self.tchs=[]  # 0=acc 1=frein 2=tourner gauche 3=tourner droite
        self.vselec=None

taillercy=200
taillercx=60
posrcx=tex-80
posrcy=50


def aff():
    fenetre.fill((0,0,0))
    fenetre.blit(imgmape,[0+cam[0],-taille_circuit-tex*2+cam[1]])
    fenetre.blit(pygame.transform.scale(pygame.image.load("images/ligne.png"),[tex,75]),[0+cam[0],-100+cam[1]])
    fenetre.blit(pygame.transform.scale(pygame.image.load("images/ligne.png"),[tex,75]),[0+cam[0],-taille_circuit+cam[1]])
    for t in trcvs: pygame.draw.rect(fenetre,t[0],(t[1],t[2],t[3],t[4]),0)
    pygame.draw.rect(fenetre,(250,250,250),(posrcx,posrcy,taillercx,taillercy),5)
    for v in voitures:
        if cam[0]+v.px < tex and cam[0]+v.px > 0 and cam[1]+v.py < tey+v.ty and cam[1]+v.py >0-v.ty :
            fenetre.blit(v.img,[v.px+cam[0],v.py+cam[1]])
            fenetre.blit( fonte.render(v.pos.nom,20,clt),[v.px+cam[0],v.py+v.ty+5+cam[1]])
            if v.finit: fenetre.blit(pygame.transform.scale(pygame.image.load("images/cp.png"),[v.tx,v.ty]),[v.px+cam[0],v.py+cam[1]])
        pygame.draw.circle(fenetre,v.pos.cl,(posrcx+int(v.px/tex*taillercx),posrcy+taillercy+int(v.py/taille_circuit*taillercy)),3)
    #stats
    fenetre.blit( font.render(str(p1.vselec.vit)[:6]+" px/s",20,clt), [20,20] )
    fenetre.blit( fonte.render(str(p1.vselec.dist)[:6]+" px parcourus",20,clt), [20,60] )
    pygame.display.update()

def bb():
    global encour
    cond=True
    for v in voitures:
        v.ts()
        if v.py<=-taille_circuit:
            if not v in finits: finits.append(v)
            v.finit=True
            v.freine()
        if v.vit > 0 or not v.finit: cond=False
        if v.px > tex-v.tx: v.px=tex-v.tx
        if v.px < 0+v.tx: v.px=0+v.tx
    if cond:
        encour=False
    
        
            

def bot():
    for b in bots:
        if random.randint(1,2) == 1 and not b.vselec.finit:
            b.vselec.accel()
            aa=random.randint(1,10)
            if aa<=2: b.vselec.tourner(1)
            elif aa<=4: b.vselec.tourner(2)

def begin():
    global voitures,bots
    xx,yy=150,0
    for x in range(nbv+1): voitures.append( Voiture(xx+120*x,yy,random.choice(vcts) ) )

    player1=Player()
    player1.nom="nathan"
    player1.tchs=[K_UP,K_DOWN,K_LEFT,K_RIGHT]
    player1.vselec=voitures[0]
    player1.vselec.pos=player1
    player1.cl=(0,250,0)
    
    for x in range(nbv):
        pp=Player()
        pp.nom="bot"+str(x)
        pp.vselec=voitures[x+1]
        pp.vselec.pos=pp
        pp.cl=(250,0,0)
        bots.append( pp )
    return player1

def azer():
    fenetre.fill((50,150,150))
    fenetre.blit(fonte.render("taille de circuit : "+str(taille_circuit),20,clt),[100,100])
    xx,yy=100,200
    for v in voitures:
        fenetre.blit(fonte.render(v.pos.nom,20,clt),[xx,yy])
        fenetre.blit(pygame.transform.scale(v.img,[100,100]),[xx,yy+30])
        xx+=110
    pygame.display.update()
    aa=True
    while aa:
        for event in pygame.event.get():
            if event.type==QUIT: aa=False
            elif event.type==KEYDOWN: aa=False

####

fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("TITRE")
pygame.key.set_repeat(40,30)

p1=begin()
azer()


while encour:
    tt=time.time()
    aff()
    bb()
    bot()
    for event in pygame.event.get():
        if event.type==QUIT: encour=False
        elif event.type==KEYDOWN:
            if event.key==K_q: encour=False
            if not p1.vselec.finit:
                if event.key==p1.tchs[0]   : p1.vselec.accel()
                elif event.key==p1.tchs[1] : p1.vselec.freine()
                elif event.key==p1.tchs[2] : p1.vselec.tourner(2)
                elif event.key==p1.tchs[3] : p1.vselec.tourner(1)
    if not p1.vselec.finit: cam=[0,tey/2-p1.vselec.py]
    else:
        p=None
        for b in bots:
            if not b.vselec.finit: p=b
        if p==None: p=p1
        cam=[0,tey/2-p.vselec.py]
    if afffps:
        fps=int(1/(time.time()-tt))
        fenetre.blit(fonte.render("fps : "+str(fps),20,clt),[tex-100,10])
        pygame.display.update()

####

pygame.draw.rect(fenetre,(105,125,186),(100,100,tex-100,tey-100),0)
pygame.draw.rect(fenetre,(250,250,250),(100,100,tex-100,tey-100),5)
fenetre.blit(font.render("Résultats",40,(250,150,150)),[350,150])
xx,yy=300,300
pos=1
for v in finits:
    fenetre.blit(fonte.render(str(pos)+" : "+v.pos.nom,20,clt),[xx,yy])
    yy+=40
    pos+=1
pygame.display.update()

encour2=True
while encour2:
    for event in pygame.event.get():
        if event.type==QUIT: encour2=False
        elif event.type==KEYDOWN:
            if event.key==K_q: encour2=False















