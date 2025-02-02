import decimal
from math import floor
allDigits = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')

def format(input):
    input = str(input)
    global allDigits
    out = list()
    oneDec = False
    for digit in input:
        try:
            out.append(allDigits.index(digit))
        except:
            if digit == '.' and oneDec == False:
                out.append('.')
                oneDec = True
            else:
                pass
    
    if out[len(out)-1] == '.':
        out = out[:len(out)-1]
    return out

def changeBase(input,inbase,outbase):
    pow0 = 0
    powref = []
    value = 0
    out = str()
    highPow = 0
    decpoint = True

    if input.count('.') == 1: # If there's a decimal, store the position of the zeroth power and remove the decimal from the input
        pow0 = len(input) -1 - input.index('.')
        input.pop(input.index('.'))
        decpoint = True

    for i in reversed(range(len(input))): # Make a separate list of the power of the base for each place in the input
        powref.append(i-pow0)

    for place in range(len(input)): # store the value of the input by iterate through the input list and convert to base 10
        value += input[place] * inbase**powref[place]

    while outbase**(highPow+1) <= value: # finds the highest power of the output base that fits into the value
        highPow += 1

    #print('{}^{} = {}'.format(outbase,highPow,outbase**highPow))

    PrecCount = 0 # safety to ensure there's no insanely long decimals(limited precision causing divide by 0 error)
    while value > 0 or highPow >= 0:
        #print('{} goes into {} {} times. append {}'.format(outbase**highPow,value,floor(decimal.Decimal(value)/decimal.Decimal(outbase**highPow)),allDigits[floor(decimal.Decimal(value)/decimal.Decimal(outbase**highPow))]))
        out = out + allDigits[floor(decimal.Decimal(value)/decimal.Decimal(outbase**highPow))] # appends the digit that represents the amount of times the highest power can fit within the value
        value = decimal.Decimal(value) - decimal.Decimal(floor(decimal.Decimal(value)/decimal.Decimal(outbase**highPow))) * decimal.Decimal(outbase**highPow) #subtracts the digit times the place from the value
        highPow -= 1
        if highPow < 0 and decpoint:
            decpoint = False
            out = out + '.'
        
        if not decpoint:
            PrecCount += 1

        if PrecCount > 6:
            break
    
    if len(out[(out.find('.')+1):]) > 20:
        out = out[0:out.find('.')+20]
    return out

if __name__ == '__main__':
    from os import system
    system('cls')    
    input = input('Enter number in decimal: ')
    print(format( changeBase( format(input),10,5)))