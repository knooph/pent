def assembly(list,base = int(5),isDec = False):

    out = '#{}'.format(base)
    indent = False
    current = int(-1)
    previous = int(-1)
    layers = [] 
    decindex = len(out) + len(str(base)) + 1
    for i in range(base): #Sets up the empty layer list
        layers.append(0)

    for index in range(len(list)):
        if index == 0:                      # If the first digit, draw a circle
            circ = False
            out += '@{}'.format(list[0])
            layers[list[0]] += 1 
            current = list[index]
        elif list[index] == current:        # If the current number is the same as the index, draw a dash
            out += '+'
            indent = False
        elif list[index] == previous:       # If the previous number is the same as the index, draw an arrow
            out += '<'
            indent = True
        elif list[index] != current and list[index] != previous and type(list[index]) == int:
            layers[list[index]] += 1 
            if indent:
                layers[previous] += 1
                indent = False
                out += '|{}.{}-{}.{}'.format(previous,layers[previous],list[int(index)],layers[list[int(index)]])
            else:
                out += '|{}.{}-{}.{}'.format(current,layers[int(current)],list[int(index)],layers[list[int(index)]]) 
                previous = current
            current = list[index]
        elif list[index] == '.':
            out = out[:decindex] + '(' + assembly(list[index+1:],base,True) + ')' + out[decindex:]
            break
    layers.sort(reverse=True)

    if out.find('#') == -1:
        out = '%' + str(layers[0]) + out 
    else:
        out = out[:len(str(base))+1] + '%' + str(layers[0]) + out[len(str(base))+1:]

    if isDec:
        return out
    else:
        return out + '$'
