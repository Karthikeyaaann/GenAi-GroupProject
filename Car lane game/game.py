import cv2
import mediapipe as mp
import pygame
import random
import sys

pygame.init()

# -------------------- Game Window --------------------
WIDTH, HEIGHT = 500, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand-Controlled Racing Car")

# Colors
WHITE = (255, 255, 255)
ROAD_COLOR = (40, 40, 40)
ROAD_EDGE_COLOR = (20, 20, 20)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Car options
CAR_OPTIONS = [
    pygame.transform.scale(pygame.image.load("player_car.png"), (50, 100)),
    pygame.transform.scale(pygame.image.load("player_car2.png"), (50, 100)),
    pygame.transform.scale(pygame.image.load("player_car3.png"), (50, 100)),
]

ENEMY_CAR = pygame.transform.scale(pygame.image.load("enemy_car.png"), (50, 100))

# -------------------- Game Variables --------------------
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 120
enemy_speed = 4
spawn_interval = 1200
last_spawn_time = pygame.time.get_ticks()
score = 0
game_over = False
game_won = False
enemies = []
lane_lines = [i for i in range(0, HEIGHT, 50)]
white_line_timer = 0
level = 1
combo_dodges = 0

# New: Distance & Finish line
distance_to_finish = 5000  # total "road length"
finish_line_y = -5000  # start far above the screen

# -------------------- Mediapipe Setup --------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

font = pygame.font.Font(None, 50)

# -------------------- CAR SELECTION SCREEN --------------------
def car_selection_screen():
    selected_index = 0
    selecting = True
    while selecting:
        WINDOW.fill((0, 0, 0))
        title = font.render("Select Your Car", True, YELLOW)
        WINDOW.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        for i, car in enumerate(CAR_OPTIONS):
            x = WIDTH//2 - (len(CAR_OPTIONS)*80)//2 + i*80
            y = HEIGHT//2
            WINDOW.blit(car, (x, y))
            if i == selected_index:
                pygame.draw.rect(WINDOW, YELLOW, (x-5, y-5, 60, 110), 3)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(CAR_OPTIONS)
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(CAR_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    return CAR_OPTIONS[selected_index]

PLAYER_CAR = car_selection_screen()

# -------------------- GAME FUNCTIONS --------------------
def draw_finish_line(y_pos):
    """Draw a checkered finish line"""
    block_size = 20
    for row in range(2):  # two rows of checkers
        for col in range(12):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(WINDOW, color,
                             (WIDTH//6 + col*block_size, y_pos + row*block_size, block_size, block_size))

def draw_window():
    WINDOW.fill(ROAD_COLOR)

    # Road edges
    edge_width = 60
    pygame.draw.rect(WINDOW, ROAD_EDGE_COLOR, (0, 0, edge_width, HEIGHT))
    pygame.draw.rect(WINDOW, ROAD_EDGE_COLOR, (WIDTH-edge_width, 0, edge_width, HEIGHT))

    # Lane lines
    for i in lane_lines:
        pygame.draw.rect(WINDOW, WHITE, (WIDTH//3 - 7, i, 15, 40), border_radius=3)
        pygame.draw.rect(WINDOW, WHITE, (2*WIDTH//3 - 7, i, 15, 40), border_radius=3)

    # Animate lane lines
    for idx in range(len(lane_lines)):
        lane_lines[idx] += 10
        if lane_lines[idx] > HEIGHT:
            lane_lines[idx] = -50

    # Draw finish line if near
    if finish_line_y < HEIGHT:
        draw_finish_line(finish_line_y)

    # Draw player and enemies
    WINDOW.blit(PLAYER_CAR, (player_x, player_y))
    for e in enemies:
        WINDOW.blit(ENEMY_CAR, (e["x"], e["y"]))

    # Score, level, distance
    score_text = font.render(f"Score: {score}", True, YELLOW)
    WINDOW.blit(score_text, (10, 10))
    level_text = font.render(f"Level: {level}", True, GREEN)
    WINDOW.blit(level_text, (10, 60))
    distance_text = font.render(f"Dist: {max(0, distance_to_finish)}", True, WHITE)
    WINDOW.blit(distance_text, (10, 110))

    if game_over:
        game_over_text = font.render("GAME OVER! Press R to restart", True, RED)
        WINDOW.blit(game_over_text, (30, HEIGHT//2 - 50))

    if game_won:
        win_text = font.render("YOU WON! Press R to restart", True, GREEN)
        WINDOW.blit(win_text, (40, HEIGHT//2 - 50))

    pygame.display.update()

def restart_game():
    global score, enemies, game_over, game_won, enemy_speed, spawn_interval
    global level, white_line_timer, combo_dodges, distance_to_finish, finish_line_y
    score = 0
    enemies = []
    game_over = False
    game_won = False
    enemy_speed = 4
    spawn_interval = 1200
    level = 1
    white_line_timer = 0
    combo_dodges = 0
    distance_to_finish = 5000
    finish_line_y = -5000

# -------------------- FIXED SPAWN ENEMY --------------------
def spawn_enemy():
    global enemies, last_spawn_time
    lane_positions = [WIDTH//4 - 25, WIDTH//2 - 25, 3*WIDTH//4 - 25]

    if not any(e["y"] < 120 for e in enemies):  # avoid stacking at top
        num_to_spawn = random.choice([1, 2])  # spawn 1 or 2 enemies
        lanes_to_spawn = random.sample(lane_positions, num_to_spawn)

        # Guarantee at least one lane is always open
        if len(lanes_to_spawn) == 3:
            lanes_to_spawn.pop()

        for lane in lanes_to_spawn:
            enemies.append({"x": lane, "y": -100})

        last_spawn_time = pygame.time.get_ticks()

# -------------------- MAIN GAME LOOP --------------------
clock = pygame.time.Clock()

while True:
    clock.tick(30)
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            frame_width = frame.shape[1]
            finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame_width
            player_x = int(finger_x * (WIDTH / frame_width))
            player_x = max(WIDTH//6, min(player_x, WIDTH - WIDTH//6 - 50))

    # White line restriction (road divider)
    middle_line_x = WIDTH//2 - 7
    if middle_line_x <= player_x + 25 <= middle_line_x + 14:
        white_line_timer += clock.get_time()
        if white_line_timer > 2000:
            game_over = True
    else:
        white_line_timer = 0

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if not game_over and not game_won:
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_interval:
            spawn_enemy()

        for e in enemies:
            e["y"] += enemy_speed

        # Collision detection
        for e in enemies:
            if player_y < e["y"] + 100 and player_y + 100 > e["y"]:
                if player_x < e["x"] + 50 and player_x + 50 > e["x"]:
                    game_over = True

        # Check for dodged enemies
        dodged = [e for e in enemies if e["y"] > HEIGHT]
        for e in dodged:
            combo_dodges += 1
            bonus = 5 if combo_dodges % 3 == 0 else 1
            score += bonus
            enemies.remove(e)

        score += 1
        if score % 200 == 0:
            enemy_speed += 1
            spawn_interval = max(400, spawn_interval - 100)
            level += 1

        # Move finish line closer
        distance_to_finish -= 10
        finish_line_y += 10

        # Win condition → player reaches finish line
        if distance_to_finish <= 0 and finish_line_y >= player_y - 50:
            game_won = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or game_won):
                restart_game()

    draw_window()
