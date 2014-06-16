import types

def problem_01(problem, output):
    if output['error']:
        return "Error: %s" % output['error']
    if isinstance(output['result'], basestring):
        return True
    if type(output['result']) is types.NoneType:
        return "You didn't return anything. Try returning a string."
    if type(output['result']) is not basestring:
        return "You should return a string but you returned a %s." % (type(output['result']).__name__)


def feedback(problem, output):
    all_attrs = globals()
    if problem.__name__ in all_attrs:
        feedback_function = all_attrs[problem.__name__]
        problem_feedback = feedback_function(problem, output)
        return problem_feedback
    else:
        return None
