import math
import pygame
import random

class vector:
    
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    
    def __add__(self,other):
        return vector(self.x+other.x,self.y+other.y)
    
    def __sub__(self,other):
        return vector(self.x-other.x,self.y-other.y)
    
    def __mul__(self,other):
        if isinstance(other,float) or isinstance(other,int):
            return vector(self.x*other,self.y*other)
    
    def __truediv__(self,other):
        if isinstance(other,int):
            return vector(self.x*1/other,self.y*1/other)
    
    def __repr__(self):
        return f'{self.x},{self.y}'

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
        
    def unitVector(self):
        return vector(self.x/self.magnitude(),self.y/self.magnitude())

    def tup(self):
        return (self.x,self.y)
    
class circle:
    def __init__(self,pos:vector,mass:int,color:tuple,child:bool,parent=None,trailLength=2,range=None) -> None:
        self.pos = pos
        self.velocity = vector()
        self.accel = vector()

        self.mass = mass
        self.radius = mass
        self.color = color
        self.child = child
        self.parent = parent

        self.trail = [self.pos]*trailLength

    def update(self,win,reset,free):
        self.pos += self.velocity
        self.velocity += self.accel
        self.accel = vector()
        self.trail.append(self.pos)
        self.trail.pop(0)

        self.display(win)

    def force(self,force):
        self.accel += force/self.mass

    def display(self,win):
        pygame.draw.circle(win,self.color,self.pos.tup(),self.radius)
        #pygame.draw.line(win,self.color,self.pos.tup(),self.trail[0].tup())
        pygame.draw.polygon(win,self.color,((self.pos + vector(self.radius/2,self.radius/2)).tup(),(self.pos + vector(self.radius/2,self.radius/2)).tup(),self.trail[0].pos.tup()))

class Player(circle):
    children = []

    def __init__(self,pos:vector,mass:int,color:tuple,children:int,InfluenceRange,ChildrenMassRange,ChildColor,trailLength=2):
        super().__init__(pos,mass,color,False,trailLength=trailLength)
        for i in range(children):
            Player.children.append(circle(vector(random.randint(pos.x+InfluenceRange,pos.x-InfluenceRange),random.randint(pos.y+InfluenceRange,pos.y-InfluenceRange)),random.randint(ChildrenMassRange[0],ChildrenMassRange[1]),ChildColor,True,self,range=InfluenceRange))

    
