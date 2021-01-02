import subprocess
import sys
modules=['requests','pandas','datetime','matplotlib']
for i in modules:
    subprocess.check_call([sys.executable, "-m", "pip", "install", i])
