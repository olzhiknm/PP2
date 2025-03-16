import pygame
import os

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player & Moving Ball")

WHITE = (255, 255, 255)
RED = (255, 0, 0)


ball_radius = 25
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed = 20

music_files = ["song1.mp3", "song2.mp3", "song3.mp3"]  
current_track = 0

if os.path.exists(music_files[current_track]):
    pygame.mixer.music.load(music_files[current_track])

running = True
while running:
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and ball_y - ball_radius - ball_speed >= 0:
                ball_y -= ball_speed
            elif event.key == pygame.K_DOWN and ball_y + ball_radius + ball_speed <= HEIGHT:
                ball_y += ball_speed
            elif event.key == pygame.K_LEFT and ball_x - ball_radius - ball_speed >= 0:
                ball_x -= ball_speed
            elif event.key == pygame.K_RIGHT and ball_x + ball_radius + ball_speed <= WIDTH:
                ball_x += ball_speed
            elif event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_n:
                current_track = (current_track + 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_track])
                pygame.mixer.music.play()
            elif event.key == pygame.K_p:
                current_track = (current_track - 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_track])
                pygame.mixer.music.play()

pygame.quit()
