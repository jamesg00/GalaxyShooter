import pygame
from pygame import mixer
import random
import math

from object import Background

pygame.init()
mixer.init()
screen = pygame.display.set_mode((300, 500))
clock = pygame.time.Clock()
running = True
dt = 0

mixer.music.load("assets/Sonic 2 Music_ Wing Fortress Zone.mp3")
mixer.music.play(-1)

player_explosion_sound = pygame.mixer.Sound("assets/playerExplosion.mp3")
missile_sound = pygame.mixer.Sound('assets/missleSound.mp3')
player_angle = 0  # Initial player angle
# Create a Font object
font = pygame.font.Font('assets/upheavtt.ttf', 32)

game_over_font = pygame.font.Font('assets/upheavtt.ttf', 32)
missile_animation_frames = [pygame.transform.rotate(pygame.image.load(f"assets/missle/image{i}.png"), 45) for i in range(1, 9)]
explosion_images = [pygame.image.load(f"assets/explosion/ex{i}.png") for i in range(1, 9)]
player_explosion_images = [pygame.image.load(f"assets/playerExplosion/explosion{i}.png") for i in range(1,5)]
enemy_image = pygame.transform.scale(pygame.image.load("assets/nice.png"), (40, 40))
enemy_image_rotated = pygame.transform.rotate(enemy_image, 360)
num_of_enemies = 4
enemies = []
active_explosions = []
player_visible = True

enemyProjectiles = []
enemyProjectiles_image = pygame.transform.scale(pygame.image.load("assets/EnemyBullet.png"), (20,20))
enemyBullet_rotate = enemy_projectiles_image = pygame.transform.rotate(pygame.image.load("assets/EnemyBullet.png"), -90)

for i in range(num_of_enemies):
    enemy_sprite = pygame.sprite.Sprite()
    enemy_sprite.image = enemy_image_rotated
    enemy_sprite.rect = enemy_image_rotated.get_rect(topleft=(0, 0))
    enemies.append({
        "img": enemy_image_rotated,  # Use the preloaded and resized image
        "x": random.randint(0, 240),
        "y": random.randint(50, 150),
        "x_change": 3,
        "y_change": 40, 
        "shoot_timer": 0,  # Add the shoot timer key
        "shoot_interval": random.uniform(1.0, 3.0),
        "sprite": enemy_sprite
    })

player_image = pygame.transform.scale(pygame.image.load("assets/705975.png"), (30, 30))
player_pos = pygame.Vector2(150, 500)

# Object
bg = Background(screen)

# Create bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("assets/download.png"), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.angle = angle

    def update(self):
        dx = 5 * math.cos(math.radians(self.angle-270))
        dy = -5 * math.sin(math.radians(self.angle-270))
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.y < 0:
            self.kill()

# Create missile class

# Create missile class
class Missile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        pygame.sprite.Sprite.__init__(self)
        self.frames = missile_animation_frames
        self.current_frame = 0
        self.frame_timer = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.speed = 300  # Speed in pixels per second
        direction = pygame.Vector2(target_pos) - pygame.Vector2(start_pos)
        if direction.length() != 0:
            self.velocity = direction.normalize() * self.speed
        else:
            self.velocity = pygame.Vector2(0, 1) * self.speed  # Move downwards if direction is zero
        missile_sound.play()  # Play the missile sound when the missile spawns

    def update(self):
        global game_over
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        self.animate()

        # Check for collision with the player
        if self.rect.colliderect(player_rect):
            trigger_player_explosion(player_pos)  # Trigger player explosion
            player_explosion_sound.play()  # Play the explosion sound
            game_over = True  # Game over when the player is hit by the missile

    def animate(self):
        self.frame_timer += dt
        if self.frame_timer > 0.1:  # Change frame every 100 milliseconds
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]



# Initialize the missile group
missile_group = pygame.sprite.Group()
score = 0
game_over = False
amplitude = 10  # Amplitude of the sine wave
frequency = 0.5

player_lives = 3
heart_image = pygame.transform.scale(pygame.image.load("assets/705975.png"), (20, 20))

def show_player_lives():
    for i in range(player_lives):
        screen.blit(heart_image, (screen.get_width() - 30 - i * 25, 10))

