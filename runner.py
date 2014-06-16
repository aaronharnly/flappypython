import problem_wrapper
import feedback
import student

def get_problems():
    return sorted([getattr(student, name) for name in dir(student) if name.startswith('problem_')])

def wrap_problems():
    for problem in get_problems():
        wrapped = problem_wrapper.wrapped_problem(problem)
        setattr(student, wrapped.__name__, wrapped)

def show_problem(problem, output):
    if output['feedback'] is True:
        show = "Great job."
    elif output['feedback'] is not None:
        show = output['feedback']
    elif output['error'] is not None:
        show = "Error: %s" % output['error']
    elif output['result'] is None and output['locals'] is None:
        show = "(not started)"
    else:
        show = "Will be graded by the teachers."
    print "%s: %s" % (problem.__name__, show)


def run():
    wrap_problems()
    output = {}
    for problem in get_problems():
        output[problem.__name__] = {}
        try:
            output[problem.__name__]['result'] = problem()
            output[problem.__name__]['error'] = None
            output[problem.__name__]['locals'] = problem.locals
        except Exception as ex:
            output[problem.__name__]['result'] = None
            output[problem.__name__]['locals'] = None
            output[problem.__name__]['error'] = ex
        output[problem.__name__]['feedback'] = feedback.feedback(problem, output[problem.__name__])
        show_problem(problem, output[problem.__name__])

    import game
    game.run(output)
