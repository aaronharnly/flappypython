import types

def problem_01(problem, output):
    if isinstance(output['result'], basestring):
        return True
    if type(output['result']) is types.NoneType:
        return "You didn't return anything. Try returning a string."
    if type(output['result']) is not basestring:
        return "You should return a string but you returned a %s." % (type(output['result']).__name__)

def problem_02(problem, output):
    if isinstance(output['result'], bool):
        return True
    if type(output['result']) is types.NoneType:
        return "You didn't return anything. Try returning a boolean."
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


def feedback(problem, output):
    all_attrs = globals()
    if problem.__name__ in all_attrs:
        feedback_function = all_attrs[problem.__name__]
        try:
            problem_feedback = feedback_function(problem, output)
        except Exception as ex:
            problem_feedbdack = str(ex)
        return problem_feedback
    else:
        return None
