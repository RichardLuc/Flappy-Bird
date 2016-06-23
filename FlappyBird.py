import pygame
import sys
import os
import random
from pygame.locals import*


class FlappyBird:
	bestScore = 0

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((400, 700))
		pygame.display.set_caption("Flappy Bird")
		self.birdAnimation = [pygame.image.load("assets/0.png"),
						 pygame.image.load("assets/1.png"),
						 pygame.image.load("assets/2.png"),
						 pygame.image.load("assets/dead.png")]
		self.background = pygame.image.load("assets/background.png")
		self.splashScreen = pygame.image.load("assets/splash.png")
		self.gameOverScreen = pygame.image.load("assets/scoreboard.png")
		self.medals = [pygame.image.load("assets/medal_bronze.png"),
					pygame.image.load("assets/medal_silver.png"),
					pygame.image.load("assets/medal_gold.png")]
		self.restart = pygame.image.load("assets/replay.png")
		self.restartButton = pygame.Rect((150, 300), (self.restart.get_width(), self.restart.get_height()))
		self.currMedal = 0
		self.sprite = 0
		self.birdX = 50
		self.birdY = 200
		self.isDead = False
		self.wallX = 400
		self.wallGap = 170
		self.topPipe = pygame.image.load("assets/top.png")
		self.bottomPipe = pygame.image.load("assets/bottom.png")
		self.offset = random.randint(-300,100)
		self.score = 0
		self.fontObj = pygame.font.SysFont("Ariel", 50)
		self.initTap = False
		self.topPipeHitBox = pygame.Rect((self.wallX, - 100 + self.offset), (self.topPipe.get_width(), self.topPipe.get_height()))
		self.bottomPipeHitBox = pygame.Rect((self.wallX, self.topPipe.get_height() - 100 + self.wallGap + self.offset), (self.bottomPipe.get_width(), self.bottomPipe.get_height()))
		self.birdHitBox = pygame.Rect((self.birdX, self.birdY), (self.birdAnimation[0].get_width(), self.birdAnimation[0].get_height()))
		self.activateAI = False

		
	
	def walls(self):
		self.wallX -= 6
		
		if self.wallX <= -50:
			self.wallX = 400
			self.score += 1
			self.offset = random.randint(-300,100)
			
		if self.topPipeHitBox.colliderect(self.birdHitBox):
			self.isDead = True
		if self.bottomPipeHitBox.colliderect(self.birdHitBox):
			self.isDead = True
	
	def controls(self):
		if self.event.type == pygame.MOUSEBUTTONDOWN:
			self.activateAI = False
			self.sprite = 1
			self.birdY -= 120
			self.birdHitBox = pygame.Rect((self.birdX, self.birdY), (self.birdAnimation[0].get_width(), self.birdAnimation[0].get_height()))
			
	def splash_screen(self):
		self.update_screen()
		self.screen.blit(pygame.transform.scale(self.splashScreen, (400, 700)), (0, 0))
		if self.event.type == pygame.MOUSEBUTTONDOWN:
			self.initTap = True

	def update_screen(self):
		if self.isDead == True:
			self.sprite = 3
			if FlappyBird.bestScore <= self.score:
				FlappyBird.bestScore = self.score
			if self.score < 10:
				self.currMedal = 0
			elif self.score >= 10 and self.score < 20:
				self.currMedal = 1
			else:
				self.currMedal = 2
				
			self.wallX = 400
			if self.birdY <= 650:
				self.birdY = 650
				
			self.screen.blit(pygame.transform.scale(self.gameOverScreen, (400, 700)), (0, 0))
			self.screen.blit(pygame.transform.scale(self.medals[self.currMedal], (76,109)), (52, 288))
			self.screen.blit(self.restart, (150, 300))
			self.screen.blit(self.fontObj.render(str(self.score), 0, (255, 255, 255)), (310, 275))
			self.screen.blit(self.fontObj.render(str(FlappyBird.bestScore), 0, (255, 255, 255)), (310, 375))
			
			for self.event in pygame.event.get():
				if self.event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if self.restartButton.collidepoint(pos):
						self.score = 0
						self.isDead = False
						self.initTap = False
						FlappyBird().main()
			
		else:
			self.screen.fill((255, 255, 255))
			self.screen.blit(self.background, (0,0))
			self.screen.blit(self.birdAnimation[self.sprite], (self.birdX, self.birdY))
			self.screen.blit(self.topPipe, (self.wallX, -100 + self.offset))
			self.screen.blit(self.bottomPipe, (self.wallX, self.topPipe.get_height() - 100 + self.wallGap + self.offset))
			self.screen.blit(self.fontObj.render(str(self.score), 0, (255, 255, 255)), (200, 50))
			
	def ai(self):
		if self.activateAI == True:
			if self.birdY >= (self.topPipe.get_height() - 100 + self.wallGap + self.offset - 30):
				self.birdY -= 120

	def main(self):
		while True:
			for self.event in pygame.event.get():
				if self.event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
					
				if self.event.type == pygame.KEYDOWN:
					self.activateAI = True
				if self.initTap == False:
					self.splash_screen()
				else:
					self.controls()
					
			if self.initTap == True:
				self.screen.fill((255, 255, 255))
				self.sprite = 2
				self.birdY += 8

				self.ai()
				self.walls()
				
				self.topPipeHitBox = pygame.Rect((self.wallX, - 100 + self.offset), (self.topPipe.get_width(), self.topPipe.get_height()))
				self.bottomPipeHitBox = pygame.Rect((self.wallX, self.topPipe.get_height() - 100 + self.wallGap + self.offset), (self.bottomPipe.get_width(), self.bottomPipe.get_height()))
				self.birdHitBox = pygame.Rect((self.birdX, self.birdY), (self.birdAnimation[0].get_width(), self.birdAnimation[0].get_height()))
				self.update_screen()

			pygame.display.update()
			pygame.time.Clock().tick(60)

			
if __name__ == "__main__":
    FlappyBird().main()
