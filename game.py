"""
This engine drives the game.
"""
import pygame
import sys
import colors
import random
import types
from settings import *

# Derived settings
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

def create_bird(resources):
    return {
        'x': resources['student']['bird_start_x'],
        'y': BIRD_START_Y,
        'velocity_y': BIRD_START_VELOCITY_Y,
        'width': resources['bird_img'].get_width(),
        'height': resources['bird_img'].get_height()
    }

def create_obstacle(resources, x, velocity_x=OBSTACLE_START_VELOCITY_X):
    door_height = resources['bird_img'].get_height() * DOOR_HEIGHT_IN_BIRDS
    #door_minimum = door_height * 0.5
    #door_maximum = SCREEN_HEIGHT - (door_height * 1.5)
    door_y = resources['student']['choose_door']()
    obstacle = {
        'x': x,
        'velocity_x': velocity_x,
        'door_y': door_y,
        'door_height': door_height,
        'passed': False,
        'newly_passed': False,
        'width': resources['obstacle_img'].get_width()
    }
    return obstacle

def create_obstacles(resources):
    return [
        create_obstacle(resources, OBSTACLE_START_X),
        create_obstacle(resources, OBSTACLE_START_X + OBSTACLE_GAP_X)
    ]

def create_clock():
    return pygame.time.Clock()

def create_game(resources):
    return {
        'started': False,
        'bird': create_bird(resources),
        'obstacles': create_obstacles(resources),
        'previous_key': None,
        'current_key': None,
        'score': 0,
        'clock': None
    }

def start_game(game):
    game['clock'] = create_clock()

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

def bird_collided(bird, obstacle):
    x_overlap = bird['x'] + bird['width'] >= obstacle['x'] and bird['x'] <= obstacle['x'] + obstacle['width']
    y_in_door = bird['y'] > obstacle['door_y'] and bird['y'] + bird['height'] < obstacle['door_y'] + obstacle['door_height']
    return x_overlap and not y_in_door

def game_is_over(bird, collided):
    return bird['y'] < 0 or bird['y'] > SCREEN_HEIGHT or collided

def update_obstacle_x(resources, x, velocity, time):
    delta = velocity * time
    new_x = resources['student']['update_obstacle'](x, delta)
    return new_x

def passed_obstacle(bird, obstacle):
    return obstacle['x'] < bird['x']

def update_score(score, passed_obstacle):
    if passed_obstacle:
        return score + 1
    else:
        return score

def update_obstacle_frame(resources, bird, obstacle, time):
    obstacle['x'] = update_obstacle_x(resources, obstacle['x'], obstacle['velocity_x'], time)
    old_passed = obstacle['passed']
    obstacle['passed'] = passed_obstacle(bird, obstacle)
    obstacle['newly_passed'] = obstacle['passed'] and not old_passed
    return obstacle

def update_game(game, resources):
    """
    Update the background, bird, and obstacles
    """
    should_start = resources['student']['should_start_game'](game['current_key'], game['started'])
    if should_start:
        game['started'] = True
        game['current_key'] = None
        game['clock'] = create_clock()
        return game
    elif not game['started']:
        return game

    time = game['clock'].tick() / float(TICK_TIME_MS)

    # Bird
    key_pressed = game['current_key'] == pygame.K_SPACE and game['previous_key'] is None
    game['bird'] = update_bird_frame(game['bird'], key_pressed, time)

    # Obstacles
    for obstacle in game['obstacles']:
        obstacle = update_obstacle_frame(resources, game['bird'], obstacle, time)

    passed_new_obstacle = any(o['newly_passed'] for o in game['obstacles'])
    game['score'] = update_score(game['score'], passed_new_obstacle)

    if game['obstacles'][0]['x'] + game['obstacles'][0]['width'] < 0:
        game['obstacles'].pop(0)
        game['obstacles'].append(create_obstacle(resources, game['obstacles'][0]['x'] + OBSTACLE_GAP_X))

    # Check for game over
    collided = any([bird_collided(game['bird'], obstacle) for obstacle in game['obstacles']])
    if game_is_over(game['bird'], collided):
        game = create_game(resources)

    # Keys
    game['previous_key'] = game['current_key']
    game['current_key'] = None
    return game

def draw_background(screen, resources, game):
    screen.fill(colors.SKY)

def draw_bird(screen, resources, bird):
    bird_img = resources['bird_img']
    #angle = -1 * (float(bird['velocity_y']) / BIRD_MAX_VELOCITY) * BIRD_MAX_ANGLE
    #rotated_img = pygame.transform.rotate(bird_img, angle)
    #pygame.draw.rect(screen, colors.WHITE, [bird['x'], bird['y'], bird['width'], bird['height']])
    screen.blit(bird_img, (bird['x'], bird['y']))

