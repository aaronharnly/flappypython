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
    You should take credit for your great game!

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
    (This problem doesn't change the game. Just getting warmed up.)
    """
    return

def problem_03():
    """
    Time to start the game!

    We want to start the game if the player has pressed the spacebar,
    and we haven't already started the game.

    Complete the function 'should_start_game' below, by using one or more of
    'and', 'or', and 'not' so that we start the game only when the player
    is pressing the spacebar, and the game has NOT already started.
    """
    def should_start_game(player_pressing_spacebar, game_already_started):
        return

def problem_04():
    """
    Your bird needs a place to live!
    See how she is way off to the side right now? Let's fix that.

    Define a variable named 'bird_x' and set it to a number between 0 and 300.
    This will be the location of your bird.

    Some values will make the game very difficult! You probably want the bird
    close to the left side of the screen.
    """
    # Add your code here

def problem_05():
    """
    Now it's time to get things moving.
    Each time we update the screen, we want the pipes to move towards your bird.

    Create a function named 'update_pipes' that takes two parameters:
        'x', and 'speed'.

    'x' is the old location of the pipes.
    'speed' is how fast the pipes move.

    Your function should return the new position of the pipes, which should be:

        the old location + the pipe's speed

    Can you write that using the variables?
    """
    # Add your function here

def problem_06():
    """
    You probably had a hard time getting past the pipes!

    To add a gap into the pipes, we need to write a function that picks a random location
    for the gap. To do that, you need to import the 'random' module.

    In the lines below:

    1. Import the 'random' module

    2. Create a function named 'choose_gap' that calls random.randint()
    with two parameters, to return a random number between those two numbers.
    They should probably be around 50 and 350, but you can experiment.
    """
    # Add your 'import' statement and 'choose_gap' function here


# Congratulations!
# Great job and thank you for a rewarding year.
# Play your game, or you can try changing the numbers at the top of the file 'settings.py'
#
# ###############################################################
#


#
# do not change below
#
if __name__ == '__main__':
    import runner
    runner.run()
