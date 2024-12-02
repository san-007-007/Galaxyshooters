import pygame
import random
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for both development and PyInstaller """
    try:
        # If we're running as a frozen executable (e.g., PyInstaller)
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        # If we're in development (not frozen)
        else:
            return os.path.join(os.path.abspath('.'), relative_path)
    except Exception as e:
        print("Error in resource_path:", e)
        return None

#initialize pygame
pygame.init()

#create screen
screen=pygame.display.set_mode((800,600))

pygame.display.set_caption("Galaxy Shooters")

icon=pygame.image.load(resource_path("Icons/icon.png"))
pygame.display.set_icon(icon)

ply1=pygame.math.Vector2((370,480))

background=pygame.image.load(resource_path("Icons/bg.jpg"))
craft=pygame.image.load(resource_path("Icons/craft.png"))
alien=pygame.image.load(resource_path("Icons/alien.png"))
explode=pygame.image.load(resource_path("Icons/explosion.png"))

game_state = "playing"  # Change state to game over
speed=1
enemy_positions=[]
bullets=[]
bullet_positions=[]
score=0

font = pygame.font.Font(None, 36)

def playerMovements(keys):
    if (keys[pygame.K_UP] or keys[pygame.K_w])and ply1.y>0:
        ply1.y-=speed
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and ply1.x>0:
        ply1.x-=speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and ply1.x<600:
        ply1.x+=speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and ply1.y<600:
        ply1.y+=speed

def generate_enemy():
    x=random.randint(0,300)
    y=random.randint(0,100)
    enemy_position=pygame.math.Vector2((x,y))
    enemy_positions.append(enemy_position)

def move_enemies():
    for pos in enemy_positions:
        if pos.x==600:
            enemy_positions.remove(pos)
            pos.x=0
            enemy_positions.append(pos)
        pos.x+=speed/4
        pos.y+=speed/4
        screen.blit(alien,pos)

def fireBullet():
    bullet_vector=pygame.Vector2(ply1.x+10,ply1.y)
    bullet=pygame.Rect(bullet_vector.x,bullet_vector.y,5,50)
    bullets.append(bullet)
    bullet_positions.append(bullet_vector)


def isKilled():
    global score
    for bullet in bullets:
        for enemy in  enemy_positions:
            if bullet.colliderect(pygame.Rect(enemy.x,enemy.y,alien.get_width(),alien.get_height())):
                score+=1
                enemy_positions.remove(enemy)
                bullets.remove(bullet)
                for i in range(50):#for loop used for visual effect
                    screen.blit(explode, (enemy.x, enemy.y))  # display explosion
                    pygame.display.update()
                break
def isDead():
    global game_state
    ply1_rect=pygame.Rect(ply1.x,ply1.y,craft.get_width(),craft.get_height())
    for enemy in enemy_positions:
        enemy_rect=pygame.Rect(enemy.x,enemy.y,alien.get_width(),alien.get_height())
        if ply1_rect.colliderect(enemy_rect):
            game_state = "game_over"  # Change state to game over

def moveBullet():
    for bullet in bullets:
        bullet.y-=100
        if bullet.y<=0:
            bullets.remove(bullet)
        else:
            pygame.draw.rect(screen,"cyan",bullet)

def draw_text(surface, text, position, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def reset_game():
    global ply1, enemy_positions, bullets, bullet_positions, score, game_state
    ply1 = pygame.math.Vector2((370, 480))  # Reset player position
    enemy_positions.clear()  # Clear enemy positions
    bullets.clear()  # Clear bullets
    bullet_positions.clear()  # Clear bullet positions
    score = 0  # Reset score
    game_state = "playing"  # Set the game state to "playing"

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    keys = pygame.key.get_pressed()

    # Game state: playing
    if game_state == "playing":
        screen.fill((0, 0, 0))  # Clear screen (black background)
        screen.blit(background, (0, 0))  # Draw background
        screen.blit(craft, (ply1.x, ply1.y))  # Draw player spaceship

        # Player movement and actions
        playerMovements(keys)
        if keys[pygame.K_f]:
            fireBullet()
        if random.randint(0, 25) < 1:
            generate_enemy()

        # Move and draw bullets and enemies
        moveBullet()
        move_enemies()
        isKilled()
        isDead()  # Check for collisions between player and enemies

        # Draw score
        draw_text(screen, "Score: " + str(score), (10, 10))

        pygame.display.update()  # Update the display

    # Game state: game_over
    elif game_state == "game_over":
        screen.blit(background,(0,0))
        draw_text(screen, "Score: " + str(score), ((screen.get_width() - 120) / 2, screen.get_height() / 2 - 50))
        draw_text(screen, "GAME OVER", ((screen.get_width() - 120) / 2, screen.get_height() / 2), "red")
        draw_text(screen, "Press Enter to Restart", ((screen.get_width() - 22 * 10) / 2, screen.get_height() / 2 + 50), "green")

        # Check if Enter is pressed to restart
        if keys[pygame.K_RETURN]:
            reset_game()  # Reset the game state and variables

        pygame.display.update()