def draw_obstacle(screen, resources, obstacle):
    if obstacle['x'] + obstacle['width'] > 0 and obstacle['x'] < SCREEN_WIDTH:
        obstacle_img = resources['obstacle_img']
        cap_img = resources['obstacle_cap_img']
        # upper section of the pipe
        screen.blit(obstacle_img, (obstacle['x'], 0), area=obstacle_img.get_rect(height=obstacle['door_y']))
        screen.blit(cap_img, (obstacle['x'], obstacle['door_y'] - cap_img.get_height()))
        # lower section of the pipe
        lower_y = obstacle['door_y'] + obstacle['door_height']
        screen.blit(obstacle_img, (obstacle['x'], lower_y))
        screen.blit(cap_img, (obstacle['x'], lower_y))

def draw_obstacles(screen, resources, obstacles):
    for obstacle in obstacles:
        draw_obstacle(screen, resources, obstacle)

def draw_score(screen, resources, score):
    render = resources['score_font'].render(str(score), 1, colors.SCORE)
    screen.blit(render, (SCORE_X, SCORE_Y))

def draw_title(screen, resources):
    author = resources['student']['author']
    render_1 = resources['title_font'].render(TITLE, 1, colors.BLACK)
    render_2 = resources['title_font'].render("By %s" % author, 1, colors.BLACK)
    render_3 = resources['title_font'].render("[press space]", 1, (100, 100, 100))
    screen.blit(render_1, (20, 100))
    screen.blit(render_2, (20, 100 + TITLE_FONT_SIZE))
    screen.blit(render_3, (20, 100 + TITLE_FONT_SIZE*2))

def draw_screen(screen, resources, game):
    """
    Draw the background, bird, and obstacles
    """
    draw_background(screen, resources, game)
    draw_obstacles(screen, resources, game['obstacles'])
    draw_bird(screen, resources, game['bird'])
    draw_score(screen, resources, game['score'])
    if not game['started']:
        draw_title(screen, resources)
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

def create_title_font():
    return pygame.font.SysFont(TITLE_FONT, TITLE_FONT_SIZE)

def create_bird_img():
    img = pygame.image.load(BIRD_IMAGE_FILE)
    img = img.convert()
    colorkey = img.get_at((0, 0))
    img.set_colorkey(colorkey, pygame.RLEACCEL)
    return img

def create_obstacle_img():
    img = pygame.image.load(OBSTACLE_IMAGE_FILE)
    img = img.convert()
    return img

def create_obstacle_cap_img():
    img = pygame.image.load(OBSTACLE_CAP_IMAGE_FILE)
    img = img.convert()
    return img

def _default_update_obstacle(x, velocity):
    return x

def create_working_student():
    return {
        'author': "Your Teachers",
        'should_start_game': lambda a, b: a and not b,
        'bird_start_x': 100,
        'update_obstacle': lambda a, b: a + b,
        'choose_door': lambda: random.randint(50, 350)
    }

def create_student(output):
    if output == 'please':
        return create_working_student()
    update_obstacle = output.get('problem_05', {}).get('locals', {}).get('update_pipes')
    if not isinstance(update_obstacle, types.FunctionType) or not hasattr(update_obstacle, 'arity') or update_obstacle.arity != 2:
        update_obstacle = _default_update_obstacle

    choose_door = output.get('problem_06', {}).get('locals', {}).get('choose_gap')
    if not isinstance(choose_door, types.FunctionType):
        choose_door = lambda: SCREEN_HEIGHT + 100

    return {
        'author': output.get('problem_01', {}).get('result') or '???',
        'should_start_game': output.get('problem_03', {}).get('locals', {}).get('should_start_game') or (lambda x, y: False),
        'bird_start_x': output.get('problem_04', {}).get('locals', {}).get('bird_start_x') or BIRD_START_X,
        'update_obstacle': update_obstacle,
        'choose_door': choose_door
    }

def create_resources(output):
    return {
        'screen': create_screen(),
        'score_font': create_score_font(),
        'title_font': create_title_font(),
        'bird_img': create_bird_img(),
        'obstacle_img': create_obstacle_img(),
        'obstacle_cap_img': create_obstacle_cap_img(),
        'output': output,
        'student': create_student(output)
    }

def run(output=None):
    """
    Runs the game.
    """
    if output is None:
        output = {}
    resources = create_resources(output)
    game = create_game(resources)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                game['current_key'] = event.key

        game = update_game(game, resources)
        draw_screen(resources['screen'], resources, game)

def quit():
    """
    Exit the game
    """
    pygame.quit()
    print "Thanks for playing!"
    sys.exit()


if __name__ == '__main__':
    run('please')
