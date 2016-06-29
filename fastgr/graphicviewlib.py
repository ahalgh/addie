import numpy as np

from PyQt4 import QtCore

import mplgraphicsview as base


class BraggView(base.MplGraphicsView):
    """ Graphics view for Bragg diffraction
    """
    def __init__(self, parent):
        """
        Initialization
        Parameters
        ----------
        parent
        """
        base.MplGraphicsView.__init__(self, parent)

        # control class
        self._bankPlotDict = dict()
        for bank_id in range(1, 7):
            self._bankPlotDict[bank_id] = False

        self._singleGSSMode = True
        self._bankColorDict = {1: 'black',
                               2: 'red',
                               3: 'blue',
                               4: 'green',
                               5: 'brown',
                               6: 'yellow'}

        self._gssColorList = ["black", "red", "blue", "green",
                              "cyan", "magenta", "yellow"]
        self._currColorIndex = 0

        return

    def check_banks(self, bank_to_plot_list):
        """ Check the to-plot bank list against the current being-plot bank list,
        to find out the banks which are to plot and to be removed from plot.
        Args:
            bank_to_plot_list:
        Returns:
            2-tuple.  (1) list of banks' IDs to be plot and (2) list of
            banks' IDs to be removed from current canvas.
        """
        # check
        assert isinstance(bank_to_plot_list, list)

        new_plot_banks = bank_to_plot_list[:]
        to_remove_banks = list()

        for bank_id in self._bankPlotDict.keys():
            if self._bankPlotDict[bank_id] is False:
                # previously-not-being plot. either in new_plot_banks already or no-op
                continue
            elif bank_id in bank_to_plot_list:
                # previously-being plot, then to be removed from new-plot-list
                new_plot_banks.remove(bank_id)
            else:
                # previously-being plot, then to be removed from canvas
                to_remove_banks.append(bank_id)
        # END-FOR (bank_id)

        return new_plot_banks, to_remove_banks

    def get_multi_gss_color(self):
        """
        Get the present color in multiple-GSS mode
        Returns:

        """
        color = self._gssColorList[self._currColorIndex]
        self._currColorIndex += 1
        if self._currColorIndex == len(self._gssColorList):
            self._currColorIndex = 0

        return color

    def plot_banks(self, plot_bank_dict, unit):
        """
        Plot a few banks to canvas.  If the bank has been plot on canvas already,
        then remove the previous data
        Args:
            plot_bank_dict: dictionary: key = ws group name, value = dictionary (key = bank ID, value = (x, y, e)
            unit: string for X-range unit.  can be TOF, dSpacing or Q (momentum transfer)

        Returns:

        """
        # check
        assert isinstance(plot_bank_dict, dict)

        # plot
        for ws_group in plot_bank_dict.keys():
            for bank_id in plot_bank_dict[ws_group]:
                # add the new plot
                if self._singleGSSMode:
                    bank_color = self._bankColorDict[bank_id]
                else:
                    bank_color = self.get_multi_gss_color()
                vec_x, vec_y, vec_e = plot_bank_dict[ws_group][bank_id]
                plot_id = self.add_plot_1d(vec_x, vec_y, marker='.', color=bank_color,
                                           x_label=unit, y_label='I(%s)' % unit,
                                           label='%s Bank %d' % (ws_group, bank_id))
            #self._bankPlotDict[bank_id] = plot_id
        # END-FOR (bank id)

        return

    def plot_general_ws(self, bragg_ws_name, vec_x, vec_y, vec_e):
        plot_id = self.add_plot_1d(vec_x, vec_y, marker='.', color='black',
                                   label=bragg_ws_name)

        return

    def remove_banks(self, bank_id_list):
        """
        Remove a few bank ID fro Bragg plot
        Args:
            bank_id_list:

        Returns:

        """
        # check
        assert isinstance(bank_id_list, list)

        # remove
        for bank_id in bank_id_list:
            bank_line_id = self._bankPlotDict[bank_id]
            # remove from canvas
            try:
                self.remove_line(bank_line_id)
            except ValueError as val_error:
                error_message = 'Unable to remove bank %d plot (ID = %d) due to %s.' % (bank_id,
                                                                                        bank_line_id,
                                                                                        str(val_error))
                raise ValueError(error_message)
            # remove from data structure
            self._bankPlotDict[bank_id] = False
        # END-FOR

        # debug output
        db_buf = ''
        for bank_id in self._bankPlotDict:
            db_buf += '%d: %s \t' % (bank_id, str(self._bankPlotDict[bank_id]))
        print 'After removing %s, Buffer: %s.' % (str(bank_id_list), db_buf)

        return

    def reset(self):
        """
        Reset the canvas for new Bragg data
        Returns:
        None
        """
        # clear the control-dictionary and uncheck all the banks
        # set mutex on
        for bank_id in self._bankPlotDict.keys():
            self._bankPlotDict[bank_id] = False

        # clear all lines
        self.clear_all_lines()

        return

    def set_to_single_gss(self, mode_on):
        """
        Set to single-GSAS/multiple-bank model
        Args:
            mode_on:

        Returns:

        """
        assert isinstance(mode_on, bool)

        self._singleGSSMode = mode_on

        return


