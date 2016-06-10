import sys

import ui_mainWindow

import PyQt4
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

import fastgrdriver as driver

__version__ = "1.0.0"


class MainWindow(PyQt4.QtGui.QMainWindow):
    """ Main FastGR window
    """

    def __init__(self, parent=None):
        """ Initialization
        Parameters
        ----------
        parent :: parent application
        """

        # Base class
        QtGui.QMainWindow.__init__(self, parent)

        self.ui = ui_mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.dockWidget_ipython.setup()

        # set widgets
        self._init_widgets()

        # define the event handling methods
        # bragg diffraction tab
        self.connect(self.ui.pushButton_loadBraggFile, QtCore.SIGNAL('clicked()'),
                     self.do_load_bragg_file)
        self.connect(self.ui.checkBox_bank1, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank2, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank3, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank4, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank5, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank6, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.comboBox_xUnit, QtCore.SIGNAL('stateChanged(int)'),
                     self.evt_plot_bragg_bank)

        # for tab G(R)
        self.connect(self.ui.pushButton_loadSQ, QtCore.SIGNAL('clicked()'),
                     self.do_load_sq)
        self.connect(self.ui.radioButton_sq, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_sq)
        self.connect(self.ui.radioButton_sq, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_sq)
        self.connect(self.ui.radioButton_sq, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_sq)
        self.connect(self.ui.pushButton_showQMinMax, QtCore.SIGNAL('clicked()'),
                     self.do_show_sq_bound)
        self.connect(self.ui.pushButton_generateGR, QtCore.SIGNAL('clicked()'),
                     self.do_generate_gr)
        self.connect(self.ui.pushButton_saveGR, QtCore.SIGNAL('clicked()'),
                     self.do_save_GR)

        # define the driver
        self._myController = driver.FastGRDriver()

        return

    def _init_widgets(self):
        """ Initialize widgets
        Returns
        -------

        """
        self.ui.comboBox_xUnit.clear()
        self.ui.comboBox_xUnit.addItems(['TOF', ])

        return

    def do_generate_gr(self):
        """
        Generate G(r) by the present user-setup
        Returns
        -------

        """
        # get data
        # calculate the G(R)
        min_r = float(self.ui.doubleSpinBoxQmin.value())
        max_r = float(self.ui.doubleSpinBoxQmax.value())
        delta_r = float(self.ui.doubleSpinBoxDelR.value())

        min_q = float(self.ui.doubleSpinBoxQmin.value())
        max_q = float(self.ui.doubleSpinBoxQmax.value())

        gr_ws_name = self._myController.calculate_gr(min_r, delta_r, max_r, min_q, max_q)

        # plot G(R)
        vec_r, vec_g, vec_ge = self._myController.get_gr(min_q, max_q)
        self.ui.graphicsView_gr.plot_gr(vec_r, vec_g, vec_ge)

        # add to tree
        gr_param_str = 'Q: (%.3f, %.3f)' % (min_q, max_q)
        self.ui.treeWidget_grWsList.add_gr(gr_param_str, gr_ws_name)

        return

    def do_load_bragg_file(self):
        """
        Load Bragg files including GSAS, NeXus, 3-column ASCii.
        Returns
        -------
        """
        # get file
        ext = 'GSAS (*.gsa, *.gss);;DAT (*.dat);;Nexus (*.nxs)'
        bragg_file_name = str(QtGui.QFileDialog.getOpenFileName(self, 'Choose Bragg File', ext))
        if bragg_file_name is None:
            return

        # load file
        gss_ws_name = self._myController.load_bragg_file(bragg_file_name)

        # split
        self._gssGroupName = self._myController.split_to_single_bank(gss_ws_name)

        # plot
        self.ui.checkBox_bank1.setChecked(True)

        return

    def do_load_sq(self):
        """
        Load S(Q) from file
        Returns
        -------

        """
        # get the file
        ext = 'DAT (*.dat);;All (*.*)'
        sq_file_name = str(QtGui.QFileDialog.getOpenFileName(self, 'Choose S(Q) File', ext))
        if sq_file_name is None:
            return

        # open the file
        self._myController.load_sq(sq_file_name)

        # plot the figure
        vec_q, vec_s, vec_e = self._myController.get_sq()
        self.ui.graphicsView_sq.plot_sq(vec_q, vec_s, vec_e)
        self.ui.radioButton_sq.setChecked(True)

        # calculate and calculate G(R)
        self.do_generate_gr()

        return

    def do_save_GR(self):
        """

        Returns
        -------

        """
        # TODO/NOW - Implement!
        self.ui.dockWidget_ipython.wild_test()

    def do_show_sq_bound(self):
        """
        Show or hide the left and right boundary of the S(Q)
        Returns
        -------

        """
        q_left = self.ui.doubleSpinBoxQmin.value()
        q_right = self.ui.doubleSpinBoxQmax.value()
        self.ui.graphicsView_sq.toggle_boundary(q_left, q_right)

        return

    def evt_plot_bragg_bank(self):
        """

        Returns
        -------

        """
        print '[Plot] Bragg Bank ... '

        assert self._gssGroupName is not None

        # get data via driver one by one

        return

    def evt_plot_sq(self):
        """ Event handling to plot S(Q)
        Returns
        -------

        """
        # get the raw S(Q)
        vec_q, vec_sq, vec_se = self._myController.get_sq()

        # get the unit
        sq_unit = None
        if self.ui.radioButton_sq.isChecked():
            # use the original S(Q)
            sq_unit = 'S(Q)'
            vec_y = vec_sq
        elif self.ui.radioButton_sqm1.isChecked():
            # use S(Q)-1
            sq_unit = 'S(Q)-1'
            vec_y = vec_sq - 1
        elif self.ui.radioButton_qsqm1:
            # use Q(S(Q)-1)
            sq_unit = 'Q(S(Q)-1)'
            vec_y = vec_q * (vec_sq - 1)
        else:
            raise RuntimeError('None of S(Q), S(Q)-1 or Q(S(Q)-1) is chosen.')

        # plot
        self.ui.graphicsView_gr.plot_gr(vec_q, vec_y, vec_se, sq_unit)

        return


def main():
    app = PyQt4.QtGui.QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(PyQt4.QtGui.QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()