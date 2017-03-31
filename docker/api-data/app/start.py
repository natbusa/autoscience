import sys
import os,subprocess

# respectively to file, /dev/null, and stderr/stdout
#stdout=open('./logfile.out.log', 'a')
#stderr=open('./logfile.err.log', 'a')

#stdout = open('/dev/null', 'w')
#stderr = open('/dev/null', 'w')

stdout = sys.stdout
stderr = sys.stdout

subprocess.Popen(['nohup', './bg.sh'], stdout=stdout, stderr=stderr, preexec_fn=os.setpgrp)

print('done')
