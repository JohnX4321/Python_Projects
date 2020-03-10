import sys,os,ast

def _get_terminal_size():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl,termios,struct
            return struct.unpack('hh',fcntl.ioctl(fd,termios.TIOCGWISE,'1234'))
        except:
            pass

    cr=ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)


    if not cr:
        try:
            with open(os.ctermid()) as fd:
                cr=ioctl_GWINSZ(fd)
        except:
            cr=(os.getenv('LINES',25),os.getenv('COLOURS',80))
    return int(cr[1]),int(cr[0])


def supported_chars(*tests):

    for test in tests:
        try:
            test.encode(sys.stdout.encoding)
            return test
        except UnicodeEncodeError:
            pass
    return '?'*len(tests[0])

def log(*args, trunc=True, m=0):
    if LOGGING and (m in LOGGING_MODES or 0 in LOGGING_MODES):
        args = (str(arg)[:100] + '...' if trunc and len(str(arg)) > 100 else arg for arg in args)
        with open(LOG_FILE, 'a') as f:
            print(*args, file=f)


def in_game_log(string, x, y):
    if IN_GAME_LOGGING:
        print(POS_STR(x, y, string))


def getenv_b(opt):
    """ Converts an enviroment variable into a boolean. """
    o = os.getenv(opt)
    if o:
        return o.lower() in ('true', '1', 'on')


getenv = os.getenv

DEBUG = getenv_b('PYCRAFT_DEBUG')
if os.getenv('PYCRAFT_LOGGING_MODES'):
    LOGGING_MODES = ast.literal_eval(os.getenv('PYCRAFT_LOGGING_MODES'))
else:
    # 0 for all modes
    LOGGING_MODES = [0]

IN_GAME_LOGGING = getenv_b('PYCRAFT_IN_GAME_LOGGING')
LOG_FILE = os.getenv('PYCRAFT_LOG_FILE') or 'pycraft.log'
LOGGING = getenv_b('PYCRAFT_LOGGING')

WIDTH, HEIGHT = _get_terminal_size()
CLS = '\033[2J'
CLS_END = '\033[0J'
CLS_END_LN = '\033[0K'
REDRAW = '\033[0;0f'
HIDE_CUR = '\033[?25l'
SHOW_CUR = '\033[?25h'
POS_STR = lambda x, y, s: '\033[{};{}H{}'.format(y+1, x+1, s)

if LOGGING:
    open(LOG_FILE, 'w').close()
