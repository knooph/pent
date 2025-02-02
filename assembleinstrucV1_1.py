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
    tot_layer = 1
    store = str('')
    pendingCirc = False
    for i in range(base):
        layerFill.append(0)

    for index in range(len(list)):

        if index == 0:                      # If the first digit, set pending circle to true so it can be drawn later. This is so the interpreter draws the circle on top of the line
            pendingCirc = True
            store += f'@{list[0]}'
            current = list[index]
            layerFill[int(list[index])] = 1

        elif list[index] == current:        # If the current number is the same as the index, draw a dash
            if pendingCirc:
                store += '+'
            else:
                out += '+'
            indent = False
            
        elif list[index] == previous:       # If the previous number is the same as the index, draw an arrow
            out += '<'
            indent = True

        elif list[index] == '.':            # Passes the rest of the list to a new assebly method
            store = store[:len(str(list[0]))+1] + '(' + assembly(list[index+1:],base,True) + ')' + store[len(str(list[0]))+1:]
            break

        elif list[index] != current and list[index] != previous and type(list[index]) == int: # Otherwise draw a line
            
            if pendingCirc and len(out) > (len(str(base))+len(str(tot_layer))+2): #adds a placeholder character * to be replaced later
                pendingCirc = False
                out += '*'

            if indent:                     # if drawing a line and indenting, 
                indent = False        
                layerFill = clearList(layerFill) #clear the list that keeps track of layers
                layerFill[int(previous)] += 1    #add 1 layer the start and end position of line
                layerFill[int(list[index])] += 1
                tot_layer += 1                   #updates layer count
                current = list[index]
                out += '|^{}-{}'.format(previous,current)

            elif layerFill[int(list[index])] >= 1:
                previous = current
                current = list[index]
                layerFill = clearList(layerFill)
                layerFill[int(current)] += 1
                tot_layer += 1
                out += '|/{}-{}'.format(previous,current)
            
            else:
                previous = current
                current = list[index]
                layerFill[int(current)] += 1
                out += '|{}-{}'.format(previous,current)
            
    if out.find('*') == -1 and pendingCirc: #if there is no placeholder and there is a circle pending, add it to the end of out
        out += store
    elif out.find('*') >= 0:    # if there is a placeholder, replace it
        out = out.replace('*',store)

    out = out[:len(str(base))+1] + f'%{tot_layer}' + out[len(str(base))+1:]

    if isDec:
        return out
    else:
        return out + '$'
                    
if __name__ == '__main__':
    from os import system
    system('cls')
    #input = changeBase(format(input('Enter number in decimal: ')),10,5)
    input = input('Enter number in decimal: ')
    print(format( changeBase( format(input),10,5)))
    print(assembly( format( changeBase( format(input),10,5) ),5 ))