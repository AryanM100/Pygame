#!/bin/python3
import pygame
import sys
from random import randint
import time
from collections import namedtuple

pygame.init()
screen = pygame.display.set_mode((600,400))
pygame.display.set_caption("Dinothon")
clock = pygame.time.Clock()
font = pygame.font.Font(None,50)
game_active = 0
start_time = 0
score = 0
player_gravity = 0
level2 = 10
level3 = 20
level4 = 50
a = 0

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = font.render(f"Score : {current_time}",True,"Black")
	score_rect = score_surf.get_rect(center = (300,30))
	screen.blit(score_surf,score_rect)
	return current_time

def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			if obstacle_rect.bottom == 345:
				obstacle_rect.x += 10
			elif obstacle_rect.bottom == 221:
				obstacle_rect.x -= 19
			elif obstacle_rect.bottom == 351:
				obstacle_rect.x -= 13
			else:
				obstacle_rect.y += 9.7


			if obstacle_rect.bottom == 351:
				screen.blit(enemy, obstacle_rect)
			elif obstacle_rect.bottom == 345:
				screen.blit(enemy3, obstacle_rect)
			elif obstacle_rect.bottom == 221:
				screen.blit(enemy2, obstacle_rect)
			else:
				screen.blit(enemy4, obstacle_rect)

		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x >= -400]	

		return obstacle_list		
	else: return []

def collisions(player, obstacles):  	     
	if obstacles:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect):
			 	return 0
	if game_active == 2:
		return 2
	elif game_active == 3:
		return 3
	else:
		return 1

#Surfaces
sound = pygame.mixer.Sound("music.wav")
sound.set_volume(0.035)

star = pygame.image.load("star.png").convert_alpha()
star = pygame.transform.rotozoom(star,0,0.05)
star_rect = star.get_rect(center = (50,200))

player = pygame.image.load('dino.png').convert_alpha()
player = pygame.transform.scale(player,(60,60))
player_rect = player.get_rect(midbottom = (50,349))

back1 = pygame.image.load("both1.jpg").convert_alpha()
back1 = pygame.transform.scale(back1,(600,400))

back2 = pygame.image.load("both2.jpg").convert_alpha()
back2 = pygame.transform.scale(back2,(600,400))

endText = font.render("Game Over",True,"Black")
endText = pygame.transform.rotozoom(endText,0,2)
end_rect = endText.get_rect(midbottom = (320,125))

gameName = font.render("Dinothon",True,"Green")
gameName = pygame.transform.rotozoom(gameName,0,1.8)
gameName_rect = gameName.get_rect(midbottom = (310,125))

game_message = font.render("Press Space To Run", True,"Cyan")
game_message = pygame.transform.rotozoom(game_message,0,1.75)
game_message_rect = game_message.get_rect(midbottom = (300,375))

