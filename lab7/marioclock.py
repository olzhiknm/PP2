import pygame
import time
import math


pygame.init()


WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")


clock_image = pygame.image.load("mickeyclock.jpeg")
clock_image = pygame.transform.scale(clock_image, (WIDTH, HEIGHT))


center = (WIDTH // 2, HEIGHT // 2)


minute_hand_length = 100
second_hand_length = 120

running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(clock_image, (0, 0))
    

    current_time = time.localtime()
    minutes = current_time.tm_min
    seconds = current_time.tm_sec
    
    minute_angle = math.radians(-(minutes * 6) + 90)
    second_angle = math.radians(-(seconds * 6) + 90)
    
    minute_end = (center[0] + minute_hand_length * math.cos(minute_angle),
                  center[1] - minute_hand_length * math.sin(minute_angle))
    second_end = (center[0] + second_hand_length * math.cos(second_angle),
                  center[1] - second_hand_length * math.sin(second_angle))
    
    pygame.draw.line(screen, (0, 0, 0), center, minute_end, 8)  
    pygame.draw.line(screen, (255, 0, 0), center, second_end, 4)  
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
