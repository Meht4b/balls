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
        if isinstance(other,float) or isinstance(other,int):
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
    def __init__(self,pos:vector,mass:int,color:tuple,child:bool,parent=None,trailLength=2,range=None,timer=None) -> None:
        self.pos = pos
        self.velocity = vector()
        self.accel = vector()

        self.mass = mass
        self.radius = mass
        self.color = color
        self.child = child
        self.parent = parent
        self.timer = timer

        self.trail = [self.pos]*trailLength

    def update(self,win):
        self.pos += self.velocity
        self.velocity += self.accel
        self.accel = vector()
        self.trail.append(self.pos)
        self.trail.pop(0)

        self.display(win)

    def force(self,force):
        self.accel += force/self.mass

    def display(self,win):
        if self.parent:
            
            color = (self.color[0]*self.timer/self.parent.ChildrenLifetime,self.color[0]*self.timer/self.parent.ChildrenLifetime,self.color[0]*self.timer/self.parent.ChildrenLifetime)
            pygame.draw.circle(win,color,self.pos.tup(),self.radius)
            pygame.draw.line(win,color,self.pos.tup(),self.trail[0].tup())

        else:
            pygame.draw.circle(win,self.color,self.pos.tup(),self.radius)
            pygame.draw.line(win,self.color,self.pos.tup(),self.trail[0].tup())
        #pygame.draw.polygon(win,self.color,((self.pos + vector(self.radius/2,self.radius/2)).tup(),(self.pos + vector(self.radius/2,self.radius/2)).tup(),self.trail[0].tup()))

class Player(circle):
    children = []

    def __init__(self,pos:vector,mass:int,color:tuple,childrenNumber:int,InfluenceRange,ChildrenMassRange,ChildrenMassMultiplier,ChildColor,SelfForce,SelfFriction,ChildForce,ChildFriction,ChildrenLifetime,regen,trailLength=2):
        super().__init__(pos,mass,color,False,trailLength=trailLength)
        for i in range(childrenNumber):

            Player.children.append(circle(vector(random.randint(pos.x-InfluenceRange,pos.x+InfluenceRange),random.randint(pos.y-InfluenceRange,pos.y+InfluenceRange)),random.randint(ChildrenMassRange[0],ChildrenMassRange[1])*ChildrenMassMultiplier,ChildColor,True,self,range=InfluenceRange,timer=ChildrenLifetime))

        self.SelfForce = SelfForce
        self.SelfFriction = SelfFriction
        self.ChildForce = ChildForce
        self.ChildFriction = ChildFriction
        self.InfluenceRange = InfluenceRange
        self.ChildrenLifetime = ChildrenLifetime
        self.regen = regen
        self.regenTracker = regen
        self.childrenNumber = childrenNumber
        self.ChildrenMassRange = ChildrenMassRange
        self.ChildrenMassMultiplier = ChildrenMassMultiplier
        self.ChildColor = ChildColor

    def PlayerUpdate(self,win,ResetVel,NullForce):
        mousepos = vector(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        
        #making player head follow cursor
        self.force((mousepos-self.pos)*self.SelfForce)
        self.force(self.velocity*-self.SelfFriction)
        self.update(win)

        #making player children follow cursor
        for i in Player.children:
            dis = mousepos - i.pos
            if dis.magnitude()<self.InfluenceRange and not NullForce:
                #adding friction and force
                i.force(dis*self.ChildForce)
                i.force(i.velocity*-self.ChildFriction)
                i.timer = self.ChildrenLifetime

            else:
                i.timer-=1
            
            #space button
            if ResetVel:
                i.velocity = vector()
            i.update(win)

            #killing far away children
            if i.timer==0:
                Player.children.remove(i)

        #regenerating children
        if len(Player.children)<self.childrenNumber:
            if self.regenTracker<0:
                self.regenTracker = self.regen
                Player.children.append(circle(vector(random.randint(int(self.pos.x-self.InfluenceRange),int(self.pos.x+self.InfluenceRange)),random.randint(int(self.pos.y-self.InfluenceRange),int(self.pos.y+self.InfluenceRange))),random.randint(self.ChildrenMassRange[0],self.ChildrenMassRange[1])*self.ChildrenMassMultiplier,self.ChildColor,True,self,range=self.InfluenceRange,timer=self.ChildrenLifetime))
            self.regenTracker-=1
        #self.collision()

    #do collision
    @staticmethod
    def partition(array, low, high):
    
        pivot = array[high].pos.x
        i = low - 1
        for j in range(low, high):
            if array[j].pos.x <= pivot:
                i = i + 1
                (array[i], array[j]) = (array[j], array[i])
        (array[i + 1], array[high]) = (array[high], array[i + 1])
        return i + 1

    @staticmethod
    def quicksort(array, low, high):
        if low < high:

            pi = Player.partition(array, low, high)
            Player.quicksort(array, low, pi - 1)
            Player.quicksort(array, pi + 1, high)

    @classmethod
    def collision(cls):
        possibleCollision = []
        Player.quicksort(Player.children,0,len(Player.children)-1)
        i,j = 0,1
        
        while i<len(Player.children)-1:
            Start = Player.children[i].pos.x+Player.children[i].radius
            End = Player.children[j].pos.x-Player.children[j].radius
            if End < Start:
                possibleCollision.append((Player.children[i],Player.children[j]))
                if j==len(Player.children)-1:
                    i+=1
                else:
                    j+=1

            else:
                i+=1
        
        for i in possibleCollision:
            dis = (i[0].pos - i[1].pos).magnitude()
            if dis<i[0].radius+i[1].radius:
                total_mass = i[0].mass + i[1].mass
                v1x = (i[0].velocity.x * (i[0].mass - i[1].mass) + 2 * i[1].mass * i[1].velocity.x) / total_mass
                v1y = (i[0].velocity.y * (i[0].mass - i[1].mass) + 2 * i[1].mass * i[1].velocity.y) / total_mass
                v2x = (i[1].velocity.x * (i[1].mass - i[0].mass) + 2 * i[0].mass * i[0].velocity.x) / total_mass
                v2y = (i[1].velocity.y * (i[1].mass - i[0].mass) + 2 * i[0].mass * i[0].velocity.y) / total_mass
                
                i[0].velocity = vector(v1x,v1y)
                i[1].velocity = vector(v2x,v2y)
                print('coll')
            