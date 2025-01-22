path='//'
command="xdg-open '%s'"%path
subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

