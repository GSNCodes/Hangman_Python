import os
import math
import random
import pygame

## Base -- Set-up
pygame.init()
WIDTH, HEIGHT = 800, 500
run = True
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman !")
clock = pygame.time.Clock()


## Game Images
images = []
for i in range(7):
	images.append(pygame.image.load('images/hangman' + str(i) + '.png'))

print(images)


## Game Variables
hangman_image = 0
guessed = []

## Button Set-up
RADIUS = 20
GAP = 15
letters = []
ASCII = 65
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT   = pygame.font.SysFont('comicsans', 60)
TITLE_FONT  = pygame.font.SysFont('comicsans', 70)
start_x = round((WIDTH-((2*RADIUS + GAP) * 13)) / 2)
start_y = 400

for i in range(26):
	x = start_x + GAP*2 + (((RADIUS*2) + GAP) * (i%13))
	y = start_y + (i//13) * (GAP + RADIUS*2)
	letters.append([x, y, chr(i+ASCII), True])



def draw(hangman_image, guessed, word):
	window.fill(WHITE)

	## Draw Title
	title = TITLE_FONT.render("Hangman !", 1, BLACK)
	window.blit(title, (WIDTH/2 - title.get_width()/2, 20))

	## Draw word
	word_display = ''
	for w in word:
		if w in guessed:
			word_display += w + ' '
		else:
			word_display += '_ '
	text = WORD_FONT.render(word_display, 1, BLACK)
	window.blit(text, (400, 200))

	## Draw buttons
	for letter in letters:
		x, y, character, visible = letter
		if visible:
			pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
			text = LETTER_FONT.render(character, 1, BLACK)
			window.blit(text, (x - text.get_width()/2, y - text.get_height()/2))




	window.blit(images[hangman_image], (150,100))
	pygame.display.update()

def end_message(msg):
	pygame.time.delay(1000)
	window.fill(WHITE)
	text = WORD_FONT.render(msg, 1, BLACK)
	window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
	pygame.display.update()
	pygame.time.delay(3000)


def game_play(hangman_image, guessed, run):
	words = ['DEVELOPER', 'POTATO', 'GSN', 'PYTHON']
	word = random.choice(words)
	close_window = False
	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				close_window = True
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				m_x, m_y = pygame.mouse.get_pos()
				for letter in letters:
					x, y, character, visible = letter
					if visible:
						dist = math.sqrt((x-m_x)**2 + (y-m_y)**2)
						if dist < 2*RADIUS:
							letter[3] = False
							guessed.append(character)

							if character not in word:
								hangman_image += 1
		draw(hangman_image, guessed, word)

		won = True
		for w in word:
			if w not in guessed:
				won = False
				break

		if won:
			end_message("You Won !!!!")
			break

		if hangman_image == 6:
			end_message("You lost :( ")
			break

		pygame.display.update()

	if not close_window:
		guessed = []
		for letter in letters:
			letter[3] = True
		game()

## Game Loop

def game():
	window.fill(WHITE)
	play_again = "Do you want to play again?"
	text = WORD_FONT.render(play_again, 1, BLACK)
	window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))




	pygame.draw.circle(window, BLACK, (300, 400), RADIUS*2, 3)
	yes = "Yes"
	text = LETTER_FONT.render(yes, 1, BLACK)
	window.blit(text, (300 - text.get_width()/2, 400 - text.get_height()/2))

	pygame.draw.circle(window, BLACK, (450, 400), RADIUS*2, 3)
	no = "No"
	text = LETTER_FONT.render(no, 1, BLACK)
	window.blit(text, (450 - text.get_width()/2, 400 - text.get_height()/2))

	pygame.display.update()
	# pygame.time.delay(2000)
	
	click = True
	while click:
		loc = 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				break

			if event.type == pygame.MOUSEBUTTONDOWN:
				m_x, m_y = pygame.mouse.get_pos()
				for i,coords in enumerate([(300,400), (450, 400)]):
					x, y = coords
					dist = math.sqrt((x-m_x)**2 + (y-m_y)**2)
					if dist < 2*RADIUS:
						click = False
						loc = i

			if loc == 0:
				game_play(0, [], True)
			
			


if __name__ == '__main__':

	game_play(hangman_image, guessed, run)


	pygame.quit()
