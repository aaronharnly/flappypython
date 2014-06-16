"""
This engine drives the game.
"""
import pygame
import sys
import student
import colors
import random

# Settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
TICK_TIME_MS = 100
CAPTION = "Computer Science Final Exam: Flappy Bird"

GRAVITY = 8.0

BIRD_START_VELOCITY_Y = 0
BIRD_JUMP_VELOCITY_Y = -30
BIRD_START_X = 100
BIRD_START_Y = 300
BIRD_WIDTH = 40
BIRD_HEIGHT = 40

OBSTACLE_GAP_X = 0.8 * SCREEN_WIDTH
OBSTACLE_START_X = 1.2 * SCREEN_WIDTH
OBSTACLE_START_VELOCITY_X = -20
OBSTACLE_WIDTH = BIRD_WIDTH
DOOR_HEIGHT = BIRD_HEIGHT * 2.5
DOOR_MINIMUM = BIRD_HEIGHT * 0.5
DOOR_MAXIMUM = SCREEN_HEIGHT - (DOOR_HEIGHT * 1.5)

SCORE_FONT = 'Helvetica,Arial'
SCORE_FONT_SIZE = 40
SCORE_X = 10
SCORE_Y = 10

# Derived settings
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

def create_bird():
    return {
        'x': BIRD_START_X,
        'y': BIRD_START_Y,
        'velocity_y': BIRD_START_VELOCITY_Y
    }

def create_obstacle(x, velocity_x=OBSTACLE_START_VELOCITY_X):
    obstacle = {
        'x': x,
        'velocity_x': velocity_x,
        'door_y': random.randint(DOOR_MINIMUM, DOOR_MAXIMUM),
        'passed': False,
        'newly_passed': False
    }
    return obstacle

def create_obstacles():
    return [
        create_obstacle(OBSTACLE_START_X),
        create_obstacle(OBSTACLE_START_X + OBSTACLE_GAP_X)
    ]

def create_game():
    return {
        'bird': create_bird(),
        'obstacles': create_obstacles(),
        'previous_key': None,
        'current_key': None,
        'score': 0,
        'clock': pygame.time.Clock()
    }

#
# Each of these 'update' functions represents the changes that should happen
# in each 'tick' of the clock.
#
# We can't guarantee that the updates will be called on each tick -- the computer
# may run fast or slow -- so the changes made by these functions are adjusted by the
# number of ticks that have actually passed since the last call.
#
def update_bird_velocity(velocity, key_pressed, time):
    if key_pressed:
        return BIRD_JUMP_VELOCITY_Y
    else:
        return velocity + GRAVITY * time

def update_bird_y(y, velocity, time):
    return y + velocity * time

def update_bird_frame(bird, key_pressed, time):
    bird['velocity_y'] = update_bird_velocity(bird['velocity_y'], key_pressed, time)
    bird['y'] = update_bird_y(bird['y'], bird['velocity_y'], time)
    return bird

def game_is_over(bird, collided):
    return bird['y'] < 0 or bird['y'] > SCREEN_HEIGHT or collided

def update_obstacle_x(x, velocity, time):
    return x + velocity * time

def passed_obstacle(bird, obstacle):
    return obstacle['x'] < bird['x']

def update_score(score, passed_obstacle):
    if passed_obstacle:
        return score + 1
    else:
        return score

def update_obstacle_frame(bird, obstacle, time):
    obstacle['x'] = update_obstacle_x(obstacle['x'], obstacle['velocity_x'], time)
    old_passed = obstacle['passed']
    obstacle['passed'] = passed_obstacle(bird, obstacle)
    obstacle['newly_passed'] = obstacle['passed'] and not old_passed
    return obstacle

def update_game(game):
    """
    Update the background, bird, and obstacles
    """
    time = game['clock'].tick() / float(TICK_TIME_MS)

    # Bird
    key_pressed = game['current_key'] == pygame.K_SPACE and game['previous_key'] is None
    game['bird'] = update_bird_frame(game['bird'], key_pressed, time)

    # Obstacles
    for obstacle in game['obstacles']:
        obstacle = update_obstacle_frame(game['bird'], obstacle, time)

    passed_new_obstacle = any(o['newly_passed'] for o in game['obstacles'])
    game['score'] = update_score(game['score'], passed_new_obstacle)

    if game['obstacles'][0]['x'] + OBSTACLE_WIDTH < 0:
        game['obstacles'].pop(0)
        game['obstacles'].append(create_obstacle(game['obstacles'][0]['x'] + OBSTACLE_GAP_X))

    # Check for game over
    if game_is_over(game['bird'], False):
        game = create_game()

    # Keys
    game['previous_key'] = game['current_key']
    game['current_key'] = None
    return game

def draw_background(screen, resources, game):
    screen.fill(colors.SKY)

def draw_bird(screen, resources, bird):
    pygame.draw.rect(screen, colors.BIRD, [bird['x'], bird['y'], BIRD_WIDTH, BIRD_HEIGHT])

def draw_obstacle(screen, resources, obstacle):
    if obstacle['x'] + OBSTACLE_WIDTH > 0 and obstacle['x'] < SCREEN_WIDTH:
        pygame.draw.rect(screen, colors.OBSTACLE, [obstacle['x'], 0, OBSTACLE_WIDTH, SCREEN_HEIGHT])
        pygame.draw.rect(screen, colors.SKY, [obstacle['x'], obstacle['door_y'],
            OBSTACLE_WIDTH, DOOR_HEIGHT])

def draw_obstacles(screen, resources, obstacles):
    for obstacle in obstacles:
        draw_obstacle(screen, resources, obstacle)

def draw_score(screen, resources, score):
    render = resources['score_font'].render(str(score), 1, colors.SCORE)
    screen.blit(render, (SCORE_X, SCORE_Y))

def draw_screen(screen, resources, game):
    """
    Draw the background, bird, and obstacles
    """
    draw_background(screen, resources, game)
    draw_obstacles(screen, resources, game['obstacles'])
    draw_bird(screen, resources, game['bird'])
    draw_score(screen, resources, game['score'])
    pygame.display.flip()

def create_screen():
    """
    Set up the game screen.

    Returns the screen
    """
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(CAPTION)
    return screen

def create_score_font():
    return pygame.font.SysFont(SCORE_FONT, SCORE_FONT_SIZE)

def create_resources():
    return {
        'screen': create_screen(),
        'score_font': create_score_font()
    }

def run():
    """
    Runs the game.
    """
    resources = create_resources()
    game = create_game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                game['current_key'] = event.key

        game = update_game(game)
        draw_screen(resources['screen'], resources, game)

def quit():
    """
    Exit the game
    """
    pygame.quit()
    print "Thanks for playing!"
    sys.exit()


if __name__ == '__main__':
    run()
