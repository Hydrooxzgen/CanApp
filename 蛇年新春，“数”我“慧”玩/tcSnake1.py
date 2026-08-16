import pygame
import random
import time
import sys
import tkinter.messagebox as box
import webbrowser

stopping = False
pygame.init()
# 定义常量
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# 设置窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 设置字体
font = pygame.font.SysFont("Microsoft YaHei UI", 30)
small_font = pygame.font.SysFont("Microsoft YaHei UI", 20)

# 游戏变量
snake = [(100, 100), (80, 100), (60, 100)]  # 蛇
snake_direction = 'RIGHT'  # 初始方向
snake_speed = 4 # 初始速度
score = 0  # 积分

# 难度控制
difficulty = 'EASY'
difficulty_speed = {'EASY': 4, 'MEDIUM': 12, 'HARD': 15}

# 食物
food = []
food_type = []  # True for big food, False for small food
food_equations = []

def display_message(msg, color, y_offset=0):
    message = font.render(msg, True, color)
    screen.blit(message, [WIDTH / 2 - message.get_width() / 2, HEIGHT / 2 + y_offset])

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, RED, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))


def draw_food():
    for i in range(len(food)):
        # 获取食物位置
        food_x, food_y = food[i]

        if food_type[i]:  # 大食物 (橙色)
            pygame.draw.rect(screen, ORANGE, pygame.Rect(food_x, food_y, BLOCK_SIZE * 1, BLOCK_SIZE * 1))
        else:  # 小食物 (绿色)
            pygame.draw.rect(screen, GREEN, pygame.Rect(food_x, food_y, BLOCK_SIZE, BLOCK_SIZE))

        # 显示数学公式，确保公式在食物的正中间
        eq_text = small_font.render(food_equations[i], True, BLACK)

        # 计算公式显示位置，确保公式不会超出屏幕范围
        eq_x = food_x + (BLOCK_SIZE if not food_type[i] else BLOCK_SIZE * 2) / 2 - eq_text.get_width() / 2
        eq_y = food_y + (BLOCK_SIZE if not food_type[i] else BLOCK_SIZE * 2) / 2 - eq_text.get_height() / 2

        # 如果公式位置超出屏幕，调整位置
        eq_x = max(0, min(eq_x, WIDTH - eq_text.get_width()))
        eq_y = max(0, min(eq_y, HEIGHT - eq_text.get_height()))

        screen.blit(eq_text, [eq_x, eq_y])
def check_collision(x, y):
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True  # Collide with walls
    if (x, y) in snake:
        return True  # Collide with itself
    return False