def show_score():
    global score_text, score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255 ))
    score_text2 = font.render("Score: " + str(score), True, (0, 0, 0 ))
    y_offset = amplitude * math.sin(frequency * pygame.time.get_ticks() / 1000)  # Calculate y offset based on sine function 
    screen.blit(score_text2, (15, 15 + y_offset)) 
    screen.blit(score_text, (10, 10 + y_offset))

enemy_bullet_image = pygame.transform.scale(pygame.image.load("assets/EnemyBullet.png"), (20, 20))
enemy_bullet_image_rotated = pygame.transform.rotate(enemy_bullet_image, 360)

def enemy_shoot(position):
    global enemyProjectiles  # This line is technically not needed for appending, but added for clarity
    # Projectiles move downwards with a fixed speed
    velocity = pygame.Vector2(0, 200)  # 300 pixels per second downwards
    projectile_rect = enemy_bullet_image_rotated.get_rect(center=position)
    enemyProjectiles.append({'rect': projectile_rect, 'velocity': velocity})
    bullet_sound = pygame.mixer.Sound('assets/arcade-8bit-fx-159064.mp3')
    bullet_sound.play()

amplitude_game_over = 10  # Amplitude of the sine wave for "GAME OVER" text
frequency_game_over = 0.5  # Frequency of the sine wave for "GAME OVER" text


def show_game_over(score):
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    score_text = game_over_font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))

    y_offset_game_over = amplitude_game_over * math.sin(frequency_game_over * pygame.time.get_ticks() / 1000)  # Sine wave for GAME OVER text
    y_offset_score = amplitude * math.sin(frequency * pygame.time.get_ticks() / 1000)  # Sine wave for score text

    screen.blit(game_over_text, (game_over_rect.x, game_over_rect.y + y_offset_game_over))
    screen.blit(score_text, (score_rect.x, score_rect.y + y_offset_score))


player_group = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
bullet_fired = False

for enemy in enemies:
    enemy_sprite = pygame.sprite.Sprite()
    enemy_sprite.image = enemy["img"]
    enemy_sprite.rect = enemy["img"].get_rect(topleft=(enemy["x"], enemy["y"]))
    enemy_group.add(enemy_sprite)
    enemy["sprite"] = enemy_sprite  # Add sprite to enemy dictionary

enemy_shoot_timer = 0
enemy_shoot_interval = 6  # seconds between each shot
missile_spawned_for_score_10 = False
player_hit_enemy = False
player_hit_missile = False
player_hit_enemy_projectile = False


