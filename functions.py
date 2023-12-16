import sys
from typing import Any


def sys_print(*args:Any, sep:str = '\n'):
	sys.stdout.write(sep.join(map(str, args)) + '\n')
	sys.stdout.flush()