player_stand = pygame.image.load("dino.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,0.3)
player_stand_rect = player_stand.get_rect(midbottom = (300,300))

#Enemies
enemy = pygame.image.load("dino1.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (55,55))

enemy2 = pygame.image.load("dino1.png").convert_alpha()
enemy2 = pygame.transform.rotozoom(enemy2,90,0.1)

enemy3 = pygame.image.load("dino2.png").convert_alpha()
enemy3 = pygame.transform.rotozoom(enemy3, 90, 0.1)

enemy4 = pygame.image.load("dino1.png").convert_alpha()
enemy4 = pygame.transform.rotozoom(enemy4, 180, 0.1)

enemy5 = pygame.image.load("dino2.png").convert_alpha()
enemy5 = pygame.transform.rotozoom(enemy5, 270, 0.1)

obstacle_rect_list = []

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(700,1500))

obstacle_timer2 = pygame.USEREVENT + 2
pygame.time.set_timer(obstacle_timer2, 900)

obstacle_timer3 = pygame.USEREVENT + 3
pygame.time.set_timer(obstacle_timer3, randint(600,1500))


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if game_active != 0 and game_active != 4:
			if event.type == obstacle_timer and game_active <= 2:
				if randint(0,2):
					obstacle_rect_list.append(enemy.get_rect(midbottom = (randint(800,1000),351)))
				else:
					obstacle_rect_list.append(enemy.get_rect(midbottom = (randint(800,1000),221)))
			if event.type == obstacle_timer2 and game_active == 2:
				obstacle_rect_list.append(enemy.get_rect(midbottom = (randint(-100,-50),345)))
			if event.type == obstacle_timer3 and game_active == 3:
				obstacle_rect_list.append(enemy.get_rect(midbottom = (randint(-20,620),randint(-200,-50))))

		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = 1
				start_time = int(pygame.time.get_ticks() / 1000)

	if game_active == 1:
		sound.play()
		screen.blit(back1,(0,0))
		score = display_score()
		star_rect.midbottom = (550,145)
		screen.blit(star,star_rect)

		#Enemy Movement
		obstacle_rect_list = obstacle_movement(obstacle_rect_list)
		game_active = collisions(player_rect,obstacle_rect_list)
		#Player
		player_gravity += 1
		player_rect.y += player_gravity
		if player_rect.bottom >= 349: player_rect.bottom = 349
		screen.blit(player,player_rect)

		keys = pygame.key.get_pressed()
		if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and (player_rect.bottom == 349) and score >= 0.1:
			player_gravity = -18
		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
			player_rect.x += 5
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
			player_rect.x -= 5

		if player_rect.x <= -25 or player_rect.x >= 570:
			game_active = 0
		
		if score >= 40:
			obstacle_rect_list.clear()

		if player_rect.colliderect(star_rect):
			game_active = 2
			player_rect.left = 300
			obstacle_rect_list.clear()

	elif game_active == 2:
		screen.blit(back2,(0,0))
		score = display_score()
		star_rect.center = (-21,310)
		screen.blit(star, star_rect)

		#Enemy Movement
		obstacle_rect_list = obstacle_movement(obstacle_rect_list)
		game_active = collisions(player_rect,obstacle_rect_list)
		#Player
		player_gravity += 1
		player_rect.y += player_gravity
		if player_rect.bottom >= 349: player_rect.bottom = 349
		screen.blit(player,player_rect)

		keys1 = pygame.key.get_pressed()
		if (keys1[pygame.K_SPACE] or keys1[pygame.K_UP]) and (player_rect.bottom == 349):
			player_gravity = -18
		if (keys1[pygame.K_RIGHT] or keys1[pygame.K_d]):
			player_rect.x += 5
		if (keys1[pygame.K_LEFT] or keys1[pygame.K_a]):
			player_rect.x -= 5

		if player_rect.x <= -25 or player_rect.x >= 570:
			game_active = 0
		if player_rect.colliderect(star_rect):
			game_active = 3
			a = display_score()
			player_rect.left = 80
			obstacle_rect_list.clear()

	elif game_active == 3:
		screen.blit(back1,(0,0))
		score = display_score()
		
		
		star_rect.center = (550,165)
		screen.blit(star,star_rect)
		
		#Enemy Movement
		obstacle_rect_list = obstacle_movement(obstacle_rect_list)
		game_active = collisions(player_rect,obstacle_rect_list)
		#Player
		player_gravity += 1
		player_rect.y += player_gravity
		if player_rect.bottom >= 349: player_rect.bottom = 349
		screen.blit(player,player_rect)

		keys1 = pygame.key.get_pressed()
		if (keys1[pygame.K_SPACE] or keys1[pygame.K_UP]) and player_rect.bottom == 349:
			player_gravity = -18
		if (keys1[pygame.K_RIGHT] or keys1[pygame.K_d]):
			player_rect.x += 5
		if (keys1[pygame.K_LEFT] or keys1[pygame.K_a]):
			player_rect.x -= 5

		if player_rect.x <= -25 or player_rect.x >= 570:
			game_active = 0
		
		if score > a + 7:
			game_active = 4
			player_rect.left = 80
			obstacle_rect_list.clear()


	elif game_active == 4:
		sound.stop()
		screen.fill((30,135,150))
		player_rect.midbottom = (100,349)
		win_message = font.render("You Win!",True,"Black")
		win_message = pygame.transform.rotozoom(win_message,0,2)
		win_message_rect = win_message.get_rect(midbottom = (290,200))
		screen.blit(win_message, win_message_rect)

		game2_message = font.render(f"Press Space To Restart",True,"Black")
		game2_message = pygame.transform.rotozoom(game2_message,0,1.5)
		game2_message_rect = game2_message.get_rect(midbottom = (300,325))
		screen.blit(game2_message, game2_message_rect)

	elif game_active == 0:
		sound.stop()
		screen.fill((30,135,150))
		screen.blit(player_stand, player_stand_rect)
		obstacle_rect_list.clear()
		player_rect.midbottom = (100,349)
		player_gravity = 0

		score_message = font.render(f"L Score : {score}",True,"Black")
		score_message = pygame.transform.rotozoom(score_message,0,2)
		score_message_rect = score_message.get_rect(midbottom = (315,125))
		screen.blit(game_message, game_message_rect)
		
		if score > 0 : screen.blit(score_message, score_message_rect)
		else: screen.blit(gameName, gameName_rect)
			
	
	pygame.display.update()
	clock.tick(60)