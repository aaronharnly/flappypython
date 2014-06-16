import types
import inspect

def problem_01(problem, output):
    if isinstance(output['result'], basestring):
        return True
    if type(output['result']) is types.NoneType:
        return "(not started yet)"
    if type(output['result']) is not basestring:
        return "You should return a string but you returned a %s." % (type(output['result']).__name__)

def problem_02(problem, output):
    if isinstance(output['result'], bool):
        return True
    if type(output['result']) is types.NoneType:
        return "(not started yet)"
    if type(output['result']) is not basestring:
        return "You should return a string but you returned a %s." % (type(output['result']).__name__)

def problem_03(problem, output):
    if 'should_start_game' not in output['locals']:
        return "Uh oh, what happened to the 'should_start_game' function? Put it back!"
    ssg = output['locals']['should_start_game']
    if not isinstance(ssg, types.FunctionType):
        return "should_start_game should be a function."
    # check the output
    if type(ssg(False, False)) is types.NoneType:
        return "(not started yet)"
    if ssg(False, False) or ssg(False, True):
        return "The game should NOT start if the user is not pressing the spacebar!"
    if ssg(True, True):
        return "The game should NOT start if it is already started!"
    if not ssg(True, False):
        return "The game *should* start if the user is pressing the spacebar, and the game hasn't started."
    return True

def problem_04(problem, output):
    if output['locals'] == {}:
        return "(not started yet)"
    if 'bird_start_x' not in output['locals'] and 'bird_start_x' in [x.lower() for x in output['locals']]:
        return "Check your capitalization! The variable should be named 'bird_start_x'"
    if 'bird_start_x' not in output['locals']:
        return "The variable should be named 'bird_start_x'"
    if not(isinstance(output['locals']['bird_start_x'], int)):
        return "bird_start_x should be an integer."
    if output['locals']['bird_start_x'] < 0:
        return "bird_start_x should be greater than 0"
    if output['locals']['bird_start_x'] > 300:
        return "bird_start_x should be less than 300"
    return True

def problem_05(problem, output):
    if not output['locals']:
        return "(not started yet)"
    if 'update_pipes' not in output['locals']:
        return "No 'update_pipes' function defined. Check your spelling?"
    up = output['locals']['update_pipes']
    if not isinstance(up, types.FunctionType):
        return "update_pipes should be a function."
    argspec = inspect.getargspec(up)
    arity = len(argspec[0])
    up.arity = arity
    if arity < 2 or arity > 2:
        return "The function update_pipes should take 2 parameters. You have %s" % arity
    if up(1000, 2) != 1002:
        return "Check your formula. It should be: the old location + the pipe's speed"
    if up(0, 5) != 5:
        return "Check your formula. It should be: the old location + the pipe's speed"
    if up(-10, 2) != -8:
        return "Check your formula. It should be: the old location + the pipe's speed"
    if up(1000, -6) != 994:
        return "Check your formula. It should be: the old location + the pipe's speed"
    return True


def problem_06(problem, output):
    if not output['locals']:
        return "(not started yet)"
    if 'random' not in output['locals']:
        return "Have you imported 'random'?"
    if 'choose_gap' not in output['locals']:
        return "No 'choose_gap' function defined. Make sure you define the function."
    cg = output['locals']['choose_gap']
    if not isinstance(cg, types.FunctionType):
        return "choose_gap should be a function."
    argspec = inspect.getargspec(cg)
    arity = len(argspec[0])
    cg.arity = arity
    if arity > 0:
        return "The function choose_gap should not take parameters. You have %s" % arity
    return True


def feedback(problem, output):
    all_attrs = globals()
    if problem.__name__ in all_attrs:
        feedback_function = all_attrs[problem.__name__]
        try:
            problem_feedback = feedback_function(problem, output)
        except Exception as ex:
            problem_feedback = str(ex)
        return problem_feedback
    else:
        return None
