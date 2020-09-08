def run(main_window=None):
    main_window.postprocessing_ui.move_to_button.clicked.connect(main_window.move_to_folder_clicked)
    main_window.postprocessing_ui.name_search.returnPressed.connect(main_window.name_search_clicked)
    main_window.postprocessing_ui.clear_name_search.clicked.connect(main_window.clear_name_search_clicked)
    main_window.postprocessing_ui.import_button.clicked.connect(main_window.import_table_clicked)
    main_window.postprocessing_ui.export_button.clicked.connect(main_window.export_table_clicked)
    main_window.postprocessing_ui.populate_table.clicked.connect(main_window.populate_table_clicked)
    main_window.postprocessing_ui.table.customContextMenuRequested['QPoint'].connect(main_window.table_right_click)
    main_window.postprocessing_ui.table.cellChanged['int', 'int'].connect(main_window.check_step2_gui)
    main_window.postprocessing_ui.background_yes.clicked.connect(main_window.yes_background_clicked)
    main_window.postprocessing_ui.background_comboBox.currentIndexChanged['int'].connect(
        main_window.background_combobox_changed)
    main_window.postprocessing_ui.q_range_min.editingFinished.connect(main_window.check_q_range)
    main_window.postprocessing_ui.q_range_max.editingFinished.connect(main_window.check_q_range)
    main_window.postprocessing_ui.pushButton.clicked.connect(main_window.reset_q_range)
    main_window.postprocessing_ui.plazcek_fit_range_max.editingFinished.connect(main_window.check_plazcek_widgets)
    main_window.postprocessing_ui.plazcek_fit_range_min.editingFinished.connect(main_window.check_plazcek_widgets)
    main_window.postprocessing_ui.hydrogen_no.clicked.connect(main_window.no_hidrogen_clicked)
    main_window.postprocessing_ui.hydrogen_yes.clicked.connect(main_window.hidrogen_clicked)
    main_window.postprocessing_ui.fourier_filter_from.editingFinished.connect(main_window.check_fourier_filter_widgets)
    main_window.postprocessing_ui.fourier_filter_to.editingFinished.connect(main_window.check_fourier_filter_widgets)
    main_window.postprocessing_ui.run_ndabs_output_file_name.textChanged['QString'].connect(
        main_window.output_file_name_changed)
    main_window.postprocessing_ui.pdf_qmax_line_edit.editingFinished.connect(main_window.pdf_qmax_line_edit_changed)
    main_window.postprocessing_ui.sum_scans_output_file_name.editingFinished.connect(
        main_window.sum_scans_output_file_name_changed)
    main_window.postprocessing_ui.pushButton_3.clicked.connect(main_window.help_button_clicked_ndabs)
    main_window.postprocessing_ui.pushButton_4.clicked.connect(main_window.help_button_clicked_scans)
    main_window.postprocessing_ui.run_sum_scans_button.clicked.connect(main_window.run_sum_scans_clicked)
    main_window.postprocessing_ui.run_ndabs_button.clicked.connect(main_window.run_ndabs_clicked)
    main_window.postprocessing_ui.adv_pushButton_isotope.clicked.connect(main_window.isrp_button_clicked)