from assembleinstrucV1_1 import *
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
    tot_layer = int(1)
    layer = int(1)
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
                tot_layer = int(str(tot_layer) + str(input[index]))
            
        elif input[index] == '@':   #If cursor on circle marker
            temp.append(int(0))
            temp.append(int(1)) # set up two temporary variables

            while not isMarker(input[index+1]): # All digits up to a marker being read as the circle position on polygon
                index += 1
                skip += 1
                temp[0] = int(str(temp[0]) + input[index])

            drawCircle(temp[0],screen,base,True,originMod) #draws the origin circle

            if input[index+1] == '(':       # If there is a decimal in the circle
                temp[1] = str(input[(index+2):(input.find(')'))])+'$' #Get the slice of the input that's just the decimal to pass back to the interpreter

                interpret(screen,temp[1],drawCircle(temp[0],screen,base,False))

                skip += (len(temp[1])+2) # skip to the end of the dcimal section
                input =  input[:input.find('(')] + '*'*(len(temp[1])+2) + input[input.find(')')+1:] # replace the decimal section with *'s to pass over so it doesn't interfere with future string searches
                print(input,'<<<<modified-string')

            temp = list([]) # destroy temporary values
        
        elif input[index] == '|':

            if input[index+1] == '^': #Check or indentation
                layer += 1
                index += 1
                skip += 1

            temp.append('') # creates temporary variable num1
            temp.append('') # creates temporary variable num2

            while not isMarker(input[index+1]): # Everything read up to the next marker will be the starting digit
                index += 1
                skip += 1
                temp[0] = int(str(temp[0]) + str(input[index]))
            index += 1
            skip += 1
            while not isMarker(input[index+1]): # Everything read up to the next marker will be the ending digit
                index += 1
                skip += 1
                temp[1] = int(str(temp[1]) + str(input[index]))
            drawLine(temp[0],temp[1],layer,layer,tot_layer,screen,base,True,originMod)

            if input[index+1] == '+' or input[index+1] == '<':
                temp.append('') # creates temporary variablefor line mods
                while not (input[index+1] == '+' or input[index+1] == '<'):
                    index += 1
                    skip += 1
                    temp[2] = str(temp[2]) + input[index]
                print('Line Modifiers:',temp[2])
                drawLineMods(screen,temp[2],drawLine(temp[0],temp[1],layer,layer,tot_layer,screen,base,False,originMod))
            temp = list()
        elif input[index] == '*': # pass over dummy character
            pass

        elif input[index] == '$': # Denotes end of the string
            break

        else:
            print('could not identify',input[index])

    print('_'*73,'\n')


def Pent(text, folder = './'):
    
    input = assembly( format( changeBase( format( text ),10,5) ),5 )


    window = pygame.display.set_mode()

    interpret(window,input)

    pygame.display.flip()
    pygame.image.save(window,f'{folder}pent-{text}.png')

if __name__ == '__main__':
    text = input('Enter number in decimal to be converted to pent: ')
    Pent(text)
    mainloop()