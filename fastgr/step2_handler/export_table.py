from PyQt4.QtCore import Qt
from fastgr.utilities.file_handler import FileHandler


class ExportTable(object):
    
    column_label = []
    data = []
    output_text = []
    
    def __init__(self, parent = None, filename = ''):
        self.parent = parent
        self.filename = filename
        
    def run(self):
        self.collect_data()
        self.format_data()
        self.export_data()
    
    def collect_data(self):
        nbr_row = self.parent.ui.table.rowCount()

        _full_column_label = []
        nbr_column = self.parent.ui.table.columnCount()
        for j in range(nbr_column):
            _column_label = str(self.parent.ui.table.horizontalHeaderItem(j).text())
            _full_column_label.append(_column_label)
        self.column_label = _full_column_label

        _data = []
        for i in range(nbr_row):
            
            _row = []
            
            # select flag
            _select_flag = self.retrieve_flag_state(row = i, column = 0)
            _row.append(_select_flag)
            
            # name 
            _name_item = str(self.parent.ui.table.item(i, 1).text())
            _row.append(_name_item)
            
            # runs
            _run_item = str(self.parent.ui.table.item(i, 2).text())
            _row.append(_run_item)
            
            # sample formula
            _sample_formula = str(self.parent.ui.table.item(i, 3).text())
            _row.append(_sample_formula)
            
            # mass density
            _mass_density = str(self.parent.ui.table.item(i, 4).text())
            _row.append(_mass_density)
            
            # radius
            _radius = str(self.parent.ui.table.item(i, 5).text())
            _row.append(_radius)
            
            # packing fraction
            _packing_fraction = str(self.parent.ui.table.item(i, 6).text())
            _row.append(_packing_fraction)
            
            # sample shape
            _sample_shape = self.retrieve_sample_shape(row = i, column = 7)
            _row.append(_sample_shape)
            
            # do abs corr?
            _do_corr = self.retrieve_abs_corr_state(row = i, column = 8)
            _row.append(_do_corr)
            
            _data.append(_row)
        self.data = _data

    def format_data(self):
        _column_label = self.column_label
        _data = self.data
        
        output_text = []
        _title = "|".join(_column_label)
        output_text.append("#" + _title)
        
        for _row in _data:
            _formatted_row = "|".join(_row)
            output_text.append(_formatted_row)

        self.output_text = output_text

    def export_data(self):
        _output_text = self.output_text
        _filename = self.filename
        _o_file = FileHandler(filename = _filename)
        _o_file.create_ascii(contain = _output_text)

    def retrieve_abs_corr_state(self, row=0, column=8):
        _widget = self.parent.ui.table.cellWidget(row, 8).children()[1]
        if (_widget.checkState() == Qt.Checked):
            return 'True'
        else:
            return 'False'

    def retrieve_sample_shape(self, row=0, column=7):
        _widget = self.parent.ui.table.cellWidget(row, column)
        _selected_index = _widget.currentIndex()
        _sample_shape = str(_widget.itemText(_selected_index))
        return _sample_shape
            
    def retrieve_flag_state(self, row=0, column=0):
        _widget = self.parent.ui.table.cellWidget(row, column)
        if _widget.checkState() == Qt.Checked:
            return "True"
        else:
            return "False"