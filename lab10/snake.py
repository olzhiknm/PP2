import sqlite3
import pygame
import random

def init_db():
    conn = sqlite3.connect("snake_game.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_score (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        level INTEGER,
        score INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    conn.commit()
    conn.close()

def get_or_create_user(username):
    conn = sqlite3.connect("snake_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
    else:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        user_id = cursor.lastrowid
        cursor.execute("INSERT INTO user_score (user_id, level, score) VALUES (?, ?, ?)", (user_id, 1, 0))
        conn.commit()
    cursor.execute("SELECT level FROM user_score WHERE user_id=?", (user_id,))
    level = cursor.fetchone()[0]
    conn.close()
    return user_id, level

def save_score(user_id, level, score):
    print(f"[SAVE] Saving score: User ID={user_id}, Level={level}, Score={score}")  # отладка
    conn = sqlite3.connect("snake_game.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE user_score SET score=?, level=? WHERE user_id=?", (score, level, user_id))
    conn.commit()
    conn.close()

def get_walls(level):
    walls = []
    if level >= 2:
        walls.append(pygame.Rect(150, 150, 300, 10))
    if level >= 3:
        walls.append(pygame.Rect(150, 250, 300, 10))
    if level >= 4:
        walls.append(pygame.Rect(0, 100, 600, 10))
    return walls

def draw_snake(win, snake_list):
    for segment in snake_list:
        pygame.draw.rect(win, (0, 200, 0), (*segment, 10, 10))

def game_loop(user_id, start_level):
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    font = pygame.font.SysFont("arial", 24)
    clock = pygame.time.Clock()

    x, y = 300, 200
    x_change, y_change = 0, 0
    snake = []
    length = 1
    score = 0
    level = start_level
    food = [random.randint(0, WIDTH//10 - 1)*10, random.randint(0, HEIGHT//10 - 1)*10]
    speed = 10 + level * 2
    wall_rects = get_walls(level)
    running = True
    paused = False

    print("[GAME] Game loop started.")  # отладка

    while running:
        while paused:
            print("[PAUSE] Game is paused.")  # отладка
            win.fill((255, 255, 255))
            pause_text = font.render("Paused. Press 'R' to resume.", True, (0, 0, 0))
            win.blit(pause_text, (150, 180))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_score(user_id, level, score)
                    running = False
                    paused = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[EVENT] Quit event received.")  # отладка
                save_score(user_id, level, score)
                running = False
            if event.type == pygame.KEYDOWN:
                print(f"[KEYDOWN] Key: {event.key}")  # отладка
                if event.key == pygame.K_LEFT:
                    x_change, y_change = -10, 0
                elif event.key == pygame.K_RIGHT:
                    x_change, y_change = 10, 0
                elif event.key == pygame.K_UP:
                    x_change, y_change = 0, -10
                elif event.key == pygame.K_DOWN:
                    x_change, y_change = 0, 10
                elif event.key == pygame.K_p:
                    paused = True
                    save_score(user_id, level, score)

        x += x_change
        y += y_change

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (len(snake) > 1 and [x, y] in snake) or any(pygame.Rect(x, y, 10, 10).colliderect(w) for w in wall_rects):
            print("[COLLISION] Game over condition met.")
            save_score(user_id, level, score)
            running = False

        snake.append([x, y])
        if len(snake) > length:
            del snake[0]

        if [x, y] == food:
            food = [random.randint(0, WIDTH//10 - 1)*10, random.randint(0, HEIGHT//10 - 1)*10]
            length += 1
            score += 10
            print(f"[EAT] Food eaten! Score: {score}, Length: {length}")  # отладка
            if score % 50 == 0:
                level += 1
                print(f"[LEVEL UP] New level: {level}")  # отладка
                wall_rects = get_walls(level)
                speed += 2

        win.fill((0, 0, 0))
        pygame.draw.rect(win, (200, 0, 0), (*food, 10, 10))
        draw_snake(win, snake)
        for wall in wall_rects:
            pygame.draw.rect(win, (255, 255, 255), wall)
        score_text = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
        win.blit(score_text, (10, 10))
        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    init_db()
    username = "player"
    user_id, current_level = get_or_create_user(username)
    print(f"[START] Welcome {username}! Your current level is {current_level}. Starting the game...")
    game_loop(user_id, current_level)
    print("[END] Game Over.")