def generate_food():
    global food, food_type, food_equations
    food.clear()
    food_type.clear()
    food_equations.clear()

    big_food = 2  # 每次生成2个大食物
    small_food_count = random.randint(3, 7)  # 小食物数量为3-7个

    # 生成大食物（大食物占4个格子）
    for _ in range(big_food):
        x = random.randint(1, (WIDTH - BLOCK_SIZE * 1) // BLOCK_SIZE) * BLOCK_SIZE  # 2个格子的起始位置
        y = random.randint(1, (HEIGHT - BLOCK_SIZE * 1) // BLOCK_SIZE) * BLOCK_SIZE  # 2个格子的起始位置
        food.append((x, y))
        food_type.append(True)  # 大食物
        food_equations.append(generate_math_equation(difficulty, True))

    # 生成小食物
    for _ in range(small_food_count):
        x = random.randint(1, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(1, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food.append((x, y))
        food_type.append(False)  # 小食物
        food_equations.append(generate_math_equation(difficulty, False))

    # 确保大食物和小食物的公式中有正确和错误的组合
    # 大食物至少有1个正确，1个错误
    correct_big_food = random.choice([True, False])  # 至少有一个大食物公式正确
    # 小食物至少有1个正确，其他是错误的
    correct_small_foods = random.sample(range(small_food_count), 1)  # 至少1个小食物公式正确

    # 生成大食物公式（一个正确，另一个错误）
    for i in range(big_food):
        if (i == 0 and correct_big_food) or (i == 1 and not correct_big_food):
            food_equations[i] = generate_math_equation(difficulty, True, correct=True)
        else:
            food_equations[i] = generate_math_equation(difficulty, True, correct=False)

    # 生成小食物公式（至少两个错误）
    for i in range(small_food_count):
        if i in correct_small_foods:
            food_equations[big_food + i] = generate_math_equation(difficulty, False, correct=True)
        else:
            food_equations[big_food + i] = generate_math_equation(difficulty, False, correct=False)

def generate_math_equation(difficulty, is_big_food, correct=True):
    # 生成不同难度的数学公式
    if is_big_food:
        # 更难的大食物公式
        if difficulty == 'EASY':
            num1 = random.randint(1, 5)
            num2 = random.randint(1, 5)
            answer = num1 + num2
            equation = f"{num1} + {num2} = {answer}"
        elif difficulty == 'MEDIUM':
            num1 = random.randint(5, 10)
            num2 = random.randint(1, 5)
            answer = num1 - num2
            equation = f"{num1} - {num2} = {answer}"
        else:  # HARD
            num1 = random.randint(10, 20)
            num2 = random.randint(1, 3)
            answer = num1 * num2
            equation = f"{num1} * {num2} = {answer}"

    else:
        # 相对简单的小食物公式
        if difficulty == 'EASY':
            num1 = random.randint(1, 5)
            num2 = random.randint(1, 5)
            answer = num1 + num2
            equation = f"{num1} + {num2} = {answer}"
        elif difficulty == 'MEDIUM':
            num1 = random.randint(3, 8)
            num2 = random.randint(1, 3)
            answer = num1 * num2
            equation = f"{num1} * {num2} = {answer}"
        else:  # HARD
            num1 = random.randint(5, 10)
            num2 = random.randint(5, 10)
            answer = num1 + num2
            equation = f"{num1} + {num2} = {answer}"

    # 如果需要错误的公式，改变结果
    if not correct:
        # 解析公式中的数字
        parts = equation.split("=")
        expression = parts[0].strip()  # 获取表达式部分
        numbers = [int(n) for n in expression.split() if n.isdigit()]  # 提取数字

        if len(numbers) == 2:  # 如果公式有两个数字
            num1, num2 = numbers
            if "+" in expression:
                wrong_answer = random.randint(num1 + num2 - 5, num1 + num2 + 5)
            elif "-" in expression:
                wrong_answer = random.randint(num1 - num2 - 5, num1 - num2 + 5)
            elif "*" in expression:
                wrong_answer = random.randint(num1 * num2 - 5, num1 * num2 + 5)
            equation = f"{num1} {expression.split()[1]} {num2} = {wrong_answer}"
        else:
            # 对于一些异常情况，直接给出错误公式
            wrong_answer = random.randint(0, 20)
            equation = f"{expression} = {wrong_answer}"

    return equation


def evaluate_math_answer(food_index, answer):
    equation = food_equations[food_index]
    parts = equation.split('=')
    correct_answer = eval(parts[0])
    if int(parts[1].strip()) == correct_answer:
        return True
    return False

def game_over(why=''):
    display_message(f"你失败了！你{why}而死", RED, 0)
    pygame.display.update()
    time.sleep(2)

def check_food_collision(snake_head, food, food_type, food_equations):
    """检查蛇头与食物的碰撞，确保蛇可以吃到食物"""
    for i, food_pos in enumerate(food):
        if food_type[i]:  # 大食物
            # 大食物占用一个 2x2 的区域，确保蛇头与这个区域的任意部分重叠
            food_x, food_y = food_pos
            for dx in range(2):  # 大食物横向占用2格
                for dy in range(2):  # 大食物纵向占用2格
                    if (snake_head[0] == food_x + dx * BLOCK_SIZE and
                        snake_head[1] == food_y + dy * BLOCK_SIZE):
                        return i  # 返回食物的索引
        else:  # 小食物（占用一个格子）
            if snake_head == food_pos:
                return i  # 返回食物的索引
    return -1  # 没有吃到任何食物

# 游戏主循环
def game_loop():
    global stopping
    global snake, snake_direction, score, food, food_type, food_equations, snake_speed
    snake = [(100, 100), (80, 100), (60, 100)]
    snake_direction = 'RIGHT'
    score = 0
    generate_food()

    clock = pygame.time.Clock()
    game_running = True

    while game_running:
        screen.fill(WHITE)
        draw_snake(snake)
        draw_food()

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                box.showinfo('正在打开验证页面....', '你需要填写为何退出程序，通过后将会退出。')
                webbrowser.open('https://tanweibo.github.io/tcSnake/verify/why_exit', new=2)
                game_running = True
                # box.showinfo('Game Over', f'你得分：{score}')
                # game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    snake_direction = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    snake_direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    snake_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    snake_direction = 'RIGHT'
                elif event.key == pygame.K_F5:
                    box.showinfo('重新开始', '点击确认键重新开始')


        # Snake movement
        head_x, head_y = snake[0]
        if snake_direction == 'UP':
            head_y -= BLOCK_SIZE
        elif snake_direction == 'DOWN':
            head_y += BLOCK_SIZE
        elif snake_direction == 'LEFT':
            head_x -= BLOCK_SIZE
        elif snake_direction == 'RIGHT':
            head_x += BLOCK_SIZE

        if check_collision(head_x, head_y):
            game_over('撞到自身或墙')
            game_running = False
            continue

        snake.insert(0, (head_x, head_y))

        # Check food collision
        food_eaten = False
        for i in range(len(food)):
            if (head_x, head_y) == food[i]:
                if food_type[i]:  # Big food
                    if evaluate_math_answer(i, food_equations[i]):
                        score += 5
                    else:
                        score -= 5
                else:  # Small food
                    if evaluate_math_answer(i, food_equations[i]):
                        score += 1
                    else:
                        score -= 2

                food.pop(i)
                food_type.pop(i)
                food_equations.pop(i)
                food_eaten = True
                break

        if food_eaten:
            generate_food()

        # Remove snake tail if no food eaten
        if not food_eaten:
            snake.pop()

        # Update score and speed
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, [10, 10])

        # If score is negative, game over
        if score < 0:
            game_over('分数过低')
            game_running = False

        pygame.display.update()
        clock.tick(snake_speed + difficulty_speed[difficulty])
        # 判断蛇是否吃到食物
    food_index = check_food_collision(snake[0], food, food_type, food_equations)
    if food_index != -1:
        food_type_taken = food_type[food_index]
        correct_formula = food_equations[food_index]  # 获取食物的数学公式正确性

        if correct_formula:  # 如果公式是正确的
            if food_type_taken:  # 吃到正确的大食物
                score += 5
            else:  # 吃到正确的小食物
                score += 1
        else:  # 如果公式是错误的
            if food_type_taken:  # 吃到错误的大食物
                score -= 5
            else:  # 吃到错误的小食物
                score -= 2

        # 更新食物和公式
        food.pop(food_index)
        food_type.pop(food_index)
        food_equations.pop(food_index)

        # 重新生成食物
        generate_food()
# 开始游戏
def main_menu():
    global difficulty
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        display_message("贪吃蛇", BLACK, -50)
        easy_button = pygame.Rect(WIDTH / 4 - 100, HEIGHT / 2 - 50, 200, 50)
        medium_button = pygame.Rect(WIDTH / 4 - 100, HEIGHT / 2 + 10, 200, 50)
        hard_button = pygame.Rect(WIDTH / 4 - 100, HEIGHT / 2 + 70, 200, 50)

        pygame.draw.rect(screen, BLACK, easy_button)
        pygame.draw.rect(screen, BLACK, medium_button)
        pygame.draw.rect(screen, BLACK, hard_button)

        easy_text = font.render("简单", True, WHITE)
        medium_text = font.render("中等", True, WHITE)
        hard_text = font.render("困难", True, WHITE)

        screen.blit(easy_text, (WIDTH / 4, HEIGHT / 2 - 40))
        screen.blit(medium_text, (WIDTH / 4, HEIGHT / 2 + 20))
        screen.blit(hard_text, (WIDTH / 4, HEIGHT / 2 + 80))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    difficulty = 'EASY'
                    game_loop()
                elif medium_button.collidepoint(event.pos):
                    difficulty = 'MEDIUM'
                    game_loop()
                elif hard_button.collidepoint(event.pos):
                    difficulty = 'HARD'
                    game_loop()
    pygame.quit()
    return

if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()
