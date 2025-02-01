import time
import math
import pygame

def screenDimension(): #Returns the smallest dimension of the screen
    if pygame.display.get_init() and pygame.display.get_window_size()[0] >= pygame.display.get_window_size()[1]:
        return pygame.display.get_window_size()[1]
    elif pygame.display.get_init() and pygame.display.get_window_size()[1] >= pygame.display.get_window_size()[0]:
        return pygame.display.get_window_size()[0]
    else:
        return [0,0]

def referencePoly(screen,sides=int(5),originMod = [[0,0],0]):
    px=[]
    py=[]

    if originMod[0] == [0,0] and originMod[1] == 0:
        scale = int(screenDimension()*0.4)
        originMod[0] = [pygame.display.get_window_size()[0]/2,pygame.display.get_window_size()[1]/2]
    else:
        #print(originMod[1])
        scale = originMod[1] * 0.6

    for i in range(sides):    #Generates the coordinates of the vertices of the shape
        px.append(math.sin(2*math.pi/sides*i))
        py.append(math.cos(2*math.pi/sides*i))
    
    for p in range(0,sides-1):
        point1 = [px[p]*scale+originMod[0][0], -1*py[p]*scale+originMod[0][1]] # creates tuples by grabbing coordinates from the right list for points 1 and 2. z1 & z2 are scale factors
        point2 = [px[p+1]*scale+originMod[0][0], -1*py[p+1]*scale+originMod[0][1]]
        pygame.draw.line(screen,[100,100,100],point1,point2,2)
    pygame.draw.line(screen,[100,100,100],[px[0]*scale+originMod[0][0], -1*py[0]*scale+originMod[0][1]],[px[sides-1]*scale+originMod[0][0], -1*py[sides-1]*scale+originMod[0][1]],2)

def drawCircle(center,screen,sides=5,drawBool=True,originMod=[[0,0],0]):
    px=[]
    py=[]
    if originMod[1] == 0:
        scale = int(screenDimension()*0.4)
    else:
        scale = scale = originMod[1] * 0.6

    for i in range(sides):    #Generates the coordinates of the vertices of the shape
        px.append(math.sin(2*math.pi/sides*i))
        py.append(math.cos(2*math.pi/sides*i))

    if originMod[0] == [0,0]: # if there is no origin argument, set to center of screen
        originMod[0] = [pygame.display.get_window_size()[0]/2,pygame.display.get_window_size()[1]/2]

    if drawBool: # if input is to draw the circle(default)
        point1 = [px[center]*scale+originMod[0][0], -1*py[center]*scale+originMod[0][1]] # adjust polygon vertex coords to be centered around origin
        pygame.draw.circle(screen,[255,255,255],point1,scale/4)
        pygame.draw.circle(screen,[0,0,0],point1,scale/4-2)
        pygame.draw.circle(screen,[255,255,255],originMod[0],pow(scale,0.30377))
    elif not drawBool: #returns the center of the circle and scale in [0,0],[0] if not drawing
        point1 = [px[center]*scale+originMod[0][0], -1*py[center]*scale+originMod[0][1]]
        return [point1,scale/4]
    
def drawLine(num1,num2,z1,z2,z,screen,sides=int(5),drawBool=True,originMod=[[0,0],0]):
    px=[]
    py=[]


    if originMod[1] == 0:
        scale = screenDimension() * 0.4
    else:
        scale = originMod[1] * 0.6

    z1 = (1.2*z-z1+1)/(1.2*z) * scale
    z2 = (1.2*z-z2+1)/(1.2*z) * scale

    for i in range(sides):    #Generates the coordinates of the vertices of the shape
        px.append(math.sin(2*math.pi/sides*i))
        py.append(math.cos(2*math.pi/sides*i))

    if originMod == [0,0]:
        originMod = [pygame.display.get_window_size()[0]/2,pygame.display.get_window_size()[1]/2]
    
    point1 = [px[num1]*z1+originMod[0][0], -1*py[num1]*z1+originMod[0][1]] # creates tuples by grabbing coordinates from the right list for points 1 and 2. z1 & z2 are scale factors
    point2 = [px[num2]*z2+originMod[0][0], -1*py[num2]*z2+originMod[0][1]]
    if drawBool:
        pygame.draw.line(screen,[255,255,255],point1,point2,4)
    else:

        if (point1[0]-point2[0]) == 0:
            m = 230
        else:
            m = (point1[1]-point2[1])/(point1[0]-point2[0])
        x = point2[0]
        b = point2[1]
        #print(m,x,b,sep='\n')
        return [m,x,b,num1,num2,sides,scale]

def drawLineMods(screen,que=str(),line=[0,0,0,0,0,0,0]):
    #originMod = [pygame.display.get_window_size()[0]/2,pygame.display.get_window_size()[1]/2]
    
    if math.sin(2*math.pi/line[5]*line[4]) > math.sin(2*math.pi/line[5]*line[3]):
        LoR = 1
    else:
        LoR = -1

    m = line[0]
    x = line[1]
    b = line[2]
    if line[6] == 0:
        scale = screenDimension() * 0.4
    else:
        scale = line[6]
    orthom = -1 * m**-1
    step = 1
    arrowLength = scale/15
    arrowWidth = scale/15

    for i in que:
        if i == '<':
            step += 1
            px = x - LoR*(step*1.4*arrowLength*math.cos(math.atan(m)))
            py = b - LoR*(step*1.4*arrowLength*math.sin(math.atan(m)))
            rx = px + LoR*(arrowLength*math.cos(math.atan(m)) - arrowWidth*math.cos(math.atan(orthom)))
            ry = py + LoR*(arrowLength*math.sin(math.atan(m)) - arrowWidth*math.sin(math.atan(orthom)))
            lx = px + LoR*(arrowLength*math.cos(math.atan(m)) + arrowWidth*math.cos(math.atan(orthom)))
            ly = py + LoR*(arrowLength*math.sin(math.atan(m)) + arrowWidth*math.sin(math.atan(orthom)))
        elif i == '+':
            step += 0.5
            px = x - LoR*(step*1.4*arrowLength*math.cos(math.atan(m)))
            py = b - LoR*(step*1.4*arrowLength*math.sin(math.atan(m)))
            rx = px + LoR*(-1* arrowWidth*math.cos(math.atan(orthom)))
            ry = py + LoR*(-1* arrowWidth*math.sin(math.atan(orthom)))
            lx = px + LoR*(arrowWidth*math.cos(math.atan(orthom)))
            ly = py + LoR*(arrowWidth*math.sin(math.atan(orthom)))

        pygame.draw.line(screen,[255,255,255],[px,py],[rx,ry],2)
        pygame.draw.line(screen,[255,255,255],[px,py],[lx,ly],2)

#window = pygame.display.set_mode()
#pygame.display.flip()

def mainloop():
    run = True
    while run:
        time.sleep(0.01)
        events = pygame.event.get() # writes the event que to a list
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # if an event is a keypress and escape key stop the program, just escape key throws error bc not all events are keys
                run = False
                break