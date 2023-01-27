import pygame, sys, os
FPS = 60
def initStart(settings=(0.5)):
    pygame.init()

    volume = settings
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((width, height),pygame.HWSURFACE)

    # Stretch the background image to fit the screen
    background = pygame.image.load("JellyJam.png").convert()
    background = pygame.transform.scale(background, (width, height))

    # Blit the background image to the screen
    screen.blit(background, (0, 0))
    pygame.display.set_caption("Jelly Jam Menu")
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        start_button = createMenu(screen,width/2-100,200,200,50,"Start")
        settings_button = createMenu(screen,width/2-100,300,200,50,"Settings")
        exit_button = createMenu(screen,width/2-100,400,200,50,"Exit")
        if isClicked(screen,background,start_button):
            screen.blit(background, (0, 0))
            pygame.display.flip()
        if isClicked(screen,background,settings_button):
            screen.blit(background, (0, 0))
            screen.fill((100,100,100))
            pygame.display.flip()
            initSettings(screen,volume)
        if isClicked(screen,background,exit_button):
            pygame.quit()
            sys.exit()
        pygame.display.update()

def createMenu(screen,a,b,c,d,prompt="",radius=10):
    # Create the font object
    font = pygame.font.Font(None, 36)
    button = pygame.draw.rect(screen, (140,140,140), (a,b,c,d),border_radius=radius)
    text = font.render(prompt, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = button.center
    screen.blit(text, text_rect)
    pygame.display.flip()
    return button

def isClicked(screen,background,button):
    if pygame.mouse.get_pressed()[0]:
            if button.collidepoint(pygame.mouse.get_pos()):
                return True
    return False

def initSettings(screen,volume):
    background = pygame.image.load("JellyJam.png").convert()
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    while True:
        incSound = createMenu(screen,width/2+125,200,50,50,"->")
        decSound = createMenu(screen,width/2-175,200,50,50,"<-")
        sound = createMenu(screen,width/2-100,200,200,50,"Sound: "+str(volume*100))
        back = createMenu(screen,width/2-100,400,200,50,"Back")
        pygame.display.flip()
        if isClicked(screen,background,incSound) and volume <= 0.9:
            volume = round(volume+0.1,2)
            pygame.time.wait(200)
        if isClicked(screen,background,decSound) and volume >= 0.1:
            volume = round(volume-0.1,2)
            pygame.time.wait(200)
        if isClicked(screen,background,sound):
            if volume == 0:
                volume = .5
            else:
                volume = 0
            pygame.time.wait(200)
        if isClicked(screen,background,back):
            pygame.time.wait(200)
            initStart(volume)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

initStart()