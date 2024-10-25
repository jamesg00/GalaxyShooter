WWII Game Explanation
WWII is a Pygame-based game where the player controls a sprite that can move in four directions and shoot bullets at enemies. The game features multiple enemies that shoot projectiles and missiles that spawn based on the player's score. When the player or an enemy is hit, an explosion animation is displayed.

Features
Player movement and shooting.
Enemy movement and shooting.
Missiles that spawn and move towards the player.
Collision detection for bullets, enemies, and missiles.
Explosion animations upon collisions.
Score tracking and game over condition.
How to Play
Start the Game: Launch the game, and control the player sprite using arrow keys.
Shoot Bullets: Use the spacebar to shoot bullets at enemies.
Avoid Projectiles: Dodge enemy bullets and missiles.
Score Points: Shoot enemies to score points. Every 10 points, a missile will spawn.
Game Over: The game ends when the player collides with an enemy, bullet, or missile.
Code Explanation
Initialization and Asset Loading
python
Copy code
import pygame
from pygame import mixer
import random
import math
from object import Background

# Initialize Pygame
pygame.init()
mixer.init()
screen = pygame.display.set_mode((300, 500))
clock = pygame.time.Clock()

# Load sounds and music
mixer.music.load("assets/Sonic 2 Music_ Wing Fortress Zone.mp3")
mixer.music.play(-1)
player_explosion_sound = pygame.mixer.Sound("assets/playerExplosion.mp3")
missile_sound = pygame.mixer.Sound('assets/missleSound.mp3')

# Load fonts and images
font = pygame.font.Font('assets/upheavtt.ttf', 32)
game_over_font = pygame.font.Font('assets/upheavtt.ttf', 32)
missile_animation_frames = [pygame.transform.rotate(pygame.image.load(f"assets/missle/image{i}.png"), 45) for i in range(1, 9)]
explosion_images = [pygame.image.load(f"assets/explosion/ex{i}.png") for i in range(1, 9)]
player_explosion_images = [pygame.image.load(f"assets/playerExplosion/explosion{i}.png") for i in range(1, 5)]
enemy_image = pygame.transform.scale(pygame.image.load("assets/nice.png"), (40, 40))
enemy_image_rotated = pygame.transform.rotate(enemy_image, 360)
![Screenshot 2024-10-25 123102](https://github.com/user-attachments/assets/8d581e62-8d64-4bd3-b759-7b8803a3cfe9)
![Screenshot 2024-10-25 123145](https://github.com/user-attachments/assets/d327932d-90b6-4ad9-84c5-497d2cc418b2)
