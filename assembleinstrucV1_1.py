from formatInput import *
def clearList(list):
    for i in range(len(list)):
        list[i] = 0
    return list
        
def assembly(list,base = int(5),isDec = False):
    out = '#{}'.format(base)
    indent = False
    current = int(-1)
    previous = int(-1)
    layerFill = []
    decindex = int()

    for i in range(base):
        layerFill.append(0)

    for index in range(len(list)):
        #print('\nDigit:{},(index {})\nCurrent:{}\nPrevious:{}'.format(list[index],index,current,previous))
        if index == 0:                      # If the first digit, draw a circle
            circ = False
            out += '@{}'.format(list[0])
            decindex = len(out)
            current = list[index]
            layerFill[int(list[index])] = 1

        elif list[index] == current:        # If the current number is the same as the index, draw a dash
            out += '+'
            indent = False

        elif list[index] == previous:       # If the previous number is the same as the index, draw an arrow
            out += '<'
            indent = True

        elif list[index] == '.':            # Passes the rest of the list to a new assebly method and inserts that at decindex
            out = out[:decindex] + '(' + assembly(list[index+1:],base,True) + ')' + out[decindex:]
            break

        elif list[index] != current and list[index] != previous and type(list[index]) == int: # Otherwise draw a line
            
            if indent:                     # if drawing a line and indenting, 
                indent = False
                layerFill = clearList(layerFill)
                layerFill[int(previous)] += 1
                current = list[index]
                out += '|^{}-{}'.format(previous,current)
            else:
                previous = current
                current = list[index]
                out += '|{}-{}'.format(previous,current)
            
    if isDec:
        return out
    else:
        return out + '$'
                    
if __name__ == '__main__':
    from os import system
    system('cls')
    input = input('Enter number in quinary: ')
    print(format(input))
    print(assembly(format(input),5))


#input: 1 , 2 , 4, 2 , 3, . , 0 , 0 , 3
#action c   l   l  <   l  .   c   +   l
#prev  -1   1   2  2   4  -  -1  -1   0
#curren 1   2   4  4   3  -   0   0   3