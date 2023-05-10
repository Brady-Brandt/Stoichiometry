import pygame

SCREEN_DIM = (800, 800)
pygame.init()

screen = pygame.display.set_mode(SCREEN_DIM)
pygame.display.set_caption("Stoichiometry")


while True:
	screen.fill(BACKGROUND)	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit = True

	pygame.display.flip()
