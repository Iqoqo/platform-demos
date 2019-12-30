import tools
from pathlib import Path
import sys

if __name__ == '__main__':
    src = Path(sys.argv[1])
    target = Path('/local/repo/run-result') / src.name
    print(f"{src}->{target}")
    tools.proc_video(src, target)
    print(target.stat())
