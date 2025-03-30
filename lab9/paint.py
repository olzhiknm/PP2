import pygame
import math

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App - Lab 9")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
colors = [BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255)]
current_color = BLACK
tool = "brush"

screen.fill(WHITE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)


def draw_ui():
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, 30))
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (10 + i*40, 5, 30, 20))
    tools = ["brush", "rect", "circle", "eraser", "square", "rtriangle", "etriangle", "rhombus"]
    for i, t in enumerate(tools):
        text = font.render(t, True, BLACK)
        screen.blit(text, (200 + i*70, 5))

start_pos = None

def draw_shape(tool, start, end):
    x1, y1 = start
    x2, y2 = end
    if tool == "rect":
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        pygame.draw.rect(screen, current_color, rect, 2)
    elif tool == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(screen, current_color, start, radius, 2)
    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(x1, y1, side if x2 > x1 else -side, side if y2 > y1 else -side)
        pygame.draw.rect(screen, current_color, rect, 2)
    elif tool == "rtriangle":
        points = [start, (x1, y2), (x2, y2)]
        pygame.draw.polygon(screen, current_color, points, 2)
    elif tool == "etriangle":
        height = abs(y2 - y1)
        half_base = height // math.sqrt(3)
        points = [(x1, y2), (x1 + half_base, y1), (x1 + 2 * half_base, y2)]
        pygame.draw.polygon(screen, current_color, points, 2)
    elif tool == "rhombus":
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
        pygame.draw.polygon(screen, current_color, points, 2)

running = True
while running:
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < 30:
                for i in range(len(colors)):
                    if 10 + i*40 < x < 40 + i*40:
                        current_color = colors[i]
                tools = ["brush", "rect", "circle", "eraser", "square", "rtriangle", "etriangle", "rhombus"]
                for i, t in enumerate(tools):
                    if 200 + i*70 < x < 200 + i*70 + 60:
                        tool = t
            else:
                start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if start_pos:
                end_pos = event.pos
                draw_shape(tool, start_pos, end_pos)
                start_pos = None

    if pygame.mouse.get_pressed()[0]:
        if tool == "brush":
            pygame.draw.circle(screen, current_color, pygame.mouse.get_pos(), 4)
        elif tool == "eraser":
            pygame.draw.circle(screen, WHITE, pygame.mouse.get_pos(), 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
