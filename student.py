"""
Congratulations on finishing Computer Science!

In this last class you will show your knowledge of Python programming
by completing short exercises.

As you complete each exercise, run this file -- each completed function
will make the Flappy Bird game run a bit better.
"""
#
# Problem 1
#
def problem_01():
    """
    You need to take credit for your game!

    Show that you understand strings by changing this function
    so that it returns a string.

    Then save and run this file, and see your name in the title screen.
    """
    return


def problem_02():
    """
    Booleans are used everywhere in computer science and programming.

    Show that you understand booleans by changing this function
    so that it returns a boolean.

    (Hint: there are two correct answers!)
    """
    return

def problem_03():
    """
    We want to start the game if the player has pressed the spacebar,
    and we haven't already started the game.

    Complete the function 'should_start_game' below, by using one or more of
    'and', 'or', and 'not' so that we start the game only when the player
    is pressing the spacebar, and the game has NOT already started.
    """
    def should_start_game(player_pressing_spacebar, game_already_started):
        return player_pressing_spacebar and not game_already_started


def problem_04():
    """
    We use variables to store values.

    Define a variable named 'bird_x' and set it to a number between 0 and 300.
    This will be the location of your bird.

    Some values will make the game very difficult! You probably want the bird
    close to the left side of the screen.
    """
    # Add your code here
    bird_start_x = 300

#
# do not change below
#
if __name__ == '__main__':
    import runner
    runner.run()