class GofRView(base.MplGraphicsView):
    """
    Graphics view for G(R)
    """
    def __init__(self, parent):
        """
        Initialization
        """
        base.MplGraphicsView.__init__(self, parent)

        # class variable containers
        self._grDict = dict()

        self._colorList = ['black', 'red', 'blue', 'green', 'brown', 'orange']
        self._colorIndex = 0

        return

    def plot_gr(self, key_plot, vec_r, vec_g, vec_e=None, plot_error=False):
        """
        Plot G(r)
        Parameters
        -------
        vec_r: numpy array for R
        vec_g: numpy array for G(r)
        vec_e: numpy array for G(r) error
        Returns
        -------

        """
        # TODO/NOW - Doc and check
        if plot_error:
            self.add_plot_1d(vec_r, vec_g, vec_e)
            raise NotImplementedError('ASAP')
        else:
            line_id = self.add_plot_1d(vec_r, vec_g, marker='.',
                                       color=self._colorList[self._colorIndex % len(self._colorList)])
            self._colorIndex += 1
            self._grDict[key_plot] = line_id

        return

    def remove_gr(self, key_plot):
        """

        Parameters
        ----------
        key_plot

        Returns
        -------

        """
        # TODO/NOW - Doc and check
        line_id = self._grDict[key_plot]

        self.remove_line(line_id)

        del self._grDict[line_id]

        return


