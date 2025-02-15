from assembleinstruc import *
from formatInput import *
from drawPentV2_1 import *
import pygame
from os import system
system('cls')

def isMarker(char = str()):
    if char == '#':
        return True
    elif char == '(':
        return True
    elif char == ')':
        return True
    elif char == '@':
        return True
    elif char == '|':
        return True
    elif char == '.':
        return True
    elif char == '-':
        return True
    elif char == '$':
        return True
    elif char == '*':
        return True
    elif char == '+':
        return True
    elif char == '<':
        return True
    elif char == '%':
        return True

def interpret(screen,input = str(),originMod = [[0,0],0]):
    print('\nInterpreter:{}'.format(input),'_'*(60-len(input)))
    if originMod == [0,0,0]:
        originMod = [pygame.display.get_window_size()[0]/2,pygame.display.get_window_size()[1]/2]

    temp = list([]) # I like doing this so I can create and destroy temporary variables as I like
    base = int(2) # Default the base to 2 because 1 is impossible
    layers = int()
    skip = 0
    for index in range(len(input)): # iterates the index trhough the length of the string
        if not skip > 0:
            print('index:{} char:{}'.format(index,input[index]))

        if skip > 0:
            skip -= 1
            pass

        elif input[index] == '#':     # If cursor on base marker
            base = int()
            while not isMarker(input[index+1]): #All digits up to a marker being read as the base
                index += 1
                skip += 1
                base = int(str(base) + input[index])
            referencePoly(screen,base,originMod)
        elif input[index] == '%':
            while not isMarker(input[index+1]):
                index += 1
                skip += 1
                layers = int(str(layers) + input[index])
            
        elif input[index] == '@':   #If cursor on circle marker
            temp.append(int(0))
            temp.append(int(1)) # set up two temporary variables

            while not isMarker(input[index+1]): # All digits up to a marker being read as the circle position on polygon
                index += 1
                skip += 1
                temp[0] = int(str(temp[0]) + input[index])
            drawCircle(temp[0],screen,base,True,originMod)
            if input[index+1] == '(':       # If there is a decimal in the circle
                temp[1] = str(input[(index+2):(input.find(')'))])+'$' #Get the slice of the input that's just the decimal to pass back to the interpreter

                interpret(screen,temp[1],drawCircle(temp[0],screen,base,False))

                skip += (len(temp[1])+2) # skip to the end of the dcimal section
                input =  input[:input.find('(')] + '*'*(len(temp[1])+2) + input[input.find(')')+1:] # replace the decimal section with *'s to pass over so it doesn't interfere with future string searches
                print(input,'<<<<modified-string')

            temp = list([]) # destroy temporary values
        
        elif input[index] == '|':
            temp.append('') # create for temporary values for num1 num2 z1 z2
            temp.append('')
            temp.append('')
            temp.append('')

            while not isMarker(input[index+1]): # All digits up to a marker being read as the start position for a line
                index += 1
                skip += 1
                temp[0] = int(str(temp[0]) + input[index])

            index += 1 # read over dot
            skip += 1

            while not isMarker(input[index+1]): # All digits up to a marker being read as the starting layer for a line
                index += 1
                skip += 1
                temp[1] = int(str(temp[1]) + input[index])

            index += 1 # read over dash
            skip += 1

            while not isMarker(input[index+1]): # All digits up to a marker being read as the ending position for a line
                index += 1
                skip += 1
                temp[2] = int(str(temp[2]) + input[index])

            index += 1 # read over dot
            skip += 1

            while not isMarker(input[index+1]): # All digits up to a marker being read as the ending layer for a line
                index += 1
                skip += 1
                temp[3] = int(str(temp[3]) + input[index])
            
            drawLine(temp[0],temp[2],temp[1],temp[3],layers,screen,base,True,originMod)

            
            if input[index+1] == '+' or input[index+1] == '<':
                temp.append('')
                while input[index+1] == '+' or input[index+1] == '<':
                    index += 1
                    skip += 1
                    temp[4] = temp[4] + input[index]
                print('Line Modifiers:',temp[4])
                drawLineMods(screen,temp[4],drawLine(temp[0],temp[2],temp[1],temp[3],layers,screen,base,False,originMod))
            
            temp = list([]) # destroy temporary values
            
        elif input[index] == '*': # pass over dummy character
            pass

        elif input[index] == '$': # Denotes end of the string
            break

        else:
            print('could not identify',input[index])

    print('_'*73,'\n')

input = assembly( format( changeBase( format( input("Enter decimal number to be converted to pent: ") ),10,5) ),5 )
#input = assembly( format( changeBase( format( '23424523.4564' ),10,5) ),5 )
#input = assembly(format(input('Enter number in quinary: ')),5)
#input = assembly(format('12344334342'),5)
#print(input)

window = pygame.display.set_mode()
#interpret(window,input)
interpret(window,input)
#interpret(window,'#5@2(@1|1.1-2.1)|2.1-4.1|4.1-0.1$')
#print(assembly( format( changeBase( format( "15.6" ),10,5) ),5 ))

pygame.display.flip()
mainloop()