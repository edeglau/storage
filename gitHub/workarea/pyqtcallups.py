#Standalone

import sys, os, PyQt4
from PyQt4 import QtCore, QtGui
import module
reload(module)

def main():
	app = QtGui.QApplication(sys.argv)
	app.setStyle('plastique')
	window=module.class()
	window.show()
	sys.exit(app.exec_())
  
if __name__=="__main__":
	main()

#call

'python modul/path.py'

#application

import sys, os
import module
reload(module)
window=module.class()
window.show()


#call
exec(open('modul/path.py')

