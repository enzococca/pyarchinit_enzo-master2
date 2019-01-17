#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
        pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
                             stored in Postgres
                             -------------------
    begin                : 2007-12-01
    copyright            : (C) 2008 by Luca Mandolesi
    email                : mandoluca at gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from __future__ import absolute_import
import os
from builtins import range
from builtins import str
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.PyQt.uic import loadUiType
from qgis.core import QgsSettings
from ..modules.db.pyarchinit_conn_strings import Connection
from ..modules.db.pyarchinit_db_manager import Pyarchinit_db_management
from ..modules.db.pyarchinit_utility import Utility
from ..modules.gis.pyarchinit_pyqgis import Pyarchinit_pyqgis
from ..modules.utility.pdf_models.pyarchinit_exp_Findssheet_pdf import generate_pdf
from ..modules.utility.pyarchinit_error_check import Error_check
from ..modules.utility.pyarchinit_exp_Individui_pdf import generate_pdf
from ..gui.sortpanelmain import SortPanelMain

MAIN_DIALOG_CLASS, _ = loadUiType(os.path.join(os.path.dirname(__file__), os.pardir, 'gui', 'ui', 'Schedaind.ui'))


class pyarchinit_Schedaind(QDialog, MAIN_DIALOG_CLASS):
    L=QgsSettings().value("locale/userLocale")[0:2]
    if L=='it':
        MSG_BOX_TITLE = "PyArchInit - Scheda Individui"
    elif L=='en':
        MSG_BOX_TITLE = "PyArchInit - Individual Form"
    elif L=='de':
        MSG_BOX_TITLE = "PyArchInit - Formular Individuel"
    DATA_LIST = []
    DATA_LIST_REC_CORR = []
    DATA_LIST_REC_TEMP = []
    REC_CORR = 0
    REC_TOT = 0
    if L=='it':
        STATUS_ITEMS = {"b": "Usa", "f": "Trova", "n": "Nuovo Record"}
    else :
        STATUS_ITEMS = {"b": "Current", "f": "Find", "n": "New Record"}
    BROWSE_STATUS = "b"
    SORT_MODE = 'asc'
    if L=='it':
        SORTED_ITEMS = {"n": "Non ordinati", "o": "Ordinati"}
    else:
        SORTED_ITEMS = {"n": "Not sorted", "o": "Sorted"}
    SORT_STATUS = "n"
    UTILITY = Utility()
    DB_MANAGER = ""
    TABLE_NAME = 'individui_table'
    MAPPER_TABLE_CLASS = "SCHEDAIND"
    NOME_SCHEDA = "Scheda Individuo"
    ID_TABLE = "id_scheda_ind"
    if L=='it':
        CONVERSION_DICT = {
            ID_TABLE: ID_TABLE,
            "Sito": "sito",
            "US": "us",
            "Area": "area",
            "Nr. Individuo": "nr_individuo",
            "Data Schedatura": "data_schedatura",
            "Schedatore": "schedatore",
            "Stima del sesso": "sesso",
            "Stima dell'eta' di morte min": "eta_min",
            "Stima dell'eta' di morte max": "eta_max",
            "Classi di eta'": "classi_eta",
            "Osservazioni": "osservazioni"
        }
        SORT_ITEMS = [
            ID_TABLE,
            "Sito",
            "Area",
            "US",
            "Nr. Individuo",
            "Data schedatura",
            "Schedatore",
            "Stima del sesso",
            "Stima dell'eta' di morte min",
            "Stima dell'eta' di morte max",
            "Classi di eta'",
            "Osservazioni"
        ]
    elif L=='de':
        CONVERSION_DICT = {
            ID_TABLE: ID_TABLE,
            "Ausgrabungsstätte": "sito",
            "SE": "us",
            "Areal": "area",
            "Nr. Individuel": "nr_individuo",
            "Katalogisierungsdaten": "data_schedatura",
            "Physikalische Daten": "schedatore",
            "Geschätztes Geschlecht": "sesso",
            "Schätzung des Todesalters  min": "eta_min",
            "Schätzung des Todesalters  max": "eta_max",
            "Altersklassen": "classi_eta",
            "Beobachtungen": "osservazioni"
        }
        SORT_ITEMS = [
            ID_TABLE,
            "Ausgrabungsstätte",
            "SE",
            "Areal",
            "Nr. Individuel",
            "Katalogisierungsdaten",
            "Physikalische Daten",
            "Geschätztes Geschlecht",
            "Schätzung des Todesalters  min",
            "Schätzung des Todesalters  max",
            "Altersklassen",
            "Beobachtungen"
        ]
    else:
        CONVERSION_DICT = {
            ID_TABLE: ID_TABLE,
            "Site": "sito",
            "SU": "us",
            "Area": "area",
            "Individual Nr.": "nr_individuo",
            "Date Form": "data_schedatura",
            "Filler": "schedatore",
            "Extimation sex": "sesso",
            "Extimation age of death min": "eta_min",
            "Extimation age of death max": "eta_max",
            "Age class": "classi_eta",
            "Note": "osservazioni"
        }
        SORT_ITEMS = [
            ID_TABLE,
            "Site",
            "SU",
            "Area",
            "Individual Nr.",
            "Date Form",
            "Filler",
            "Extimation sex",
            "Extimation age of death min",
            "Extimation age of death max",
            "Age class",
            "Note"
        ]   
    TABLE_FIELDS = [
        'sito',
        'area',
        'us',
        'nr_individuo',
        'data_schedatura',
        'schedatore',
        'sesso',
        'eta_min',
        'eta_max',
        'classi_eta',
        'osservazioni'
    ]

    DB_SERVER = "not defined"  ####nuovo sistema sort

    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.pyQGIS = Pyarchinit_pyqgis(iface)
        self.setupUi(self)
        self.currentLayerId = None
        try:
            self.on_pushButton_connect_pressed()
        except Exception as e:
            QMessageBox.warning(self, "Connection System", str(e), QMessageBox.Ok)

    def enable_button(self, n):
        self.pushButton_connect.setEnabled(n)

        self.pushButton_new_rec.setEnabled(n)

        self.pushButton_view_all.setEnabled(n)

        self.pushButton_first_rec.setEnabled(n)

        self.pushButton_last_rec.setEnabled(n)

        self.pushButton_prev_rec.setEnabled(n)

        self.pushButton_next_rec.setEnabled(n)

        self.pushButton_delete.setEnabled(n)

        self.pushButton_new_search.setEnabled(n)

        self.pushButton_search_go.setEnabled(n)

        self.pushButton_sort.setEnabled(n)

    def enable_button_search(self, n):
        self.pushButton_connect.setEnabled(n)

        self.pushButton_new_rec.setEnabled(n)

        self.pushButton_view_all.setEnabled(n)

        self.pushButton_first_rec.setEnabled(n)

        self.pushButton_last_rec.setEnabled(n)

        self.pushButton_prev_rec.setEnabled(n)

        self.pushButton_next_rec.setEnabled(n)

        self.pushButton_delete.setEnabled(n)

        self.pushButton_save.setEnabled(n)

        self.pushButton_sort.setEnabled(n)

    def on_pushButton_connect_pressed(self):
        conn = Connection()
        conn_str = conn.conn_str()
        try:
            self.DB_MANAGER = Pyarchinit_db_management(conn_str)
            self.DB_MANAGER.connection()
            self.charge_records()  # charge records from DB
            # check if DB is empty
            if bool(self.DATA_LIST):
                self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
                self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
                self.BROWSE_STATUS = "b"
                self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
                self.label_sort.setText(self.SORTED_ITEMS["n"])
                self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR + 1)
                self.charge_list()
                self.fill_fields()
            else:
                if self.L=='it':
                    QMessageBox.warning(self,"BENVENUTO", "Benvenuto in pyArchInit" + "Scheda individui" + ". Il database e' vuoto. Premi 'Ok' e buon lavoro!",
                                        QMessageBox.Ok)
                
                elif self.L=='de':
                    
                    QMessageBox.warning(self,"WILLKOMMEN","WILLKOMMEN in pyArchInit" + "individuel formular"+ ". Die Datenbank ist leer. Tippe 'Ok' und aufgehts!",
                                        QMessageBox.Ok) 
                else:
                    QMessageBox.warning(self,"WELCOME", "Welcome in pyArchInit" + "individual form" + ". The DB is empty. Push 'Ok' and Good Work!",
                                        QMessageBox.Ok)
                self.charge_list()
                self.BROWSE_STATUS = 'x'
                self.on_pushButton_new_rec_pressed()
        except Exception as e:
            e = str(e)
            if e.find("no such table"):
                if self.L=='it':
                    msg = "La connessione e' fallita {}. " \
                          "E' NECESSARIO RIAVVIARE QGIS oppure rilevato bug! Segnalarlo allo sviluppatore".format(str(e))
                    self.iface.messageBar().pushMessage(self.tr(msg), Qgis.Warning, 0)
                
                    self.iface.messageBar().pushMessage(self.tr(msg), Qgis.Warning, 0)
                elif self.L=='de':
                    msg = "Verbindungsfehler {}. " \
                          " QGIS neustarten oder es wurde ein bug gefunden! Fehler einsenden".format(str(e))
                    self.iface.messageBar().pushMessage(self.tr(msg), Qgis.Warning, 0)
                else:
                    msg = "The connection failed {}. " \
                          "You MUST RESTART QGIS or bug detected! Report it to the developer".format(str(e))        
            else:
                if self.L=='it':
                    msg = "Attenzione rilevato bug! Segnalarlo allo sviluppatore. Errore: ".format(str(e))
                    self.iface.messageBar().pushMessage(self.tr(msg), Qgis.Warning, 0)
                
                elif self.L=='de':
                    msg = "ACHTUNG. Es wurde ein bug gefunden! Fehler einsenden: ".format(str(e))
                    self.iface.messageBar().pushMessage(self.tr(msg), Qgis.Warning, 0)  
                else:
                    msg = "Warning bug detected! Report it to the developer. Error: ".format(str(e))
                    self.iface.messageBar().pushMessage(self.tr(msg), Qgis.Warning, 0)    

    def customize_GUI(self):
        pass

    def loadMapPreview(self, mode=0):
        pass

    def charge_list(self):

        #lista sito

        sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))
        try:
            sito_vl.remove('')
        except:
            pass

        self.comboBox_sito.clear()

        sito_vl.sort()
        self.comboBox_sito.addItems(sito_vl)

    def charge_periodo_list(self):
        pass

    def charge_fase_iniz_list(self):
        pass

    def charge_fase_fin_list(self):
        pass

        # buttons functions

    def generate_list_pdf(self):
        data_list = []
        for i in range(len(self.DATA_LIST)):
            data_list.append([
                str(self.DATA_LIST[i].sito),  # 1 - Sito
                int(self.DATA_LIST[i].area),  # 2 - Area
                int(self.DATA_LIST[i].us),  # 3 - us
                int(self.DATA_LIST[i].nr_individuo),  # 4 -  nr individuo
                str(self.DATA_LIST[i].data_schedatura),  # 5 - data schedatura
                str(self.DATA_LIST[i].schedatore),  # 6 - schedatore
                str(self.DATA_LIST[i].sesso),  # 7 - sesso
                str(self.DATA_LIST[i].eta_min),  # 8 - eta' minima
                str(self.DATA_LIST[i].eta_max),  # 9- eta massima
                str(self.DATA_LIST[i].classi_eta),  # 10 - classi di eta'
                str(self.DATA_LIST[i].osservazioni)  # 11 - osservazioni
            ])
        return data_list

    def on_pushButton_pdf_exp_pressed(self):
        if self.L=='it':
            Individui_pdf_sheet = generate_pdf()
            data_list = self.generate_list_pdf()
            Individui_pdf_sheet.build_Individui_sheets(data_list)
        elif self.L=='de':
            Individui_pdf_sheet = generate_pdf()
            data_list = self.generate_list_pdf()
            Individui_pdf_sheet.build_Individui_sheets_de(data_list)
        else:
            Individui_pdf_sheet = generate_pdf()
            data_list = self.generate_list_pdf()
            Individui_pdf_sheet.build_Individui_sheets_en(data_list)    
    def on_pushButton_exp_index_ind_pressed(self):
        if self.L=='it':
            Individui_pdf_index = generate_pdf()
            data_list = self.generate_list_pdf()
            Individui_pdf_index.build_index_individui(data_list, data_list[0][0])
        elif self.L=='de':
            Individui_pdf_index = generate_pdf()
            data_list = self.generate_list_pdf()
            Individui_pdf_index.build_index_individui_de(data_list, data_list[0][0])
        else:
            Individui_pdf_index = generate_pdf()
            data_list = self.generate_list_pdf()
            Individui_pdf_index.build_index_individui_en(data_list, data_list[0][0])    
    """
    def on_toolButtonPan_toggled(self):
        self.toolPan = QgsMapToolPan(self.mapPreview)
        self.mapPreview.setMapTool(self.toolPan)
    """
    """
    def on_pushButton_showSelectedFeatures_pressed(self):

        field_position = self.pyQGIS.findFieldFrDict(self.ID_TABLE)

        field_list = self.pyQGIS.selectedFeatures()

        id_list_sf = self.pyQGIS.findItemInAttributeMap(field_position, field_list)
        id_list = []
        for idl in id_list_sf:
            sid = idl.toInt()
            id_list.append(sid[0])

        items,order_type = [self.ID_TABLE], "asc"
        self.empty_fields()

        self.DATA_LIST = []

        temp_data_list = self.DB_MANAGER.query_sort(id_list, items, order_type, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

        for us in temp_data_list:
            self.DATA_LIST.append(us)

        self.fill_fields()
        self.label_status.setText(self.STATUS["usa"])
        if type(self.REC_CORR) == "<type 'str'>":
            corr = 0
        else:
            corr = self.REC_CORR

        self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
        self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
        self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
    """

    # buttons functions
    def on_pushButton_sort_pressed(self):
        if self.check_record_state() == 1:
            pass
        else:
            dlg = SortPanelMain(self)
            dlg.insertItems(self.SORT_ITEMS)
            dlg.exec_()

            items, order_type = dlg.ITEMS, dlg.TYPE_ORDER

            self.SORT_ITEMS_CONVERTED = []
            for i in items:
                self.SORT_ITEMS_CONVERTED.append(self.CONVERSION_DICT[str(i)])

            self.SORT_MODE = order_type
            self.empty_fields()

            id_list = []
            for i in self.DATA_LIST:
                id_list.append(eval("i." + self.ID_TABLE))
            self.DATA_LIST = []

            temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE,
                                                        self.MAPPER_TABLE_CLASS, self.ID_TABLE)

            for i in temp_data_list:
                self.DATA_LIST.append(i)
            self.BROWSE_STATUS = "b"
            self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
            if type(self.REC_CORR) == "<type 'str'>":
                corr = 0
            else:
                corr = self.REC_CORR
            self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
            self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
            self.SORT_STATUS = "o"
            self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
            self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR + 1)
            self.fill_fields()

    def on_toolButtonGis_toggled(self):
        if self.L=='it':
            if self.toolButtonGis.isChecked():
                QMessageBox.warning(self, "Messaggio",
                                    "Modalita' GIS attiva. Da ora le tue ricerche verranno visualizzate sul GIS",
                                    QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Messaggio",
                                    "Modalita' GIS disattivata. Da ora le tue ricerche non verranno piu' visualizzate sul GIS",
                                    QMessageBox.Ok)
        elif self.L=='de':
            if self.toolButtonGis.isChecked():
                QMessageBox.warning(self, "Message",
                                    "Modalität' GIS aktiv. Von jetzt wird Deine Untersuchung mit Gis visualisiert",
                                    QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Message",
                                    "Modalität' GIS deaktiviert. Von jetzt an wird deine Untersuchung nicht mehr mit Gis visualisiert",
                                    QMessageBox.Ok)
        else:
            if self.toolButtonGis.isChecked():
                QMessageBox.warning(self, "Message",
                                    "GIS mode active. From now on your searches will be displayed on the GIS",
                                    QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Message",
                                    "GIS mode disabled. From now on, your searches will no longer be displayed on the GIS.",
                                    QMessageBox.Ok)
                                    
    def on_toolButtonPreview_toggled(self):
        if self.L=='it':
            if self.toolButtonPreview.isChecked():
                QMessageBox.warning(self, "Messaggio",
                                    "Modalita' Preview US attivata. Le piante delle US saranno visualizzate nella sezione Piante",
                                    QMessageBox.Ok)
                self.loadMapPreview()
            else:
                self.loadMapPreview(1)
        elif self.L=='de':
            if self.toolButtonPreview.isChecked():
                QMessageBox.warning(self, "Message",
                                    "Modalität' Preview der aktivierten SE. Die Plana der SE werden in der Auswahl der Plana visualisiert",
                                    QMessageBox.Ok)
                self.loadMapPreview()
            else:
                self.loadMapPreview(1)
                
        else:
            if self.toolButtonPreview.isChecked():
                QMessageBox.warning(self, "Message",
                                    "Preview SU mode enabled. US plants will be displayed in the Plants section",
                                    QMessageBox.Ok)
                self.loadMapPreview()
            else:
                self.loadMapPreview(1)

    """
    def on_pushButton_addRaster_pressed(self):
        if self.toolButtonGis.isChecked() == True:
            self.pyQGIS.addRasterLayer()
    """

    def on_pushButton_new_rec_pressed(self):
        if bool(self.DATA_LIST):
            if self.data_error_check() == 1:
                pass
            '''else:
                if self.BROWSE_STATUS == "b":
                    if bool(self.DATA_LIST):
                        if self.records_equal_check() == 1:
                            self.update_if(QMessageBox.warning(self, 'Errore',
                                                               "Il record e' stato modificato. Vuoi salvare le modifiche?",
                                                               QMessageBox.Ok | QMessageBox.Cancel))'''
                            # set the GUI for a new record
        if self.BROWSE_STATUS != "n":
            self.BROWSE_STATUS = "n"
            self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
            self.empty_fields()
            self.label_sort.setText(self.SORTED_ITEMS["n"])

            self.setComboBoxEditable(["self.comboBox_sito"], 0)
            self.setComboBoxEnable(["self.comboBox_sito"], "True")
            self.setComboBoxEnable(["self.lineEdit_area"], "True")
            self.setComboBoxEnable(["self.lineEdit_us"], "True")
            self.setComboBoxEnable(["self.lineEdit_individuo"], "True")

            self.set_rec_counter('', '')
            self.enable_button(0)

    def on_pushButton_save_pressed(self):
        # save record
        if self.BROWSE_STATUS == "b":
            if self.data_error_check() == 0:
                if self.records_equal_check() == 1:
                    if self.L=='it':
                        self.update_if(QMessageBox.warning(self, 'Errore',
                                                           "Il record e' stato modificato. Vuoi salvare le modifiche?",QMessageBox.Ok | QMessageBox.Cancel))
                    elif self.L=='de':
                        self.update_if(QMessageBox.warning(self, 'Error',
                                                           "Der Record wurde geändert. Möchtest du die Änderungen speichern?",
                                                           QMessageBox.Ok | QMessageBox.Cancel))
                                                           
                    else:
                        self.update_if(QMessageBox.warning(self, 'Error',
                                                           "The record has been changed. Do you want to save the changes?",
                                                           QMessageBox.Ok | QMessageBox.Cancel))
                    self.SORT_STATUS = "n"
                    self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
                    self.enable_button(1)
                    self.fill_fields(self.REC_CORR)
                else:
                    if self.L=='it':
                        QMessageBox.warning(self, "ATTENZIONE", "Non è stata realizzata alcuna modifica.", QMessageBox.Ok)
                    elif self.L=='de':
                        QMessageBox.warning(self, "ACHTUNG", "Keine Änderung vorgenommen", QMessageBox.Ok)
                    else:
                        QMessageBox.warning(self, "Warning", "No changes have been made", QMessageBox.Ok)
        else:
            if self.data_error_check() == 0:
                test_insert = self.insert_new_rec()
                if test_insert == 1:
                    self.empty_fields()
                    self.label_sort.setText(self.SORTED_ITEMS["n"])
                    self.charge_list()
                    self.charge_records()
                    self.BROWSE_STATUS = "b"
                    self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
                    self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST) - 1
                    self.set_rec_counter(self.REC_TOT, self.REC_CORR + 1)

                    self.set_rec_counter(self.REC_TOT, self.REC_CORR + 1)
                    self.setComboBoxEditable(["self.comboBox_sito"], 1)
                    self.setComboBoxEnable(["self.comboBox_sito"], "False")
                    self.setComboBoxEnable(["self.lineEdit_area"], "False")
                    self.setComboBoxEnable(["self.lineEdit_us"], "False")
                    self.setComboBoxEnable(["self.lineEdit_individuo"], "False")
                    self.fill_fields(self.REC_CORR)
                    self.enable_button(1)
            else:
                pass

    def data_error_check(self):
        test = 0
        EC = Error_check()
        if self.L=='it':
            if EC.data_is_empty(str(self.comboBox_sito.currentText())) == 0:
                QMessageBox.warning(self, "ATTENZIONE", "Campo Sito. \n Il campo non deve essere vuoto", QMessageBox.Ok)
                test = 1

            if EC.data_is_empty(str(self.lineEdit_area.text())) == 0:
                QMessageBox.warning(self, "ATTENZIONE", "Campo Area. \n Il campo non deve essere vuoto", QMessageBox.Ok)
                test = 1

            if EC.data_is_empty(str(self.lineEdit_us.text())) == 0:
                QMessageBox.warning(self, "ATTENZIONE", "Campo US. \n Il campo non deve essere vuoto", QMessageBox.Ok)
                test = 1

            if EC.data_is_empty(str(self.lineEdit_individuo.text())) == 0:
                QMessageBox.warning(self, "ATTENZIONE", "Campo nr individuo. \n Il campo non deve essere vuoto",
                                    QMessageBox.Ok)
                test = 1

            area = self.lineEdit_area.text()
            us = self.lineEdit_us.text()
            nr_individuo = self.lineEdit_individuo.text()
            eta_min = self.comboBox_eta_min.currentText()
            eta_max = self.comboBox_eta_max.currentText()

            if area != "":
                if EC.data_lenght(area, 3) == 0:
                    QMessageBox.warning(self, "ATTENZIONE",
                                        "Campo Area. \n Il valore deve essere lungo massimo 4 caratteri alfanumerici",
                                        QMessageBox.Ok)
                    test = 1

            if us != "":
                if EC.data_is_int(us) == 0:
                    QMessageBox.warning(self, "ATTENZIONE", "Campo US. \n Il valore deve essere di tipo numerico",
                                        QMessageBox.Ok)
                    test = 1

            if nr_individuo != "":
                if EC.data_is_int(nr_individuo) == 0:
                    QMessageBox.warning(self, "ATTENZIONE", "Campo Nr individuo. \n Il valore deve essere di tipo numerico",
                                        QMessageBox.Ok)
                    test = 1

            if eta_min != "":
                if EC.data_is_int(eta_min) == 0:
                    QMessageBox.warning(self, "ATTENZIONE", "Campo Età minima \n Il valore deve essere di tipo numerico",
                                        QMessageBox.Ok)
                    test = 1

            if eta_max != "":
                if EC.data_is_int(eta_max) == 0:
                    QMessageBox.warning(self, "ATTENZIONE", "Campo Età massima \n Il valore deve essere di tipo numerico",
                                        QMessageBox.Ok)
                    test = 1
        
        
        elif self.L=='de':  
            if EC.data_is_empty(str(self.comboBox_sito.currentText())) == 0:
                QMessageBox.warning(self, "ACHTUNG", " Feld Ausgrabungstätte. \n Das Feld darf nicht leer sein", QMessageBox.Ok)
                test = 1

            if EC.data_is_empty(str(self.lineEdit_area.text())) == 0:
                QMessageBox.warning(self, "ACHTUNG", "Feld Areal. \n Das Feld darf nicht leer sein", QMessageBox.Ok)
                test = 1

            if EC.data_is_empty(str(self.lineEdit_us.text())) == 0:
                QMessageBox.warning(self, "ACHTUNG", "Feld SE. \n Das Feld darf nicht leer sein", QMessageBox.Ok)
                test = 1
                
            if EC.data_is_empty(str(self.lineEdit_individuo.text())) == 0:
                QMessageBox.warning(self, "ACHTUNG", "Feld nr individuel. \n Das Feld darf nicht leer sein",
                                    QMessageBox.Ok)
                test = 1    
                
            area = self.lineEdit_area.text()
            us = self.lineEdit_us.text()
            nr_individuo = self.lineEdit_individuo.text()
            eta_min = self.comboBox_eta_min.currentText()
            eta_max = self.comboBox_eta_max.currentText()   
            
            if area != "":
                if EC.data_is_int(area) == 0:
                    QMessageBox.warning(self, "ACHTUNG", "Feld Areal. \n Der Wert muss numerisch eingegeben werden",
                                        QMessageBox.Ok)
                    test = 1

            if us != "":
                if EC.data_is_int(us) == 0:
                    QMessageBox.warning(self, "ACHTUNG", "Feld SE. \n Der Wert muss numerisch eingegeben werden",
                                        QMessageBox.Ok)
                    test = 1
            if nr_individuo != "":
                if EC.data_is_int(nr_individuo) == 0:
                    QMessageBox.warning(self, "ACHTUNG", "Feld Individuel nr. \n Der Wert muss numerisch eingegeben werden",
                                        QMessageBox.Ok)
                    test = 1

            if eta_min != "":
                if EC.data_is_int(eta_min) == 0:
                    QMessageBox.warning(self, "ACHTUNG", "Feld Todesalters  min \n Der Wert muss numerisch eingegeben werden",
                                        QMessageBox.Ok)
                    test = 1

            if eta_max != "":
                if EC.data_is_int(eta_max) == 0:
                    QMessageBox.warning(self, "ACHTUNG", "Feld Todesalters  max \n Der Wert muss numerisch eingegeben werden",
                                        QMessageBox.Ok)
                    test = 1
        
        
        
        else:  
            if EC.data_is_empty(str(self.comboBox_sito.currentText())) == 0:
                QMessageBox.warning(self, "WARNING", "Site Field. \n The field must not be empty", QMessageBox.Ok)
                test = 1

            if EC.data_is_empty(str(self.lineEdit_area.text())) == 0:
                QMessageBox.warning(self, "WARNING", "Area Field. \n The field must not be empty", QMessageBox.Ok)
                test = 1

            if EC.data_is_empty(str(self.lineEdit_us.text())) == 0:
                QMessageBox.warning(self, "WARNING", "SU Field. \n The field must not be empty", QMessageBox.Ok)
                test = 1
                
            if EC.data_is_empty(str(self.lineEdit_individuo.text())) == 0:
                QMessageBox.warning(self, "WARNING", "Individual nr. Field. \n The field must not be empty",
                                    QMessageBox.Ok)
                test = 1    
                
            area = self.lineEdit_area.text()
            us = self.lineEdit_us.text()
            nr_individuo = self.lineEdit_individuo.text()
            eta_min = self.comboBox_eta_min.currentText()
            eta_max = self.comboBox_eta_max.currentText()   
            
            if area != "":
                if EC.data_is_int(area) == 0:
                    QMessageBox.warning(self, "WARNING", "Area Field. \n The value must be numerical",
                                        QMessageBox.Ok)
                    test = 1

            if us != "":
                if EC.data_is_int(us) == 0:
                    QMessageBox.warning(self, "WARNING", "SU Field. \n The value must be numerical",
                                        QMessageBox.Ok)
                    test = 1
            if nr_individuo != "":
                if EC.data_is_int(nr_individuo) == 0:
                    QMessageBox.warning(self, "WARNING", "Individual nr. Field. \n The value must be numerical",
                                        QMessageBox.Ok)
                    test = 1

            if eta_min != "":
                if EC.data_is_int(eta_min) == 0:
                    QMessageBox.warning(self, "WARNING", "Age min Field. \n The value must be numerical",
                                        QMessageBox.Ok)
                    test = 1

            if eta_max != "":
                if EC.data_is_int(eta_max) == 0:
                    QMessageBox.warning(self, "WARNING", "Age max Field. \n The value must be numerical",
                                        QMessageBox.Ok)
                    test = 1    
        return test

    def insert_new_rec(self):
        if self.comboBox_eta_min.currentText() == "":
            eta_min = None
        else:
            eta_min = int(self.comboBox_eta_min.currentText())

        if self.comboBox_eta_max.currentText() == "":
            eta_max = None
        else:
            eta_max = int(self.comboBox_eta_max.currentText())

        if self.comboBox_classi_eta.currentText() == "":
            classi_eta = ''
        else:
            classi_eta = str(self.comboBox_classi_eta.currentText())

        try:
            data = self.DB_MANAGER.insert_values_ind(
                self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE) + 1,
                str(self.comboBox_sito.currentText()),  # 1 - Sito
                str(self.lineEdit_area.text()),  # 2 - area
                int(self.lineEdit_us.text()),  # 3 - US
                int(self.lineEdit_individuo.text()),  # 4 - individuo
                str(self.lineEdit_data_schedatura.text()),  # 5 - data schedatura
                str(self.lineEdit_schedatore.text()),  # 6 - schedatore
                str(self.comboBox_sesso.currentText()),  # 7 - sesso
                eta_min,  # 8 - eta' min
                eta_max,  # 9 - eta' max
                classi_eta,  # 10 - classi eta
                str(self.textEdit_osservazioni.toPlainText())  # 11 - osservazioni
            )
            try:
                self.DB_MANAGER.insert_data_session(data)
                return 1
            except Exception as e:
                e_str = str(e)
                if e_str.__contains__("IntegrityError"):
                    
                    if self.L=='it':
                        msg = self.ID_TABLE + " gia' presente nel database"
                        QMessageBox.warning(self, "Error", "Error" + str(msg), QMessageBox.Ok)
                    elif self.L=='de':
                        msg = self.ID_TABLE + " bereits in der Datenbank"
                        QMessageBox.warning(self, "Error", "Error" + str(msg), QMessageBox.Ok)  
                    else:
                        msg = self.ID_TABLE + " exist in db"
                        QMessageBox.warning(self, "Error", "Error" + str(msg), QMessageBox.Ok)  
                else:
                    msg = e
                    QMessageBox.warning(self, "Error", "Error 1 \n" + str(msg), QMessageBox.Ok)
                return 0

        except Exception as e:
            QMessageBox.warning(self, "Error", "Error 2 \n" + str(e), QMessageBox.Ok)
            return 0

    def on_pushButton_insert_row_rapporti_pressed(self):
        self.insert_new_row('self.tableWidget_rapporti')

    def on_pushButton_insert_row_inclusi_pressed(self):
        self.insert_new_row('self.tableWidget_inclusi')

    def on_pushButton_insert_row_campioni_pressed(self):
        self.insert_new_row('self.tableWidget_campioni')

    def check_record_state(self):
        ec = self.data_error_check()
        if ec == 1:
            return 1  # ci sono errori di immissione
        elif self.records_equal_check() == 1 and ec == 0:
            if self.L=='it':
                self.update_if(
                
                    QMessageBox.warning(self, 'Errore', "Il record e' stato modificato. Vuoi salvare le modifiche?",
                                        QMessageBox.Ok | QMessageBox.Cancel))
            elif self.L=='de':
                self.update_if(
                    QMessageBox.warning(self, 'Errore', "Der Record wurde geändert. Möchtest du die Änderungen speichern?",
                                        QMessageBox.Ok | QMessageBox.Cancel))
            else:
                self.update_if(
                    QMessageBox.warning(self, "Error", "The record has been changed. You want to save the changes?",
                                        QMessageBox.Ok | QMessageBox.Cancel))
            # self.charge_records()
            return 0  # non ci sono errori di immissione

            # records surf functions

    def on_pushButton_view_all_pressed(self):
        if self.check_record_state() == 1:
            pass
        else:
            self.empty_fields()
            self.charge_records()
            self.fill_fields()
            self.BROWSE_STATUS = "b"
            self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
            if type(self.REC_CORR) == "<type 'str'>":
                corr = 0
            else:
                corr = self.REC_CORR
            self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR + 1)
            self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
            self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
            self.label_sort.setText(self.SORTED_ITEMS["n"])

            # records surf functions

    def on_pushButton_first_rec_pressed(self):
        if self.check_record_state() == 1:
            pass
        else:
            try:
                self.empty_fields()
                self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
                self.fill_fields(0)
                self.set_rec_counter(self.REC_TOT, self.REC_CORR + 1)
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e), QMessageBox.Ok)

    def on_pushButton_last_rec_pressed(self):
        if self.check_record_state() == 1:
            pass
        else:
            try:
                self.empty_fields()
                self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST) - 1
                self.fill_fields(self.REC_CORR)
                self.set_rec_counter(self.REC_TOT, self.REC_CORR + 1)
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e), QMessageBox.Ok)

    def on_pushButton_prev_rec_pressed(self):
        if self.check_record_state() == 1:
            pass
        else:
            self.REC_CORR = self.REC_CORR - 1
            if self.REC_CORR == -1:
                self.REC_CORR = 0
                if self.L=='it':
                    QMessageBox.warning(self, "Attenzione", "Sei al primo record!", QMessageBox.Ok)
                elif self.L=='de':
                    QMessageBox.warning(self, "Achtung", "du befindest dich im ersten Datensatz!", QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, "Warning", "You are to the first record!", QMessageBox.Ok)        
            else:
                try:
                    self.empty_fields()
                    self.fill_fields(self.REC_CORR)
                    self.set_rec_counter(self.REC_TOT, self.REC_CORR + 1)
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e), QMessageBox.Ok)

    def on_pushButton_next_rec_pressed(self):
        if self.check_record_state() == 1:
            pass
        else:
            self.REC_CORR = self.REC_CORR + 1
            if self.REC_CORR >= self.REC_TOT:
                self.REC_CORR = self.REC_CORR - 1
                if self.L=='it':
                    QMessageBox.warning(self, "Attenzione", "Sei all'ultimo record!", QMessageBox.Ok)
                elif self.L=='de':
                    QMessageBox.warning(self, "Achtung", "du befindest dich im letzten Datensatz!", QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, "Error", "You are to the first record!", QMessageBox.Ok)  
            else:
                try:
                    self.empty_fields()
                    self.fill_fields(self.REC_CORR)
                    self.set_rec_counter(self.REC_TOT, self.REC_CORR + 1)
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e), QMessageBox.Ok)

    def on_pushButton_delete_pressed(self):
        
        if self.L=='it':
            msg = QMessageBox.warning(self, "Attenzione!!!",
                                      "Vuoi veramente eliminare il record? \n L'azione è irreversibile",
                                      QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Cancel:
                QMessageBox.warning(self, "Messagio!!!", "Azione Annullata!")
            else:
                try:
                    id_to_delete = eval("self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE)
                    self.DB_MANAGER.delete_one_record(self.TABLE_NAME, self.ID_TABLE, id_to_delete)
                    self.charge_records()  # charge records from DB
                    QMessageBox.warning(self, "Messaggio!!!", "Record eliminato!")
                except Exception as e:
                    QMessageBox.warning(self, "Messaggio!!!", "Tipo di errore: " + str(e))
                if not bool(self.DATA_LIST):
                    QMessageBox.warning(self, "Attenzione", "Il database è vuoto!", QMessageBox.Ok)
                    self.DATA_LIST = []
                    self.DATA_LIST_REC_CORR = []
                    self.DATA_LIST_REC_TEMP = []
                    self.REC_CORR = 0
                    self.REC_TOT = 0
                    self.empty_fields()
                    self.set_rec_counter(0, 0)
                    # check if DB is empty
                if bool(self.DATA_LIST):
                    self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
                    self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
                    self.BROWSE_STATUS = "b"
                    self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
                    self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR + 1)
                    self.charge_list()
                    self.fill_fields()
        elif self.L=='de':
            msg = QMessageBox.warning(self, "Achtung!!!",
                                      "Willst du wirklich diesen Eintrag löschen? \n Der Vorgang ist unumkehrbar",
                                      QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Cancel:
                QMessageBox.warning(self, "Message!!!", "Aktion annulliert!")
            else:
                try:
                    id_to_delete = eval("self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE)
                    self.DB_MANAGER.delete_one_record(self.TABLE_NAME, self.ID_TABLE, id_to_delete)
                    self.charge_records()  # charge records from DB
                    QMessageBox.warning(self, "Message!!!", "Record gelöscht!")
                except Exception as e:
                    QMessageBox.warning(self, "Message!!!", "Errortyp: " + str(e))
                if not bool(self.DATA_LIST):
                    QMessageBox.warning(self, "Warning", "Die Datenbank ist leer!", QMessageBox.Ok)
                    self.DATA_LIST = []
                    self.DATA_LIST_REC_CORR = []
                    self.DATA_LIST_REC_TEMP = []
                    self.REC_CORR = 0
                    self.REC_TOT = 0
                    self.empty_fields()
                    self.set_rec_counter(0, 0)
                    # check if DB is empty
                if bool(self.DATA_LIST):
                    self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
                    self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
                    self.BROWSE_STATUS = "b"
                    self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
                    self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR + 1)
                    self.charge_list()
                    self.fill_fields()
        else:
            msg = QMessageBox.warning(self, "Warning!!!",
                                      "Do you really want to break the record? \n Action is irreversible.",
                                      QMessageBox.Ok | QMessageBox.Cancel)
            if msg == QMessageBox.Cancel:
                QMessageBox.warning(self, "Messagio!!!", "Action deleted!")
            else:
                try:
                    id_to_delete = eval("self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE)
                    self.DB_MANAGER.delete_one_record(self.TABLE_NAME, self.ID_TABLE, id_to_delete)
                    self.charge_records()  # charge records from DB
                    QMessageBox.warning(self, "Message!!!", "Record deleted!")
                except Exception as e:
                    QMessageBox.warning(self, "Message!!!", "error type: " + str(e))
                if not bool(self.DATA_LIST):
                    QMessageBox.warning(self, "Warning", "the db is empty!", QMessageBox.Ok)
                    self.DATA_LIST = []
                    self.DATA_LIST_REC_CORR = []
                    self.DATA_LIST_REC_TEMP = []
                    self.REC_CORR = 0
                    self.REC_TOT = 0
                    self.empty_fields()
                    self.set_rec_counter(0, 0)
                    # check if DB is empty
                if bool(self.DATA_LIST):
                    self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
                    self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
                    self.BROWSE_STATUS = "b"
                    self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
                    self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR + 1)
                    self.charge_list()
                    self.fill_fields()  
            
            
            
            self.SORT_STATUS = "n"
            self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])

    def on_pushButton_new_search_pressed(self):
        if self.check_record_state() == 1:
            pass
        else:
            self.enable_button_search(0)
            # set the GUI for a new search

            if self.BROWSE_STATUS != "f":
                self.BROWSE_STATUS = "f"
                ###

                self.setComboBoxEditable(["self.comboBox_sito"], 1)
                self.setComboBoxEnable(["self.comboBox_sito"], "True")
                self.setComboBoxEnable(["self.lineEdit_area"], "True")
                self.setComboBoxEnable(["self.lineEdit_us"], "True")
                self.setComboBoxEnable(["self.lineEdit_individuo"], "True")
                self.setComboBoxEnable(["self.textEdit_osservazioni"], "False")

                ###
                self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
                self.set_rec_counter('', '')
                self.label_sort.setText(self.SORTED_ITEMS["n"])
                self.charge_list()
                self.empty_fields()

    def on_pushButton_search_go_pressed(self):
        if self.BROWSE_STATUS != "f":
            if self.L=='it':
                QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",
                                    QMessageBox.Ok)
            elif self.L=='de':
                QMessageBox.warning(self, "ACHTUNG", "Um eine neue Abfrage zu starten drücke  'new search' ",
                                    QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "WARNING", "To perform a new search click on the 'new search' button ",
                                    QMessageBox.Ok)  
        else:
            if self.lineEdit_us.text() != "":
                us = int(self.lineEdit_us.text())
            else:
                us = ""

            if self.lineEdit_individuo.text() != "":
                individuo = int(self.lineEdit_individuo.text())
            else:
                individuo = ""

            if self.comboBox_eta_min.currentText() != "":
                eta_min = int(self.comboBox_eta_min.currentText())
            else:
                eta_min = ""

            if self.comboBox_eta_max.currentText() != "":
                eta_max = int(self.comboBox_eta_max.currentText())
            else:
                eta_max = ""

            search_dict = {
                self.TABLE_FIELDS[0]: "'" + str(self.comboBox_sito.currentText()) + "'",  # 1 - Sito
                self.TABLE_FIELDS[1]: "'" + str(self.lineEdit_area.text()) + "'",  # 2 - Area
                self.TABLE_FIELDS[2]: us,  # 3 - US
                self.TABLE_FIELDS[3]: individuo,  # 4 - individuo
                self.TABLE_FIELDS[4]: "'" + str(self.lineEdit_data_schedatura.text()) + "'",  # 5 - data schedatura
                self.TABLE_FIELDS[5]: "'" + str(self.lineEdit_schedatore.text()) + "'",  # 6 - schedatore
                self.TABLE_FIELDS[6]: "'" + str(self.comboBox_sesso.currentText()) + "'",  # 7 - sesso
                self.TABLE_FIELDS[7]: eta_min,  # 8 - eta min
                self.TABLE_FIELDS[8]: eta_max,  # 9 - eta max
                self.TABLE_FIELDS[9]: "'" + str(self.comboBox_classi_eta.currentText()) + "'",  # 10 - classi eta
                self.TABLE_FIELDS[10]: str(self.textEdit_osservazioni.toPlainText())  # 11 - osservazioni
            }

            u = Utility()
            search_dict = u.remove_empty_items_fr_dict(search_dict)
            if not bool(search_dict):
                if self.L=='it':
                    QMessageBox.warning(self, "ATTENZIONE", "Non è stata impostata nessuna ricerca!!!", QMessageBox.Ok)
                elif self.L=='de':
                    QMessageBox.warning(self, "ACHTUNG", "Keine Abfrage definiert!!!", QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, " WARNING", "No search has been set!!!", QMessageBox.Ok) 
            else:
                res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
                if not bool(res):
                
                    if self.L=='it':
                        QMessageBox.warning(self, "ATTENZIONE", "Non e' stato trovato alcun record!", QMessageBox.Ok)
                    elif self.L=='de':
                        QMessageBox.warning(self, "ACHTUNG", "kein Eintrag gefunden!", QMessageBox.Ok)
                    else:
                        QMessageBox.warning(self, "Warning", "The record has not been found ", QMessageBox.Ok)

                        self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR + 1)
                        self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
                        self.fill_fields(self.REC_CORR)
                        self.BROWSE_STATUS = "b"
                        self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])

                        self.setComboBoxEnable(["self.comboBox_sito"], "False")
                        self.setComboBoxEnable(["self.lineEdit_area"], "False")
                        self.setComboBoxEnable(["self.lineEdit_us"], "False")
                        self.setComboBoxEnable(["self.lineEdit_individuo"], "False")
                        self.setComboBoxEnable(["self.textEdit_osservazioni"], "True")
                else:
                    self.DATA_LIST = []
                    for i in res:
                        self.DATA_LIST.append(i)
                    self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
                    self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
                    self.fill_fields()
                    self.BROWSE_STATUS = "b"
                    self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
                    self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR + 1)
                    if self.L=='it':
                        if self.REC_TOT == 1:
                            strings = ("E' stato trovato", self.REC_TOT, "record")
                            if self.toolButtonGis.isChecked():
                                id_us_list = self.charge_id_us_for_individuo()
                                self.pyQGIS.charge_individui_us(id_us_list)
                                self.pyQGIS.charge_individui_from_research(self.DATA_LIST)

                        else:
                            strings = ("Sono stati trovati", self.REC_TOT, "records")
                            if self.toolButtonGis.isChecked():
                                id_us_list = self.charge_id_us_for_individuo()
                                self.pyQGIS.charge_individui_us(id_us_list)
                                self.pyQGIS.charge_individui_from_research(self.DATA_LIST)
                    
                    elif self.L=='de':
                        if self.REC_TOT == 1:
                            strings = ("Es wurde gefunden", self.REC_TOT, "record")
                            if self.toolButtonGis.isChecked():
                                id_us_list = self.charge_id_us_for_individuo()
                                self.pyQGIS.charge_individui_us(id_us_list)
                                self.pyQGIS.charge_individui_from_research(self.DATA_LIST)

                        else:
                            strings = ("Sie wurden gefunden", self.REC_TOT, "records")
                            if self.toolButtonGis.isChecked():
                                id_us_list = self.charge_id_us_for_individuo()
                                self.pyQGIS.charge_individui_us(id_us_list)
                                self.pyQGIS.charge_individui_from_research(self.DATA_LIST)
                                
                    else:
                        if self.REC_TOT == 1:
                            strings = ("It has been found", self.REC_TOT, "record")
                            if self.toolButtonGis.isChecked():
                                id_us_list = self.charge_id_us_for_individuo()
                                self.pyQGIS.charge_individui_us(id_us_list)
                                self.pyQGIS.charge_individui_from_research(self.DATA_LIST)

                        else:
                            strings = ("They have been found", self.REC_TOT, "records")
                            if self.toolButtonGis.isChecked():
                                id_us_list = self.charge_id_us_for_individuo()
                                self.pyQGIS.charge_individui_us(id_us_list)
                                self.pyQGIS.charge_individui_from_research(self.DATA_LIST)          
                    self.setComboBoxEnable(["self.comboBox_sito"], "False")
                    self.setComboBoxEnable(["self.lineEdit_area"], "False")
                    self.setComboBoxEnable(["self.lineEdit_us"], "False")
                    self.setComboBoxEnable(["self.lineEdit_individuo"], "False")
                    self.setComboBoxEnable(["self.textEdit_osservazioni"], "True")
                    QMessageBox.warning(self, "Message", "%s %d %s" % strings, QMessageBox.Ok)

        self.enable_button_search(1)

    def update_if(self, msg):
        rec_corr = self.REC_CORR
        if msg == QMessageBox.Ok:
            test = self.update_record()
            if test == 1:
                id_list = []
                for i in self.DATA_LIST:
                    id_list.append(eval("i." + self.ID_TABLE))
                self.DATA_LIST = []
                if self.SORT_STATUS == "n":
                    temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc',
                                                                self.MAPPER_TABLE_CLASS,
                                                                self.ID_TABLE)  # self.DB_MANAGER.query_bool(self.SEARCH_DICT_TEMP, self.MAPPER_TABLE_CLASS) #
                else:
                    temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE,
                                                                self.MAPPER_TABLE_CLASS, self.ID_TABLE)
                for i in temp_data_list:
                    self.DATA_LIST.append(i)
                self.BROWSE_STATUS = "b"
                self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
                if type(self.REC_CORR) == "<type 'str'>":
                    corr = 0
                else:
                    corr = self.REC_CORR
                return 1
            elif test == 0:
                return 0

                # custom functions

    def charge_records(self):
        self.DATA_LIST = []

        if self.DB_SERVER == 'sqlite':
            for i in self.DB_MANAGER.query(self.MAPPER_TABLE_CLASS):
                self.DATA_LIST.append(i)
        else:
            id_list = []
            for i in self.DB_MANAGER.query(self.MAPPER_TABLE_CLASS):
                id_list.append(eval("i." + self.ID_TABLE))

            temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS,
                                                        self.ID_TABLE)

            for i in temp_data_list:
                self.DATA_LIST.append(i)

    def datestrfdate(self):
        now = date.today()
        today = now.strftime("%d-%m-%Y")
        return today

    def table2dict(self, n):
        self.tablename = n
        row = eval(self.tablename + ".rowCount()")
        col = eval(self.tablename + ".columnCount()")
        lista = []
        for r in range(row):
            sub_list = []
            for c in range(col):
                value = eval(self.tablename + ".item(r,c)")
                if value != None:
                    sub_list.append(str(value.text()))

            if bool(sub_list):
                lista.append(sub_list)

        return lista

    def tableInsertData(self, t, d):
        pass
        """
        self.table_name = t
        self.data_list = eval(d)
        self.data_list.sort()

        #column table count
        table_col_count_cmd = ("%s.columnCount()") % (self.table_name)
        table_col_count = eval(table_col_count_cmd)

        #clear table
        table_clear_cmd = ("%s.clearContents()") % (self.table_name)
        eval(table_clear_cmd)

        for i in range(table_col_count):
            table_rem_row_cmd = ("%s.removeRow(%d)") % (self.table_name, i)
            eval(table_rem_row_cmd)

        #for i in range(len(self.data_list)):
            #self.insert_new_row(self.table_name)

        for row in range(len(self.data_list)):
            cmd = ('%s.insertRow(%s)') % (self.table_name, row)
            eval(cmd)
            for col in range(len(self.data_list[row])):
                #item = self.comboBox_sito.setEditText(self.data_list[0][col]
                item = QTableWidgetItem(self.data_list[row][col])
                exec_str = ('%s.setItem(%d,%d,item)') % (self.table_name,row,col)
                eval(exec_str)
        """

    def insert_new_row(self, table_name):
        """insert new row into a table based on table_name"""
        cmd = table_name + ".insertRow(0)"
        eval(cmd)

    def empty_fields(self):
        # rapporti_row_count = self.tableWidget_rapporti.rowCount()
        # campioni_row_count = self.tableWidget_campioni.rowCount()
        # inclusi_row_count = self.tableWidget_inclusi.rowCount()

        self.comboBox_sito.setEditText("")  # 1 - Sito
        self.lineEdit_area.clear()  # 2 - area
        self.lineEdit_us.clear()  # 3 - US
        self.lineEdit_data_schedatura.clear()  # 4 - data schedatura
        self.lineEdit_schedatore.clear()  # 5 - schedatore
        self.lineEdit_individuo.clear()  # 6 - individuo
        self.comboBox_sesso.setEditText("")  # 7 - sesso
        self.comboBox_eta_min.setEditText("")  # 8 - eta' minima
        self.comboBox_eta_max.setEditText("")  # 9 - eta' massima
        self.comboBox_classi_eta.setEditText("")  # 10 - classi di eta'
        self.textEdit_osservazioni.clear()  # 11 - osservazioni

    def fill_fields(self, n=0):
        self.rec_num = n
        try:
            self.comboBox_sito.setEditText(str(self.DATA_LIST[self.rec_num].sito))  # 1 - Sito
            self.lineEdit_area.setText(str(self.DATA_LIST[self.rec_num].area))  # 2 - area
            self.lineEdit_us.setText(str(self.DATA_LIST[self.rec_num].us))  # 3 - us
            self.lineEdit_individuo.setText(str(self.DATA_LIST[self.rec_num].nr_individuo))  # 4 - nr individuo
            self.lineEdit_data_schedatura.setText(
                str(self.DATA_LIST[self.rec_num].data_schedatura))  # 5 - data schedatura
            self.lineEdit_schedatore.setText(str(self.DATA_LIST[self.rec_num].schedatore))  # 6 - schedatore
            self.comboBox_sesso.setEditText(str(self.DATA_LIST[self.rec_num].sesso))  # 7 - sesso

            if self.DATA_LIST[self.rec_num].eta_min == None:  # 8 - eta minima
                self.comboBox_eta_min.setEditText("")
            else:
                self.comboBox_eta_min.setEditText(str(self.DATA_LIST[self.rec_num].eta_min))

            if self.DATA_LIST[self.rec_num].eta_max == None:  # 9 - eta massima
                self.comboBox_eta_max.setEditText("")
            else:
                self.comboBox_eta_max.setEditText(str(self.DATA_LIST[self.rec_num].eta_max))

            self.comboBox_classi_eta.setEditText(str(self.DATA_LIST[self.rec_num].classi_eta))  # 10 - classi di eta

            str(self.textEdit_osservazioni.setText(self.DATA_LIST[self.rec_num].osservazioni))  # 11 - osservazioni
            if self.toolButtonPreview.isChecked():
                self.loadMapPreview()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e), QMessageBox.Ok)

    def set_rec_counter(self, t, c):
        self.rec_tot = t
        self.rec_corr = c
        self.label_rec_tot.setText(str(self.rec_tot))
        self.label_rec_corrente.setText(str(self.rec_corr))

    def set_LIST_REC_TEMP(self):
        if self.comboBox_eta_min.currentText() == "":
            eta_min = None
        else:
            eta_min = self.comboBox_eta_min.currentText()

        if self.comboBox_eta_max.currentText() == "":
            eta_max = None
        else:
            eta_max = self.comboBox_eta_max.currentText()

            # data
        self.DATA_LIST_REC_TEMP = [
            str(self.comboBox_sito.currentText()),  # 1 - Sito
            str(self.lineEdit_area.text()),  # 2 - Area
            str(self.lineEdit_us.text()),  # 3 - US
            str(self.lineEdit_individuo.text()),  # 4 - individuo
            str(self.lineEdit_data_schedatura.text()),  # 5 - data schedatura
            str(self.lineEdit_schedatore.text()),  # 6 - schedatore
            str(self.comboBox_sesso.currentText()),  # 7 - sesso
            str(eta_min),  # 8- eta minima
            str(eta_max),  # 9 - eta massima
            str(self.comboBox_classi_eta.currentText()),  # 10 - classi eta
            str(self.textEdit_osservazioni.toPlainText())]  # 11 - osservazioni

    def set_LIST_REC_CORR(self):
        self.DATA_LIST_REC_CORR = []
        for i in self.TABLE_FIELDS:
            self.DATA_LIST_REC_CORR.append(eval("unicode(self.DATA_LIST[self.REC_CORR]." + i + ")"))

    def records_equal_check(self):
        self.set_LIST_REC_TEMP()
        self.set_LIST_REC_CORR()

        if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
            return 0
        else:
            return 1

    def setComboBoxEditable(self, f, n):
        field_names = f
        value = n

        for fn in field_names:
            cmd = '{}{}{}{}'.format(fn, '.setEditable(', n, ')')
            eval(cmd)

    def setComboBoxEnable(self, f, v):
        field_names = f
        value = v

        for fn in field_names:
            cmd = '{}{}{}{}'.format(fn, '.setEnabled(', v, ')')
            eval(cmd)

    def update_record(self):
        try:
            self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS,
                                   self.ID_TABLE,
                                   [eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE + ")")],
                                   self.TABLE_FIELDS,
                                   self.rec_toupdate())
            return 1
        except Exception as e:
            QMessageBox.warning(self, "Messaggio",
                                "encoding problem: accents or characters not accepted by the database have been inserted. If you close the card now without correcting the errors you will lose the data. Make a copy of everything on a separate word sheet. Error :" + str(
                                    e), QMessageBox.Ok)
            return 0

    def rec_toupdate(self):
        rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)

        # f = open('/test_rec_to_update_ind.txt', 'w')
        # f.write(str(rec_to_update))
        # f.close()

        return rec_to_update

    def charge_id_us_for_individuo(self):
        data_list_us = []
        for rec in range(len(self.DATA_LIST)):
            sito = "'" + str(self.DATA_LIST[rec].sito) + "'"
            area = "'" + str(self.DATA_LIST[rec].area) + "'"
            us = int(self.DATA_LIST[rec].us)

            serch_dict_us = {'sito': sito, 'area': area, 'us': us}
            us_ind = self.DB_MANAGER.query_bool(serch_dict_us, "US")
            data_list_us.append(us_ind)

        data_list_id_us = []
        for us in range(len(data_list_us)):
            data_list_id_us.append(data_list_us[us][0].id_us)

        return data_list_id_us

    def testing(self, name_file, message):
        f = open(str(name_file), 'w')
        f.write(str(message))
        f.close()

## Class end
