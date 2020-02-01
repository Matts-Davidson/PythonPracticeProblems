# Roundabout Operations
# Challenge to solve simple calculations only with functions
# CodeWars

def zero(*args):
    if not args:
        return 0
    else:
        return  eval('0' + args[0])
def one(*args):
    if not args:
        return 1
    else:
        return eval('1' + args[0])
def two(*args):
    if not args:
        return 2
    else:
        return eval('2' + args[0])
def three(*args):
    if not args:
        return 3
    else:
        return eval('3' + args[0])
def four(*args):
    if not args:
        return 4
    else:
        return eval('4' + args[0])
def five(*args):
    if not args:
        return 5
    else:
        return eval('5' + args[0])
def six(*args):
    if not args:
        return 6
    else:
        return eval('6' + args[0])
def seven(*args):
    if not args:
        return 7
    else:
        return eval('7' + args[0])
def eight(*args):
    if not args:
        return 8
    else:
        return eval('8' + args[0])
def nine(*args):
    if not args:
        return 9
    else:
        return eval('9' + args[0])

def plus(num):
    return '+{}'.format(num)
def minus(num):
    return '-{}'.format(num)
def times(num):
    return '*{}'.format(num)
def divided_by(num):
    return '//{}'.format(num)