class SofQView(base.MplGraphicsView):
    """
    Graphics view for S(Q)
    """
    # boundary moving signal (1) int for left/right boundary indicator (2)
    boundaryMoveSignal = QtCore.pyqtSignal(int, float)

    # resolution of boundary indicator to be selected
    IndicatorResolution = 0.01

    def __init__(self, parent):
        """
        Initialization
        Parameters
        ----------
        parent
        """
        self._myParent = parent

        base.MplGraphicsView.__init__(self, parent)

        # declare event handling to indicators
        self._myCanvas.mpl_connect('button_press_event', self.on_mouse_press_event)
        self._myCanvas.mpl_connect('button_release_event', self.on_mouse_release_event)
        self._myCanvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

        self._mainApp = None

        # link signal
        # self.boundaryMoveSignal.connect(self._myParent.update_sq_boundary)

        # declare class variables for moving boundary
        self._showBoundary = False
        self._leftID = None
        self._rightID = None

        self._selectedBoundary = 0
        self._prevCursorPos = None

        return

    def set_main(self, main_app):
        """

        Returns
        -------

        """
        self._mainApp = main_app

        # link signal
        self.boundaryMoveSignal.connect(self._mainApp.update_sq_boundary)

        return

    def is_boundary_shown(self):
        """

        Returns
        -------

        """
        return self._showBoundary

    def move_left_indicator(self, displacement, relative):
        """

        Args:
            displacement:
            relative:

        Returns:

        """
        # check
        assert isinstance(displacement, float)
        assert isinstance(relative, bool)

        if relative:
            self.move_indicator(self._leftID, displacement)
        else:
            self.set_indicator_position(self._leftID, displacement, 0)

        return

    def move_right_indicator(self, displacement, relative):
        """

        Args:
            displacement:
            relative:

        Returns:

        """
        # check
        assert isinstance(displacement, float)
        assert isinstance(relative, bool)

        if relative:
            self.move_indicator(self._rightID, displacement)
        else:
            self.set_indicator_position(self._rightID, displacement, 0)

        return

    def on_mouse_motion(self, event):
        """

        Returns
        -------

        """
        # ignore if boundary is not shown
        if not self._showBoundary:
            return

        # ignore if no boundary is selected
        if self._selectedBoundary == 0:
            return
        elif self._selectedBoundary > 2:
            raise RuntimeError('Impossible to have selected boundary mode %d' % self._selectedBoundary)

        cursor_pos = event.xdata
        print event.xdata

        # ignore if the cursor is out of canvas
        if cursor_pos is None:
            return

        cursor_displace = cursor_pos - self._prevCursorPos

        left_bound_pos = self.get_indicator_position(self._leftID)[0]
        right_bound_pos = self.get_indicator_position(self._rightID)[0]

        x_range = self.getXLimit()
        resolution = (x_range[1] - x_range[0]) * self.IndicatorResolution

        if self._selectedBoundary == 1:
            # left boundary
            new_left_bound = left_bound_pos + cursor_displace

            # return if the left boundary is too close to right
            if new_left_bound > right_bound_pos - resolution * 5:
                return

            # move left boundary
            self.move_indicator(self._leftID, cursor_displace, 0)

            # signal main
            self.boundaryMoveSignal.emit(1, new_left_bound)

        else:
            # right boundary
            new_right_bound = right_bound_pos + cursor_displace

            # return if the right boundary is too close or left to the left boundary
            if new_right_bound < left_bound_pos + resolution * 5:
                return

            # move right boundary
            self.move_indicator(self._rightID, cursor_displace, 0)

            # emit signal to the main app
            self.boundaryMoveSignal.emit(2, new_right_bound)

        # update cursor position
        self._prevCursorPos = cursor_pos

        return

    def on_mouse_press_event(self, event):
        """

        Returns
        -------

        """
        # ignore if boundary is not shown
        if not self._showBoundary:
            return

        # get mouse cursor x position
        mouse_x_pos = event.xdata
        if mouse_x_pos is None:
            return
        else:
            self._prevCursorPos = mouse_x_pos

        # get absolute resolution
        x_range = self.getXLimit()
        resolution = (x_range[1] - x_range[0]) * self.IndicatorResolution

        # see whether it is close enough to any boundary
        left_bound_pos = self.get_indicator_position(self._leftID)[0]
        right_bound_pos = self.get_indicator_position(self._rightID)[0]
        if abs(mouse_x_pos - left_bound_pos) < resolution:
            self._selectedBoundary = 1
            print '[DB...] Left boundary selected'
        elif abs(mouse_x_pos - right_bound_pos) < resolution:
            self._selectedBoundary = 2
            print '[DB...] Right boundary selected'
        else:
            self._selectedBoundary = 0
        # END-IF-ELSE

        return

    def on_mouse_release_event(self, event):
        """

        Returns
        -------

        """
        # ignore if boundary is not shown
        if not self._showBoundary:
            return

        # get mouse cursor position
        self._prevCursorPos = event.xdata

        self._prevCursorPos = None
        self._selectedBoundary = 0

        return

    def plot_sq(self, vec_r, vec_s, vec_e, sq_y_label):
        """
        Plot S(Q)
        Parameters
        ----------
        vec_r
        vec_s
        vec_e
        sq_y_label :: label for Y-axis

        Returns
        -------

        """
        # check
        assert isinstance(vec_r, np.ndarray) and isinstance(vec_s, np.ndarray)
        assert isinstance(sq_y_label, str)

        self.clear_all_lines()
        self.add_plot_1d(vec_r, vec_s, color='blue', x_label='Q', y_label=sq_y_label,
                         marker='.')

        return

    def toggle_boundary(self, q_left, q_right):
        """ Turn on or off the left and right boundary to select Q-range
        Parameters
        ----------
        q_left ::
        q_right ::
        Returns
        -------

        """
        # check
        assert isinstance(q_left, float) and isinstance(q_right, float)
        assert q_left < q_right

        if self._showBoundary:
            # Q-boundary indicator is on. turn off
            self.remove_indicator(self._leftID)
            self.remove_indicator(self._rightID)
            self._leftID = None
            self._rightID = None
            self._showBoundary = False
        else:
            self._leftID = self.add_vertical_indicator(q_left, 'red')
            self._rightID = self.add_vertical_indicator(q_right, 'red')
            self._showBoundary = True

            # reset the x-range
            x_range = self.getXLimit()
            if x_range[0] > q_left - 1:
                self.setXYLimit(xmin=q_left-1)

        # END-IF-ELSE (show boundary)

        return
