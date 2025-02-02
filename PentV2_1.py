from assembleinstrucV1_1 import *
from formatInput import *
from drawPentV2_1 import *
import pygame

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
    tot_layer = int(0)
    layer = int(1)
    skip = 0
    prevCirc = list()
    prevLine = list()
    for index in range(len(input)): # iterates the index trhough the length of the string
        if not skip > 0:
            print('index:{} char:{}'.format(index,input[index]),end='')

        if skip > 0:
            skip -= 1
            pass

        elif input[index] == '#':     # If cursor on base marker
            base = int()
            while not isMarker(input[index+1]): #All digits up to a marker being read as the base
                index += 1
                skip += 1
                base = int(str(base) + input[index])
                print(f'\tbase set to {base}')
            referencePoly(screen,base,originMod)

        elif input[index] == '%': #Records the total layers for later
            while not isMarker(input[index+1]):
                index += 1
                skip += 1
                tot_layer = int(str(tot_layer) + str(input[index]))
                print(f'\tlayers recorded, {tot_layer}')
            
        elif input[index] == '@':   #If cursor on circle marker
            temp.append(int(0))

            while not isMarker(input[index+1]): # All digits up to a marker being read as the circle position on polygon
                index += 1
                skip += 1
                temp[0] = int(str(temp[0]) + input[index])

            drawCircle(temp[0],screen,base,True,originMod) #draws the origin circle
            prevCirc = drawCircle(temp[0],screen,base,False,originMod) # saves the output of this circle for circle modifiers

            print(f'\tdrawing circle at {temp[0]}')

            temp = list([]) # destroy temporary values

        elif input[index] == '(':       # If there is a decimal in the circle
            temp.append(int(0))
            temp[0] = str(input[(index+1):(input.find(')'))])+'$' #Get the slice of the input that's just the decimal to pass back to the interpreter

            interpret(screen,temp[0],prevCirc)

            skip += (len(temp[0])+2) # skip to the end of the dcimal section
            input =  input[:input.find('(')] + '*'*(len(temp[0])+2) + input[input.find(')')+1:] # replace the decimal section with *'s to pass over so it doesn't interfere with future string searches
            print(input,'<<<<modified-string')

            temp = list([]) # destroy temporary values
        
        elif input[index] == '|':
            temp.append('') # creates temporary variable num1
            temp.append('') # creates temporary variable num2
            temp.append(0) # creates temporary variable starting layer
            temp.append('') # creates temporary variablefor line mods

            if input[index+1] == '^': #Check or indentation
                layer += 1
                temp[2] = layer
                index += 1
                skip += 1

            elif input[index+1] == '/':
                index += 1
                skip += 1
                temp[2] = int(layer)                
                layer += 1

            else:
                temp[2] = layer

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
            
            drawLine(temp[0],temp[1],temp[2],layer,tot_layer,screen,base,True,originMod)
            print(f'\tdrawing line from {temp[0]} to {temp[1]}')

            if input[index+1] == '+' or input[index+1] == '<':
                while input[index+1] == '+' or  input[index+1] == '<':
                    index += 1
                    skip += 1
                    temp[3] = str(temp[3]) + str(input[index])
                print('Line Modifiers:',temp[3])
                drawLineMods(screen,temp[3],drawLine(temp[0],temp[1],temp[2],layer,tot_layer,screen,base,False,originMod))
            prevLine = drawLine(temp[0],temp[1],temp[2],layer,tot_layer,screen,base,False,originMod)
            temp = list([])

        elif input[index] == '+': # This only handles + signs on circles
            temp.append('')
            temp[0] += '+'
            while input[index+1] == '+':
                index += 1
                skip += 1
                temp[0] += '+'
            drawCircMods(screen,temp[0],prevCirc,prevLine[0])
            print(f'\tdrawing circ mods {temp[0]}')
            temp = list([])

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
    from os import system
    system('cls')
    text = input('Enter number in decimal to be converted to pent: ')
    Pent(text)
    mainloop()