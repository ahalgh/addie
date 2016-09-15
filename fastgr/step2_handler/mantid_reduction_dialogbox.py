from PyQt4 import QtGui

from fastgr.ui_launchMantid import Ui_Dialog as UiDialog


class MantidReductionDialogbox(QtGui.QDialog):
    
    def __init__(self, parent = None, father = None):
        self.parent = parent
        self.father = father
        
        QtGui.QDialog.__init__(self, parent = parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)
        
        _title = "Launching Mantid Reduction"
        self.setWindowTitle(_title)
        
        _runs = self.father.parameters['runs']
        nbr_jobs = len(_runs)
        _message = 'You are about to launch {} Mantid Reductions jobs!'.format(nbr_jobs)
        self.ui.label.setText(_message)
        
    def cancel_clicked(self):
        self.close()
        
    def view_jobs_clicked(self):
        self.father.view_jobs()
        
    def launch_jobs_clicked(self):
        self.father.run_reduction()
        self.close()