def trigger_player_explosion(position):
    active_explosions.append({
        "frames": iter(player_explosion_images),  # Use player explosion images
        "pos": (position[0] - player_explosion_images[0].get_width() // 2, position[1] - player_explosion_images[0].get_height() // 2),
        "frame_timer": 0,
        "frame_index": 0
    })


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:


        dt = clock.tick(60) / 1000
        enemy_shoot_timer += dt
        if enemy_shoot_timer >= enemy_shoot_interval:
            for enemy in enemies:
                enemy_shoot(enemy["sprite"].rect.center)  # Enemy shoots from its current position
            enemy_shoot_timer = 0  # Reset the timer

        screen.fill((0, 0, 0))  # Clear the screen
        bg.update(2)  # Update and draw the background

        bullet_group.update()
        missile_group.update()  # Update the missile group

        if player_visible:
            rotated_player_image = pygame.transform.rotate(player_image, player_angle)
            player_rect = rotated_player_image.get_rect(center=player_pos)
            screen.blit(rotated_player_image, player_rect.topleft)

            # Rotate the player image
        rotated_player_image = pygame.transform.rotate(player_image, player_angle)
        player_rect = rotated_player_image.get_rect(center=player_pos)

        # Draw the player
        screen.blit(rotated_player_image, player_rect.topleft)
        # Update enemy movement and sprite positions
        for enemy in enemies:
            enemy["x"] += enemy["x_change"]
            if enemy["x"] < 0 or enemy["x"] > (screen.get_width() - enemy["img"].get_width()):
                enemy["x_change"] *= -1
                enemy["y"] += enemy["y_change"]

            enemy["sprite"].rect.topleft = (enemy["x"], enemy["y"])

            enemy_hit = pygame.sprite.spritecollide(enemy["sprite"], player_group, False)
            if enemy_hit:
                player_lives -= 1
                print("Player hit!")
                if player_lives <= 0:
                    game_over = True
                else:
                    # Reset player position
                    player_pos.update(150, 500)
                    player_angle = 0


                # Update enemy shoot timer
            enemy["shoot_timer"] += dt
            if enemy["shoot_timer"] >= enemy["shoot_interval"]:
                enemy_shoot(enemy["sprite"].rect.center)
                enemy["shoot_timer"] = 0  # Reset the timer
                enemy["shoot_interval"] = random.uniform(1.0, 3.0)  # Set a new random interval

        
        for enemy in enemies:
            if player_rect.colliderect(enemy["sprite"].rect) and not player_hit_enemy:
                trigger_player_explosion(player_pos, player_explosion_images)  # Pass player_explosion_images here
                player_explosion_sound.play()  # Play the explosion sound
                player_lives -= 1
                player_hit_enemy = True
                if player_lives <= 0:
                    game_over = True
                if player_lives > 0:
                    screen.blit(rotated_player_image, player_rect.topleft)
                else:
                    player_pos.update(150, 500)
                    player_angle = 0
                break  # Exit the loop after decrementing lives            
        screen_rect = screen.get_rect()

        for bullet in bullet_group:
            hit_enemy = pygame.sprite.spritecollide(bullet, enemy_group, False)
            if hit_enemy:
                exS = mixer.Sound("assets/atari_boom4.wav")
                exS.play()
                print("Enemy hit!")
                score += 1
                bullet.kill()
                for enemy_sprite in hit_enemy:
                    active_explosions.append({
                        "frames": iter(explosion_images),  # Use an iterator for the frames
                        "pos": enemy_sprite.rect.topleft,
                        "frame_timer": 0,  # Track the delay between frames
                        "frame_index": 0  # Current frame index
                    })
                    

                    
                    # Reset enemy position
                    for enemy in enemies:
                        if enemy["sprite"] == enemy_sprite:
                            enemy["x"] = random.randint(0, 240)
                            enemy["y"] = random.randint(50, 150)
                            enemy_sprite.rect.topleft = (enemy["x"], enemy["y"])
                            break
        for missile in missile_group:
            # Check for collision with the player
            if missile.rect.colliderect(player_rect) and not player_hit_missile:
                trigger_player_explosion(player_pos)
                player_explosion_sound.play()
                player_lives -= 1
                if player_lives <= 0:
                    game_over = True
                else:
                    # Reset player position
                    player_pos.update(150, 500)
                    player_angle = 0
                missile.kill()  # Remove the missile from the group when it hits the player
                player_hit_missile = True

            # Check for collision with player's bullets
            hit_missile = pygame.sprite.spritecollide(missile, bullet_group, True)
            if hit_missile:
                for _ in hit_missile:
                    exS = mixer.Sound("assets/atari_boom4.wav")
                    exS.play()
                    active_explosions.append({
                        "frames": iter(explosion_images),
                        "pos": missile.rect.topleft,
                        "frame_timer": 0,
                        "frame_index": 0
                    })
                    missile.kill()  # Remove the missile from the group when it's hit by a bullet

# Reset the flag at the end of the frame
        player_hit_missile = False  # Remove the missile from the group when it's hit by a bullet

        for enemyProjectile in enemyProjectiles[:]:
            enemyProjectile['rect'].x += enemyProjectile['velocity'].x * dt
            enemyProjectile['rect'].y += enemyProjectile['velocity'].y * dt
            screen.blit(enemy_bullet_image_rotated, enemyProjectile['rect'].topleft)

            if player_rect.colliderect(enemyProjectile['rect']):
                trigger_player_explosion(player_pos)
                player_explosion_sound.play()  # Play the explosion sound
                player_lives -= 1
                if player_lives <= 0:
                    game_over = True
                else:
                    player_pos.update(150, 500)
                    player_angle = 0
                player_visible = False  # Hide the player
                enemyProjectiles.remove(enemyProjectile)  # Remove the projectile after collision
                break  # Exit the loop after decrementing lives
            
        # Update and draw explosions
        for explosion in active_explosions[:]:
            explosion["frame_timer"] += dt
            if explosion["frame_timer"] > 0.05:  # Change frame every 50 milliseconds
                explosion["frame_timer"] = 0
                explosion["frame_index"] += 1
                if explosion["frame_index"] >= len(explosion_images):
                    active_explosions.remove(explosion)
                else:
                    screen.blit(explosion_images[explosion["frame_index"]], explosion["pos"])
            else:
                screen.blit(explosion_images[explosion["frame_index"]], explosion["pos"])
        
        
        show_player_lives()
        show_score()
        if score % 10 == 0 and score != 0 and not missile_spawned_for_score_10:
            missile = Missile(start_pos=(-50, -50), target_pos=player_pos)
            missile_group.add(missile)
            missile_spawned_for_score_10 = True

        if score % 10 != 0:
            missile_spawned_for_score_10 = False




        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt
        if keys[pygame.K_SPACE] and not bullet_fired:
            bulletS = mixer.Sound("assets/arcade-8bit-fx-159064.mp3")
            bulletS.play()
            # Calculate the initial position of the bullet based on player angle and position
            bullet_offset_x = 30 * math.cos(math.radians(player_angle + 90))
            bullet_offset_y = -30 * math.sin(math.radians(player_angle + 90))
            bullet = Bullet(player_pos.x + bullet_offset_x, player_pos.y + bullet_offset_y, player_angle)
            bullet_group.add(bullet)
            bullet_fired = True
        elif not keys[pygame.K_SPACE]:
            bullet_fired = False  # Reset the flag when the space bar is released

        if keys[pygame.K_q]:
            player_angle = 0  # Reset player angle to 0
            player_pos.update(150, 500)  # Reset player position

            
        if player_pos.x < 0:
            player_pos.x = 0
        if player_pos.x > 300 - player_image.get_width():
            player_pos.x = 300 - player_image.get_width()
        if player_pos.y < 0:
            player_pos.y = 0
        if player_pos.y > 500 - player_image.get_height():
            player_pos.y = 500 - player_image.get_height()

        player_group.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)
        missile_group.draw(screen)  # Draw missiles



        
        
        for enemyProjectile in enemyProjectiles[:]:
            enemyProjectile['rect'].y += enemyProjectile['velocity'].y * dt
            screen.blit(enemy_bullet_image_rotated, enemyProjectile['rect'].topleft)

            # Check for collision with player
            if player_rect.colliderect(enemyProjectile['rect']):
                player_lives -= 1
                if player_lives <= 0:
                    game_over = True
                else:
                    player_pos.update(150, 500)
                    player_angle = 0
                break  # Exit the loop after decrementing lives

    


           
        pygame.display.flip()

    else:
    # Game is over, show game over screen
        screen.fill((0, 0, 0))  # Clear the screen
        show_game_over(score)
        pygame.display.update()  # Update the display
        waiting = True

        while waiting:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        game_over = False
                        score = 0
                        player_lives = 6
                        # Reset enemies
                        enemies = []
                        for i in range(num_of_enemies):
                            enemy_sprite = pygame.sprite.Sprite()
                            enemy_sprite.image = enemy_image_rotated
                            enemy_sprite.rect = enemy_image_rotated.get_rect()
                            enemy_sprite.rect.topleft = (random.randint(0, 240), random.randint(50, 150))
                            enemies.append({
                                "img": enemy_image_rotated,
                                "x": enemy_sprite.rect.x,
                                "y": enemy_sprite.rect.y,
                                "x_change": 3,
                                "y_change": 40,
                                "shoot_timer": 0,
                                "shoot_interval": random.uniform(1.0, 3.0),
                                "sprite": enemy_sprite
                            })
                        # Reset the enemy_group with new enemy sprites
                        enemy_group.empty()
                        for enemy in enemies:
                            enemy_group.add(enemy["sprite"])
                        # Reset player
                        player_pos = pygame.Vector2(150, 500)
                        player_angle = 0
                        # Clear bullet group
                        bullet_group.empty()
                        # Clear enemy projectiles
                        enemyProjectiles = []
                        # Clear active explosions
                        active_explosions = []
            pygame.display.update()
pygame.quit()
