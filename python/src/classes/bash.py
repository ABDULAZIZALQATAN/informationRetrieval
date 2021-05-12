import subprocess

def runBashFile(shFile):
    cmd = 'sh %s' % shFile
    bashCmd = 'bash -c \"%s\" ' % cmd
    return subprocess.getoutput(bashCmd)

def runBashCmd(cmd):
    bashCmd = 'bash -c \"%s\" ' % cmd
    subprocess.getoutput(bashCmd)