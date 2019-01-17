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

from qgis.PyQt.QtWidgets import QApplication, QDialog
from qgis.PyQt.uic import loadUiType

import os
import configparser

MAIN_DIALOG_CLASS, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'ui', 'pyarchinitInfoDialog.ui'))


class pyArchInitDialog_Info(QDialog, MAIN_DIALOG_CLASS):
    def __init__(self, parent=None, db=None):
        QDialog.__init__(self, parent)
        # Set up the user interface from Designer.
        self.setupUi(self)

        config = configparser.ConfigParser()
        metadata_file = os.path.join(os.path.dirname(__file__), os.pardir, 'metadata.txt')
        config.read(metadata_file)
        self.text = "<b>PyArchinit version: " + config['general']['version'] + "</b><br>" \
                    "<i>Archeological GIS Tools - PyArchInit it's a tool to manage archaeological dataset with an high portability on the main platform</i><br><br>"

        self.text += """<b>Developers:</b><br>
                        Luca Mandolesi<br>
                        adArte snc - Rimini - www.adartesnc.com<br>
                        Enzo Cocca<br>
                        Simona Gugnali<br><br>
                        """
        self.text += """<b>Special thanks for testing to:</b><br>
                        Giovanni Manghi<br>
                        Jerzy Sikora<br>
                        Michele Zappitelli<br>
                        Chiara Cesaretti<br>
                        Chiara Di Fronzo<br>
                        Valeria Casicci<br>
                        Fabio Alboni<br>
                        Yuri Godino<br>
                        Manuela Battaglia<br>
                        Tommaso Gallo<br><br>
                        """
        self.text += """<b>and supporting to:</b><br>
                        Stefano Costa<br>
                        Francesco de Virgilio<br>
                        Giuseppe Naponiello<br><br>
                         """
        self.text += """<b>Help:</b><br>
                        http://groups.google.it/group/pyarchinit-users<br>
                        or email me pyarchinit@gmail.com<br><br>
                        """
        self.text += """<b>Site:</b><br>
                        <a href="https://sites.google.com/site/pyarchinit/">https://sites.google.com/site/pyarchinit/</a>
        """
        self.textBrowser.setText(self.text)

