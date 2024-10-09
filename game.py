import pygame
import os
import random
import math
import sys

if len(sys.argv) > 1:
    circle_image_path = sys.argv[1]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


pygame.init()
screen_width, screen_height = 1000, 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("컴키즈의 모험")


font = pygame.font.Font(None, 36)

carrot_image_path = os.path.join("static", "images", "carrot.png")
hellobit_image_path = os.path.join("static", "images", "cat.png")

try:
    carrot_img = pygame.image.load(carrot_image_path)
    cat_img = pygame.image.load(hellobit_image_path)
    circle_img = pygame.image.load(circle_image_path)
except FileNotFoundError as e:
    print(f"이미지를 찾을 수 없습니다: {e}")
    pygame.quit()


def is_collision(center1, radius1, center2, radius2):
    dist = math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)
    return dist < (radius1 + radius2)


def create_circular_image(image, radius):
    mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255, 255), (radius, radius), radius)
    image_scaled = pygame.transform.scale(image, (radius * 2, radius * 2))
    mask.blit(image_scaled, (0, 0), None, pygame.BLEND_RGBA_MIN)
    return mask


def create_carrot():
    x = random.randint(30, screen_width - 30)
    y = random.randint(30, screen_height - 30)
    return (x, y)


cat_radius = 30
carrot_radius = 17
circle_radii = [30, 40, 50]
circle_speeds = [(3, 3), (-4, 4), (5, -5)]


cat_center = (screen_width // 2, screen_height // 2)


carrots = [create_carrot() for _ in range(5)]


circle_centers = [
    (random.randint(100, screen_width - 100), random.randint(100, screen_height - 100))
    for _ in range(3)
]


score = 0
game_over = False


cat_circular = create_circular_image(cat_img, cat_radius)
carrot_circular = create_circular_image(carrot_img, carrot_radius)
circle_circulars = [
    create_circular_image(circle_img, radius) for radius in circle_radii
]


def draw_elements():

    cat_rect = cat_circular.get_rect(center=cat_center)
    screen.blit(cat_circular, cat_rect)

    for carrot_center in carrots:
        carrot_rect = carrot_circular.get_rect(center=carrot_center)
        screen.blit(carrot_circular, carrot_rect)

    for i, circle_center in enumerate(circle_centers):
        circle_rect = circle_circulars[i].get_rect(center=circle_center)
        screen.blit(circle_circulars[i], circle_rect)


def move_hellobit():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return (mouse_x, mouse_y)


def move_circles():
    global circle_centers, circle_speeds, circle_radii, circle_circulars
    for i in range(len(circle_centers)):
        circle_centers[i] = (
            circle_centers[i][0] + circle_speeds[i][0],
            circle_centers[i][1] + circle_speeds[i][1],
        )

        if (circle_centers[i][0] - circle_radii[i] <= 0) or (
            circle_centers[i][0] + circle_radii[i] >= screen_width
        ):
            circle_speeds[i] = (-circle_speeds[i][0], circle_speeds[i][1])
        if (circle_centers[i][1] - circle_radii[i] <= 0) or (
            circle_centers[i][1] + circle_radii[i] >= screen_height
        ):
            circle_speeds[i] = (circle_speeds[i][0], -circle_speeds[i][1])


def check_carrot_collision(cat_center):
    global score, carrots, circle_radii, circle_circulars
    for carrot_center in carrots:
        if is_collision(cat_center, cat_radius, carrot_center, carrot_radius):
            score += 1
            carrots.remove(carrot_center)
            carrots.append(create_carrot())
            for i in range(len(circle_radii)):
                circle_radii[i] = circle_radii[i] * 1.1
                circle_circulars[i] = create_circular_image(
                    circle_img, int(circle_radii[i])
                )
            break


def check_circle_collision(cat_center):
    global game_over
    for i in range(len(circle_centers)):
        if is_collision(cat_center, cat_radius, circle_centers[i], circle_radii[i]):
            game_over = True


def display_game_over():
    game_over_text = font.render(f"Game Over! Score: {score}", True, RED)
    screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 20))

    restart_button = font.render("다시 시작하기", True, WHITE)
    screen.blit(restart_button, (screen_width // 2 - 80, screen_height // 2 + 40))

    quit_button = font.render("게임 종료", True, WHITE)
    screen.blit(quit_button, (screen_width // 2 - 80, screen_height // 2 + 80))

    restart_rect = pygame.Rect(screen_width // 2 - 80, screen_height // 2 + 40, 160, 40)
    quit_rect = pygame.Rect(screen_width // 2 - 80, screen_height // 2 + 80, 160, 40)

    return restart_rect, quit_rect


def game_loop():
    global cat_center, game_over, score
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                restart_rect, quit_rect = display_game_over()
                if restart_rect.collidepoint(mouse_pos):
                    score = 0
                    game_over = False
                    initialize_game()
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return

        if not game_over:
            cat_center = move_hellobit()

            check_carrot_collision(cat_center)

            check_circle_collision(cat_center)

            draw_elements()

            move_circles()

            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            display_game_over()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def initialize_game():
    global cat_center, carrots, circle_centers, circle_radii, circle_circulars, score, game_over

    cat_center = (screen_width // 2, screen_height // 2)

    carrots = [create_carrot() for _ in range(5)]

    circle_centers = [
        (
            random.randint(100, screen_width - 100),
            random.randint(100, screen_height - 100),
        )
        for _ in range(3)
    ]
    circle_radii = [30, 40, 50]
    circle_circulars = [
        create_circular_image(circle_img, radius) for radius in circle_radii
    ]
    score = 0
    game_over = False


if __name__ == "__main__":
    initialize_game()
    game_loop()
