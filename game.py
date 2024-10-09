import pygame
import os
import random
import math
import sys

if len(sys.argv) > 1:
    circle_image_path = sys.argv[1]
# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 초기화
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("컴키즈의 모험")

# 글꼴 설정
font = pygame.font.Font(None, 36)

# 이미지 경로 설정 (상대경로)
carrot_image_path = os.path.join("static", "images", "carrot.png")
hellobit_image_path = os.path.join("static", "images", "cat.png")

# 이미지 로드
try:
    carrot_img = pygame.image.load(carrot_image_path)
    cat_img = pygame.image.load(hellobit_image_path)
    circle_img = pygame.image.load(circle_image_path)  # 전달받은 경로에서 이미지 로드
except FileNotFoundError as e:
    print(f"이미지를 찾을 수 없습니다: {e}")
    pygame.quit()


# 원형 충돌 감지 함수
def is_collision(center1, radius1, center2, radius2):
    dist = math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)
    return dist < (radius1 + radius2)


# 이미지 원형으로 자르기
def create_circular_image(image, radius):
    mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255, 255), (radius, radius), radius)
    image_scaled = pygame.transform.scale(image, (radius * 2, radius * 2))
    mask.blit(image_scaled, (0, 0), None, pygame.BLEND_RGBA_MIN)
    return mask


# 당근 위치를 랜덤으로 생성
def create_carrot():
    x = random.randint(30, screen_width - 30)
    y = random.randint(30, screen_height - 30)
    return (x, y)


# 헬로빗, 당근, 동그라미 초기 설정
cat_radius = 30
carrot_radius = 17
circle_radii = [30, 40, 50]
circle_speeds = [(3, 3), (-4, 4), (5, -5)]  # 동그라미 속도

# 헬로빗 초기 위치 설정
cat_center = (screen_width // 2, screen_height // 2)

# 당근 5개 위치 설정
carrots = [create_carrot() for _ in range(5)]

# 동그라미 3개 위치 설정
circle_centers = [
    (random.randint(100, screen_width - 100), random.randint(100, screen_height - 100))
    for _ in range(3)
]

# 점수 초기화
score = 0
game_over = False

# 원형 이미지 생성
cat_circular = create_circular_image(cat_img, cat_radius)
carrot_circular = create_circular_image(carrot_img, carrot_radius)
circle_circulars = [
    create_circular_image(circle_img, radius) for radius in circle_radii
]


def draw_elements():
    # 헬로빗 그리기
    cat_rect = cat_circular.get_rect(center=cat_center)
    screen.blit(cat_circular, cat_rect)

    # 당근 그리기
    for carrot_center in carrots:
        carrot_rect = carrot_circular.get_rect(center=carrot_center)
        screen.blit(carrot_circular, carrot_rect)

    # 동그라미 그리기
    for i, circle_center in enumerate(circle_centers):
        circle_rect = circle_circulars[i].get_rect(center=circle_center)
        screen.blit(circle_circulars[i], circle_rect)


def move_hellobit():
    # 마우스 포인터를 따라 헬로빗 이동
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return (mouse_x, mouse_y)


def move_circles():
    global circle_centers, circle_speeds, circle_radii, circle_circulars
    for i in range(len(circle_centers)):
        circle_centers[i] = (
            circle_centers[i][0] + circle_speeds[i][0],
            circle_centers[i][1] + circle_speeds[i][1],
        )

        # 벽에 부딪히면 반사
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
            score += 1  # 점수 증가
            carrots.remove(carrot_center)  # 당근 제거
            carrots.append(create_carrot())  # 새 당근 추가
            # 동그라미 크기 증가
            for i in range(len(circle_radii)):
                circle_radii[i] = circle_radii[i] * 1.1  # 동그라미 크기를 1.1배로 키움
                circle_circulars[i] = create_circular_image(
                    circle_img, int(circle_radii[i])
                )
            break


def check_circle_collision(cat_center):
    global game_over
    for i in range(len(circle_centers)):
        if is_collision(cat_center, cat_radius, circle_centers[i], circle_radii[i]):
            game_over = True  # 동그라미와 충돌 시 게임 종료


def display_game_over():
    # 게임 종료 메시지 표시
    game_over_text = font.render(f"Game Over! Score: {score}", True, RED)
    screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 20))

    # 다시 시작 버튼 그리기
    restart_button = font.render("다시 시작하기", True, WHITE)
    screen.blit(restart_button, (screen_width // 2 - 80, screen_height // 2 + 40))

    # 게임 종료 버튼 그리기
    quit_button = font.render("게임 종료", True, WHITE)
    screen.blit(quit_button, (screen_width // 2 - 80, screen_height // 2 + 80))

    # 버튼 영역 리턴 (재시작 및 종료)
    restart_rect = pygame.Rect(screen_width // 2 - 80, screen_height // 2 + 40, 160, 40)
    quit_rect = pygame.Rect(screen_width // 2 - 80, screen_height // 2 + 80, 160, 40)

    return restart_rect, quit_rect


# 게임 루프
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
                    # 게임 재시작
                    score = 0
                    game_over = False
                    initialize_game()
                elif quit_rect.collidepoint(mouse_pos):
                    # 게임 종료
                    pygame.quit()
                    return

        if not game_over:
            # 헬로빗 이동
            cat_center = move_hellobit()

            # 당근과 충돌 확인 및 점수 증가
            check_carrot_collision(cat_center)

            # 동그라미와 충돌 확인
            check_circle_collision(cat_center)

            # 원 그리기 (헬로빗, 당근, 동그라미)
            draw_elements()

            # 동그라미 움직임
            move_circles()

            # 점수 표시
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            display_game_over()

        # 화면 업데이트
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def initialize_game():
    global cat_center, carrots, circle_centers, circle_radii, circle_circulars, score, game_over
    # 헬로빗 초기화
    cat_center = (screen_width // 2, screen_height // 2)
    # 당근 5개 위치 초기화
    # 당근 5개 위치 초기화
    carrots = [create_carrot() for _ in range(5)]
    # 동그라미 3개 초기화
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
