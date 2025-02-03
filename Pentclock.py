import PentV2_1
import formatInput
import pygame
import time

def countLoop(dt=1,base=5,limit=None,screen=pygame.display.set_mode()):
    run = True
    while run:
        x = time.time()
        
        screen.fill([0,0,0])
        PentV2_1.interpret(screen,PentV2_1.assembly( formatInput.format( formatInput.changeBase( formatInput.format( str(x) ),10,base) ),base ))
        pygame.display.flip()
        time.sleep(1/base)

        events = pygame.event.get() # writes the event que to a list
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # if an event is a keypress and escape key stop the program, just escape key throws error bc not all events are keys
                run = False
                break

countLoop(base=5)