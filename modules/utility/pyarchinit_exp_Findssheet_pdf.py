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

from datetime import date

from builtins import object
from builtins import range
from builtins import str
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, PageBreak, SimpleDocTemplate, Spacer, TableStyle, Image
from reportlab.platypus.paragraph import Paragraph

from .pyarchinit_OS_utility import *


class NumberedCanvas_Findssheet(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def define_position(self, pos):
        self.page_position(pos)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.drawRightString(200 * mm, 20 * mm,
                             "Pag. %d di %d" % (self._pageNumber, page_count))  # scheda us verticale 200mm x 20 mm


class NumberedCanvas_FINDSindex(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def define_position(self, pos):
        self.page_position(pos)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.drawRightString(270 * mm, 10 * mm,
                             "Pag. %d di %d" % (self._pageNumber, page_count))  # scheda us verticale 200mm x 20 mm


class NumberedCanvas_CASSEindex(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def define_position(self, pos):
        self.page_position(pos)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.drawRightString(270 * mm, 10 * mm,
                             "Pag. %d di %d" % (self._pageNumber, page_count))  # scheda us verticale 200mm x 20 mm


class single_Finds_pdf_sheet(object):
    def __init__(self, data):
        self.id_invmat = data[0]
        self.sito = data[1]
        self.numero_inventario = data[2]
        self.tipo_reperto = data[3]
        self.criterio_schedatura = data[4]
        self.definizione = data[5]
        self.descrizione = data[6]
        self.area = data[7]
        self.us = data[8]
        self.lavato = data[9]
        self.nr_cassa = data[10]
        self.luogo_conservazione = data[11]
        self.stato_conservazione = data[12]
        self.datazione_reperto = data[13]
        self.elementi_reperto = data[14]
        self.misurazioni = data[15]
        self.rif_biblio = data[16]
        self.tecnologie = data[17]
        self.repertato = data[21]
        self.diagnostico = data[22]

    def datestrfdate(self):
        now = date.today()
        today = now.strftime("%d-%m-%Y")
        return today

    def create_sheet(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT

        styleSheet = getSampleStyleSheet()
        styDescrizione = styleSheet['Normal']
        styDescrizione.spaceBefore = 20
        styDescrizione.spaceAfter = 20
        styDescrizione.alignment = 4  # Justified

        # format labels

        # 0 row
        intestazione = Paragraph("<b>SCHEDA INVENTARIO REPERTI<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
        # intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        logo = Image(logo_path)

        ##      if test_image.drawWidth < 800:

        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch

        # 1 row
        sito = Paragraph("<b>Sito</b><br/>" + str(self.sito), styNormal)
        nr_inventario = Paragraph("<b>Nr. Inventario</b><br/>" + str(self.numero_inventario), styNormal)

        # 2 row
        riferimenti_stratigrafici = Paragraph("<b>Riferimenti stratigrafici</b>", styNormal)
        area = Paragraph("<b>Area</b><br/>" + str(self.area), styNormal)
        us = Paragraph("<b>US</b><br/>" + str(self.us), styNormal)

        # 3 row
        criterio_schedatura = Paragraph("<b>Criterio schedatura</b><br/>" + self.criterio_schedatura, styNormal)
        tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>" + self.tipo_reperto, styNormal)
        definizione = Paragraph("<b>Definizione</b><br/>" + self.definizione, styNormal)

        # 4 row
        stato_conservazione = Paragraph("<b>Stato Conservazione</b><br/>" + self.stato_conservazione, styNormal)
        datazione = Paragraph("<b>Datazione</b><br/>" + self.datazione_reperto, styNormal)

        # 5 row
        descrizione = ''
        try:
            descrizione = Paragraph("<b>Descrizione</b><br/>" + str(self.descrizione), styDescrizione)
        except:
            pass

            # 6 row
        elementi_reperto = ''
        if eval(self.elementi_reperto):
            for i in eval(self.elementi_reperto):
                if elementi_reperto == '':
                    try:
                        elementi_reperto += ("Elemento rinvenuto: %s, Unita' di misura: %s, Quantita': %s") % (
                        str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass
                else:
                    try:
                        elementi_reperto += ("<br/>Elemento rinvenuto: %s, Unita' di misura: %s, Quantita': %s") % (
                        str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass

        elementi_reperto = Paragraph("<b>Elementi reperto</b><br/>" + elementi_reperto, styNormal)

        # 7 row
        misurazioni = ''
        if eval(self.misurazioni):
            for i in eval(self.misurazioni):
                if misurazioni == '':
                    try:
                        misurazioni += ("%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass
                else:
                    try:
                        misurazioni += ("<br/>%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass
        misurazioni = Paragraph("<b>Misurazioni</b><br/>" + misurazioni, styNormal)

        # 8 row
        tecnologie = ''
        if eval(self.tecnologie):
            for i in eval(self.tecnologie):
                if tecnologie == '':
                    try:
                        tecnologie += (
                                      "Tipo tecnologia: %s, Posizione: %s, Tipo quantita': %s, Unita' di misura: %s, Quantita': %s") % (
                                      str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass
                else:
                    try:
                        tecnologie += (
                                      "<br/>Tipo tecnologia: %s, Posizione: %s, Tipo quantita': %s, Unita' di misura: %s, Quantita': %s") % (
                                      str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass
        tecnologie = Paragraph("<b>Tecnologie</b><br/>" + tecnologie, styNormal)

        # 9 row
        rif_biblio = ''
        if eval(self.rif_biblio):
            for i in eval(self.rif_biblio):  # gigi
                if rif_biblio == '':
                    try:
                        rif_biblio += ("<b>Autore: %s, Anno: %s, Titolo: %s, Pag.: %s, Fig.: %s") % (
                        str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass
                else:
                    try:
                        rif_biblio += ("<b>Autore: %s, Anno: %s, Titolo: %s, Pag.: %s, Fig.: %s") % (
                        str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass

        rif_biblio = Paragraph("<b>Riferimenti bibliografici</b><br/>" + rif_biblio, styNormal)

        # 11 row
        repertato = Paragraph("<b>Repertato</b><br/>" + self.repertato, styNormal)
        diagnostico = Paragraph("<b>Diagnostico</b><br/>" + self.diagnostico, styNormal)

        # 12 row
        riferimenti_magazzino = Paragraph("<b>Riferimenti magazzino</b>", styNormal)

        # 13 row
        lavato = Paragraph("<b>Lavato</b><br/>" + self.lavato, styNormal)
        nr_cassa = Paragraph("<b>Nr. Cassa</b><br/>" + self.nr_cassa, styNormal)
        luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + self.luogo_conservazione, styNormal)

        # schema
        cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
            [intestazione, '01', '02', '03', '04', '05', '06', logo, '08', '09'],  # 0 row ok
            [sito, '01', '02', '03', '04', '05', '06', '07', nr_inventario, '09'],  # 1 row ok
            [riferimenti_stratigrafici, '01', '02', '03', area, '05', '06', us, '08', '09'],  # 2 row ok
            [tipo_reperto, '01', '02', criterio_schedatura, '04', '05', definizione, '07', '08', '09'],
            # 3 row ok
            [datazione, '01', '02', '03', '04', stato_conservazione, '06', '07', '08', '09'],  # 4 row ok
            [descrizione, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 5 row ok
            [elementi_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 6 row ok
            [misurazioni, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 7 row ok
            [tecnologie, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 8 row ok
            [rif_biblio, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 9 row ok
            [riferimenti_stratigrafici, '02', '03', '04', '05', '06', '07', '08', '09'],  # 10 row ok
            [repertato, '01', '02', diagnostico, '04', '05', '06', '07', '08', '09'],  # 11 row ok
            [riferimenti_magazzino, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 12 row ok
            [lavato, '01', '02', nr_cassa, '04', '05', luogo_conservazione, '07', '08', '09']  # 13 row ok
        ]

        # table style
        table_style = [

            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

            # 0 row
            ('SPAN', (0, 0), (6, 0)),  # intestazione
            ('SPAN', (7, 0), (9, 0)),  # intestazione

            # 1 row
            ('SPAN', (0, 1), (7, 1)),  # sito
            ('SPAN', (8, 1), (9, 1)),  # nr_inventario

            # 2 row
            ('SPAN', (0, 2), (3, 2)),  # rif stratigrafici
            ('SPAN', (4, 2), (6, 2)),  # area
            ('SPAN', (7, 2), (9, 2)),  # us
            ('VALIGN', (0, 2), (9, 2), 'TOP'),

            # 3 row
            ('SPAN', (0, 3), (2, 3)),  # tipo_reperto
            ('SPAN', (3, 3), (5, 3)),  # criterio_schedatura
            ('SPAN', (6, 3), (9, 3)),  # definizione
            ('VALIGN', (0, 3), (9, 3), 'TOP'),

            # 4 row
            ('SPAN', (0, 4), (4, 4)),  # datazione
            ('SPAN', (5, 4), (9, 4)),  # conservazione

            # 5 row
            ('SPAN', (0, 5), (9, 5)),  # descrizione

            # 6 row
            ('SPAN', (0, 6), (9, 6)),  # elementi_reperto

            # 7 row
            ('SPAN', (0, 7), (9, 7)),  # misurazioni

            # 8 row
            ('SPAN', (0, 8), (9, 8)),  # tecnologie

            # 9 row
            ('SPAN', (0, 9), (9, 9)),  # bibliografia

            # 10 row
            ('SPAN', (0, 10), (9, 10)),  # Riferimenti stratigrafici - Titolo

            # 11 row
            ('SPAN', (0, 11), (2, 11)),  # Riferimenti stratigrafici - area
            ('SPAN', (3, 11), (9, 11)),  # Riferimenti stratigrafici - us

            # 12 row
            ('SPAN', (0, 12), (9, 12)),  # Riferimenti magazzino - Titolo

            # 13 row
            ('SPAN', (0, 13), (2, 13)),  # Riferimenti magazzino - lavato
            ('SPAN', (3, 13), (5, 13)),  # Riferimenti magazzino - nr_cassa
            ('SPAN', (6, 13), (9, 13)),  # Riferimenti magazzino - luogo conservazione

            ('VALIGN', (0, 0), (-1, -1), 'TOP')

        ]

        t = Table(cell_schema, colWidths=50, rowHeights=None, style=table_style)

        return t

    def create_sheet_de(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT

        styleSheet = getSampleStyleSheet()
        styDescrizione = styleSheet['Normal']
        styDescrizione.spaceBefore = 20
        styDescrizione.spaceAfter = 20
        styDescrizione.alignment = 4  # Justified

        # format labels

        # 0 row
        intestazione = Paragraph("<b>FORMULAR MATERIALINVENTAR<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
        # intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo_de.jpg')
        logo = Image(logo_path)

        ##      if test_image.drawWidth < 800:

        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch

        # 1 row
        sito = Paragraph("<b>Ausgrabungsstätte</b><br/>" + str(self.sito), styNormal)
        nr_inventario = Paragraph("<b>Referenzmaterial Best.-Nr.</b><br/>" + str(self.numero_inventario), styNormal)

        # 2 row
        riferimenti_stratigrafici = Paragraph("<b>Stratigraphische Referenz</b>", styNormal)
        area = Paragraph("<b>Areal</b><br/>" + str(self.area), styNormal)
        us = Paragraph("<b>SE</b><br/>" + str(self.us), styNormal)

        # 3 row
        criterio_schedatura = Paragraph("<b>Anmeldeparameter</b><br/>" + self.criterio_schedatura, styNormal)
        tipo_reperto = Paragraph("<b>Art der Feststellung</b><br/>" + self.tipo_reperto, styNormal)
        definizione = Paragraph("<b>Definition</b><br/>" + self.definizione, styNormal)

        # 4 row
        stato_conservazione = Paragraph("<b>Erhaltungsstatus</b><br/>" + self.stato_conservazione, styNormal)
        datazione = Paragraph("<b>Datierung</b><br/>" + self.datazione_reperto, styNormal)

        # 5 row
        descrizione = ''
        try:
            descrizione = Paragraph("<b>Beschreibung</b><br/>" + str(self.descrizione), styDescrizione)
        except:
            pass

            # 6 row
        elementi_reperto = ''
        if eval(self.elementi_reperto):
            for i in eval(self.elementi_reperto):
                if elementi_reperto == '':
                    try:
                        elementi_reperto += ("Gegenstand gefunden: %s, Maßeinheit: %s, Menge: %s") % (
                        str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass
                else:
                    try:
                        elementi_reperto += ("Gegenstand gefunden: %s, Maßeinheit: %s, Menge: %s") % (
                        str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass

        elementi_reperto = Paragraph("<b>Artefakt - Teile</b><br/>" + elementi_reperto, styNormal)

        # 7 row
        misurazioni = ''
        if eval(self.misurazioni):
            for i in eval(self.misurazioni):
                if misurazioni == '':
                    try:
                        misurazioni += ("%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass
                else:
                    try:
                        misurazioni += ("<br/>%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass
        misurazioni = Paragraph("<b>Messungen</b><br/>" + misurazioni, styNormal)

        # 8 row
        tecnologie = ''
        if eval(self.tecnologie):
            for i in eval(self.tecnologie):
                if tecnologie == '':
                    try:
                        tecnologie += (
                                      "<br/>Technologies: %s, Position: %s, Quantitätstyp: %s, Maßeinheit: %s, Quantita': %s") % (
                                      str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass
                else:
                    try:
                        tecnologie += (
                                      "<br/>Technologies: %s, Position: %s, Quantitätstyp: %s, Maßeinheit: %s, Quantita': %s") % (
                                      str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass
        tecnologie = Paragraph("<b>Technologies</b><br/>" + tecnologie, styNormal)

        # 9 row
        rif_biblio = ''
        if eval(self.rif_biblio):
            for i in eval(self.rif_biblio):  # gigi
                if rif_biblio == '':
                    try:
                        rif_biblio += ("<b>Autor: %s, Jahr: %s, Titel: %s, Seite: %s, Bild: %s") % (
                        str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass
                else:
                    try:
                        rif_biblio += ("<b>Autor: %s, Jahr: %s, Titel: %s, Seite: %s, Bild: %s") % (
                        str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass

        rif_biblio = Paragraph("<b>Referenzen</b><br/>" + rif_biblio, styNormal)

        # 11 row
        repertato = Paragraph("<b>Abgerufen</b><br/>" + self.repertato, styNormal)
        diagnostico = Paragraph("<b>Diagnose</b><br/>" + self.diagnostico, styNormal)

        # 12 row
        riferimenti_magazzino = Paragraph("<b>Bestandsdaten</b>", styNormal)

        # 13 row
        lavato = Paragraph("<b>Gewaschen</b><br/>" + self.lavato, styNormal)
        nr_cassa = Paragraph("<b>Nr. Box</b><br/>" + self.nr_cassa, styNormal)
        luogo_conservazione = Paragraph("<b>Ort der Erhaltung</b><br/>" + self.luogo_conservazione, styNormal)

        # schema
        cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
            [intestazione, '01', '02', '03', '04', '05', '06', logo, '08', '09'],  # 0 row ok
            [sito, '01', '02', '03', '04', '05', '06', '07', nr_inventario, '09'],  # 1 row ok
            [riferimenti_stratigrafici, '01', '02', '03', area, '05', '06', us, '08', '09'],  # 2 row ok
            [tipo_reperto, '01', '02', criterio_schedatura, '04', '05', definizione, '07', '08', '09'],
            # 3 row ok
            [datazione, '01', '02', '03', '04', stato_conservazione, '06', '07', '08', '09'],  # 4 row ok
            [descrizione, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 5 row ok
            [elementi_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 6 row ok
            [misurazioni, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 7 row ok
            [tecnologie, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 8 row ok
            [rif_biblio, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 9 row ok
            [riferimenti_stratigrafici, '02', '03', '04', '05', '06', '07', '08', '09'],  # 10 row ok
            [repertato, '01', '02', diagnostico, '04', '05', '06', '07', '08', '09'],  # 11 row ok
            [riferimenti_magazzino, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 12 row ok
            [lavato, '01', '02', nr_cassa, '04', '05', luogo_conservazione, '07', '08', '09']  # 13 row ok
        ]

        # table style
        table_style = [

            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

            # 0 row
            ('SPAN', (0, 0), (6, 0)),  # intestazione
            ('SPAN', (7, 0), (9, 0)),  # intestazione

            # 1 row
            ('SPAN', (0, 1), (7, 1)),  # sito
            ('SPAN', (8, 1), (9, 1)),  # nr_inventario

            # 2 row
            ('SPAN', (0, 2), (3, 2)),  # rif stratigrafici
            ('SPAN', (4, 2), (6, 2)),  # area
            ('SPAN', (7, 2), (9, 2)),  # us
            ('VALIGN', (0, 2), (9, 2), 'TOP'),

            # 3 row
            ('SPAN', (0, 3), (2, 3)),  # tipo_reperto
            ('SPAN', (3, 3), (5, 3)),  # criterio_schedatura
            ('SPAN', (6, 3), (9, 3)),  # definizione
            ('VALIGN', (0, 3), (9, 3), 'TOP'),

            # 4 row
            ('SPAN', (0, 4), (4, 4)),  # datazione
            ('SPAN', (5, 4), (9, 4)),  # conservazione

            # 5 row
            ('SPAN', (0, 5), (9, 5)),  # descrizione

            # 6 row
            ('SPAN', (0, 6), (9, 6)),  # elementi_reperto

            # 7 row
            ('SPAN', (0, 7), (9, 7)),  # misurazioni

            # 8 row
            ('SPAN', (0, 8), (9, 8)),  # tecnologie

            # 9 row
            ('SPAN', (0, 9), (9, 9)),  # bibliografia

            # 10 row
            ('SPAN', (0, 10), (9, 10)),  # Riferimenti stratigrafici - Titolo

            # 11 row
            ('SPAN', (0, 11), (2, 11)),  # Riferimenti stratigrafici - area
            ('SPAN', (3, 11), (9, 11)),  # Riferimenti stratigrafici - us

            # 12 row
            ('SPAN', (0, 12), (9, 12)),  # Riferimenti magazzino - Titolo

            # 13 row
            ('SPAN', (0, 13), (2, 13)),  # Riferimenti magazzino - lavato
            ('SPAN', (3, 13), (5, 13)),  # Riferimenti magazzino - nr_cassa
            ('SPAN', (6, 13), (9, 13)),  # Riferimenti magazzino - luogo conservazione

            ('VALIGN', (0, 0), (-1, -1), 'TOP')

        ]

        t = Table(cell_schema, colWidths=50, rowHeights=None, style=table_style)

        return t
        
    def create_sheet_en(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT

        styleSheet = getSampleStyleSheet()
        styDescrizione = styleSheet['Normal']
        styDescrizione.spaceBefore = 20
        styDescrizione.spaceAfter = 20
        styDescrizione.alignment = 4  # Justified

        # format labels

        # 0 row
        intestazione = Paragraph("<b>ARTEFACT FORM<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
        # intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        logo = Image(logo_path)

        ##      if test_image.drawWidth < 800:

        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch

        # 1 row
        sito = Paragraph("<b>Site</b><br/>" + str(self.sito), styNormal)
        nr_inventario = Paragraph("<b>Inventary Nr.</b><br/>" + str(self.numero_inventario), styNormal)

        # 2 row
        riferimenti_stratigrafici = Paragraph("<b>Stratigraphic Reference</b>", styNormal)
        area = Paragraph("<b>Area</b><br/>" + str(self.area), styNormal)
        us = Paragraph("<b>SU</b><br/>" + str(self.us), styNormal)

        # 3 row
        criterio_schedatura = Paragraph("<b>Scheduling criteria</b><br/>" + self.criterio_schedatura, styNormal)
        tipo_reperto = Paragraph("<b>Artefact Type</b><br/>" + self.tipo_reperto, styNormal)
        definizione = Paragraph("<b>Definition</b><br/>" + self.definizione, styNormal)

        # 4 row
        stato_conservazione = Paragraph("<b>Status of conservation</b><br/>" + self.stato_conservazione, styNormal)
        datazione = Paragraph("<b>Datation</b><br/>" + self.datazione_reperto, styNormal)

        # 5 row
        descrizione = ''
        try:
            descrizione = Paragraph("<b>Description</b><br/>" + str(self.descrizione), styDescrizione)
        except:
            pass

            # 6 row
        elementi_reperto = ''
        if eval(self.elementi_reperto):
            for i in eval(self.elementi_reperto):
                if elementi_reperto == '':
                    try:
                        elementi_reperto += ("<br/>Finds: %s, Measure unit: %s, Quantity: %s") % (
                        str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass
                else:
                    try:
                        elementi_reperto += ("<br/>Finds: %s, Measure unit: %s, Quantity: %s") % (
                        str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass

        elementi_reperto = Paragraph("<b>Finds</b><br/>" + elementi_reperto, styNormal)

        # 7 row
        misurazioni = ''
        if eval(self.misurazioni):
            for i in eval(self.misurazioni):
                if misurazioni == '':
                    try:
                        misurazioni += ("%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass
                else:
                    try:
                        misurazioni += ("<br/>%s: %s %s") % (str(i[0]), str(i[1]), str(i[2]))
                    except:
                        pass
        misurazioni = Paragraph("<b>Measurement</b><br/>" + misurazioni, styNormal)

        # 8 row
        tecnologie = ''
        if eval(self.tecnologie):
            for i in eval(self.tecnologie):
                if tecnologie == '':
                    try:
                        tecnologie += (
                                      "<br/>Technologies: %s, Position: %s, Quantity type: %s, Measure unit: %s, Quantity: %s") % (
                                      str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass
                else:
                    try:
                        tecnologie += (
                                      "<br/>Technologies: %s, Position: %s, Quantity type: %s, Measure unit: %s, Quantity: %s") % (
                                      str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass
        tecnologie = Paragraph("<b>Technologies</b><br/>" + tecnologie, styNormal)

        # 9 row
        rif_biblio = ''
        if eval(self.rif_biblio):
            for i in eval(self.rif_biblio):  # gigi
                if rif_biblio == '':
                    try:
                        rif_biblio += ("<b>Author: %s, Year: %s, Title: %s, Pag.: %s, Fig.: %s") % (
                        str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass
                else:
                    try:
                        rif_biblio += ("<b>Author: %s, Year: %s, Title: %s, Pag.: %s, Fig.: %s") % (
                        str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]))
                    except:
                        pass

        rif_biblio = Paragraph("<b>Bibliography reference</b><br/>" + rif_biblio, styNormal)

        # 11 row
        repertato = Paragraph("<b>Found</b><br/>" + self.repertato, styNormal)
        diagnostico = Paragraph("<b>Diagnostico</b><br/>" + self.diagnostico, styNormal)

        # 12 row
        riferimenti_magazzino = Paragraph("<b>Store</b>", styNormal)

        # 13 row
        lavato = Paragraph("<b>Whashed</b><br/>" + self.lavato, styNormal)
        nr_cassa = Paragraph("<b>Box</b><br/>" + self.nr_cassa, styNormal)
        luogo_conservazione = Paragraph("<b>Place of conservation</b><br/>" + self.luogo_conservazione, styNormal)

        # schema
        cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
            [intestazione, '01', '02', '03', '04', '05', '06', logo, '08', '09'],  # 0 row ok
            [sito, '01', '02', '03', '04', '05', '06', '07', nr_inventario, '09'],  # 1 row ok
            [riferimenti_stratigrafici, '01', '02', '03', area, '05', '06', us, '08', '09'],  # 2 row ok
            [tipo_reperto, '01', '02', criterio_schedatura, '04', '05', definizione, '07', '08', '09'],
            # 3 row ok
            [datazione, '01', '02', '03', '04', stato_conservazione, '06', '07', '08', '09'],  # 4 row ok
            [descrizione, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 5 row ok
            [elementi_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 6 row ok
            [misurazioni, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 7 row ok
            [tecnologie, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 8 row ok
            [rif_biblio, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 9 row ok
            [riferimenti_stratigrafici, '02', '03', '04', '05', '06', '07', '08', '09'],  # 10 row ok
            [repertato, '01', '02', diagnostico, '04', '05', '06', '07', '08', '09'],  # 11 row ok
            [riferimenti_magazzino, '01', '02', '03', '04', '05', '06', '07', '08', '09'],  # 12 row ok
            [lavato, '01', '02', nr_cassa, '04', '05', luogo_conservazione, '07', '08', '09']  # 13 row ok
        ]

        # table style
        table_style = [

            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

            # 0 row
            ('SPAN', (0, 0), (6, 0)),  # intestazione
            ('SPAN', (7, 0), (9, 0)),  # intestazione

            # 1 row
            ('SPAN', (0, 1), (7, 1)),  # sito
            ('SPAN', (8, 1), (9, 1)),  # nr_inventario

            # 2 row
            ('SPAN', (0, 2), (3, 2)),  # rif stratigrafici
            ('SPAN', (4, 2), (6, 2)),  # area
            ('SPAN', (7, 2), (9, 2)),  # us
            ('VALIGN', (0, 2), (9, 2), 'TOP'),

            # 3 row
            ('SPAN', (0, 3), (2, 3)),  # tipo_reperto
            ('SPAN', (3, 3), (5, 3)),  # criterio_schedatura
            ('SPAN', (6, 3), (9, 3)),  # definizione
            ('VALIGN', (0, 3), (9, 3), 'TOP'),

            # 4 row
            ('SPAN', (0, 4), (4, 4)),  # datazione
            ('SPAN', (5, 4), (9, 4)),  # conservazione

            # 5 row
            ('SPAN', (0, 5), (9, 5)),  # descrizione

            # 6 row
            ('SPAN', (0, 6), (9, 6)),  # elementi_reperto

            # 7 row
            ('SPAN', (0, 7), (9, 7)),  # misurazioni

            # 8 row
            ('SPAN', (0, 8), (9, 8)),  # tecnologie

            # 9 row
            ('SPAN', (0, 9), (9, 9)),  # bibliografia

            # 10 row
            ('SPAN', (0, 10), (9, 10)),  # Riferimenti stratigrafici - Titolo

            # 11 row
            ('SPAN', (0, 11), (2, 11)),  # Riferimenti stratigrafici - area
            ('SPAN', (3, 11), (9, 11)),  # Riferimenti stratigrafici - us

            # 12 row
            ('SPAN', (0, 12), (9, 12)),  # Riferimenti magazzino - Titolo

            # 13 row
            ('SPAN', (0, 13), (2, 13)),  # Riferimenti magazzino - lavato
            ('SPAN', (3, 13), (5, 13)),  # Riferimenti magazzino - nr_cassa
            ('SPAN', (6, 13), (9, 13)),  # Riferimenti magazzino - luogo conservazione

            ('VALIGN', (0, 0), (-1, -1), 'TOP')

        ]

        t = Table(cell_schema, colWidths=50, rowHeights=None, style=table_style)

        return t    
class Box_labels_Finds_pdf_sheet(object):
    def __init__(self, data, sito):
        self.sito = sito  # Sito
        self.cassa = data[0]  # 1 - Cassa
        self.elenco_inv_tip_rep = data[1]  # 2-  elenco US
        self.elenco_us = data[2]  # 3 - elenco Inventari
        self.luogo_conservazione = data[3]  # 4 - luogo conservazione

    def datestrfdate(self):
        now = date.today()
        today = now.strftime("%d-%m-%Y")
        return today

    def create_sheet(self):
        styleSheet = getSampleStyleSheet()

        styleSheet.add(ParagraphStyle(name='Cassa Label'))
        styleSheet.add(ParagraphStyle(name='Sito Label'))

        styCassaLabel = styleSheet['Cassa Label']
        styCassaLabel.spaceBefore = 0
        styCassaLabel.spaceAfter = 0
        styCassaLabel.alignment = 2  # RIGHT
        styCassaLabel.leading = 25
        styCassaLabel.fontSize = 30

        stySitoLabel = styleSheet['Sito Label']
        stySitoLabel.spaceBefore = 0
        stySitoLabel.spaceAfter = 0
        stySitoLabel.alignment = 0  # LEFT
        stySitoLabel.leading = 25
        stySitoLabel.fontSize = 18
        stySitoLabel.fontStyle = 'bold'

        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 10
        styNormal.spaceAfter = 10
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 14
        styNormal.leading = 15

        # format labels
        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        logo = Image(logo_path)

        ##      if test_image.drawWidth < 800:

        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch

        num_cassa = Paragraph("<b>N. Cassa </b>" + str(self.cassa), styCassaLabel)
        sito = Paragraph("<b>Sito: </b>" + str(self.sito), stySitoLabel)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>Elenco N. Inv. / Tipo materiale</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>Elenco N. Inv. / Tipo materiale</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>Elenco US/(Struttura)</b>", styNormal)
        else:
            elenco_us = Paragraph("<b>Elenco US/(Struttura)</b><br/>" + str(self.elenco_us), styNormal)

            # luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

            # schema
        cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
            [logo, '01', '02', '03', '04', '05', num_cassa, '07', '08', '09'],
            [sito, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_us, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_inv_tip_rep, '01', '02', '03', '04', '05', '06', '07', '08', '09']

        ]

        # table style
        table_style = [

            ('GRID', (0, 0), (-1, -1), 0, colors.white),  # ,0.0,colors.black
            # 0 row
            ('SPAN', (0, 0), (5, 0)),  # elenco US
            ('SPAN', (6, 0), (9, 0)),  # elenco US
            ('HALIGN', (0, 0), (9, 0), 'LEFT'),
            ('VALIGN', (6, 0), (9, 0), 'TOP'),
            ('HALIGN', (6, 0), (9, 0), 'RIGHT'),

            ('SPAN', (0, 1), (9, 1)),  # elenco US
            ('HALIGN', (0, 1), (9, 1), 'LEFT'),

            ('SPAN', (0, 2), (9, 2)),  # intestazione
            ('VALIGN', (0, 2), (9, 2), 'TOP'),
            # 1 row
            ('SPAN', (0, 3), (9, 3)),  # elenco US
            ('VALIGN', (0, 3), (9, 3), 'TOP')

        ]

        colWidths = None
        rowHeights = None
        # colWidths=[80,80,80, 80,80, 80,80,80,80, 80]
        t = Table(cell_schema, colWidths, rowHeights, style=table_style)

        return t

    def create_sheet_de(self):
        styleSheet = getSampleStyleSheet()

        styleSheet.add(ParagraphStyle(name='Cassa Label'))
        styleSheet.add(ParagraphStyle(name='Sito Label'))

        styCassaLabel = styleSheet['Cassa Label']
        styCassaLabel.spaceBefore = 0
        styCassaLabel.spaceAfter = 0
        styCassaLabel.alignment = 2  # RIGHT
        styCassaLabel.leading = 25
        styCassaLabel.fontSize = 30

        stySitoLabel = styleSheet['Sito Label']
        stySitoLabel.spaceBefore = 0
        stySitoLabel.spaceAfter = 0
        stySitoLabel.alignment = 0  # LEFT
        stySitoLabel.leading = 25
        stySitoLabel.fontSize = 18
        stySitoLabel.fontStyle = 'bold'

        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 10
        styNormal.spaceAfter = 10
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 14
        styNormal.leading = 15

        # format labels
        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo_de.jpg')
        logo = Image(logo_path)

        ##      if test_image.drawWidth < 800:

        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch

        num_cassa = Paragraph("<b>Nr. Box</b>" + str(self.cassa), styCassaLabel)
        sito = Paragraph("<b>Ausgrabungsstätte: </b>" + str(self.sito), stySitoLabel)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>Liste N. Inv. / Art material</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>Liste N. Inv. / Art material</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>Liste SE/(Struktur)</b>", styNormal)
        else:
            elenco_us = Paragraph("<b>Liste SE/(Struktur)</b><br/>" + str(self.elenco_us), styNormal)

            # luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

            # schema
        cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
            [logo, '01', '02', '03', '04', '05', num_cassa, '07', '08', '09'],
            [sito, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_us, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_inv_tip_rep, '01', '02', '03', '04', '05', '06', '07', '08', '09']

        ]

        # table style
        table_style = [

            ('GRID', (0, 0), (-1, -1), 0, colors.white),  # ,0.0,colors.black
            # 0 row
            ('SPAN', (0, 0), (5, 0)),  # elenco US
            ('SPAN', (6, 0), (9, 0)),  # elenco US
            ('HALIGN', (0, 0), (9, 0), 'LEFT'),
            ('VALIGN', (6, 0), (9, 0), 'TOP'),
            ('HALIGN', (6, 0), (9, 0), 'RIGHT'),

            ('SPAN', (0, 1), (9, 1)),  # elenco US
            ('HALIGN', (0, 1), (9, 1), 'LEFT'),

            ('SPAN', (0, 2), (9, 2)),  # intestazione
            ('VALIGN', (0, 2), (9, 2), 'TOP'),
            # 1 row
            ('SPAN', (0, 3), (9, 3)),  # elenco US
            ('VALIGN', (0, 3), (9, 3), 'TOP')

        ]

        colWidths = None
        rowHeights = None
        # colWidths=[80,80,80, 80,80, 80,80,80,80, 80]
        t = Table(cell_schema, colWidths, rowHeights, style=table_style)

        return t
        
    def create_sheet_en(self):
        styleSheet = getSampleStyleSheet()

        styleSheet.add(ParagraphStyle(name='Cassa Label'))
        styleSheet.add(ParagraphStyle(name='Sito Label'))

        styCassaLabel = styleSheet['Cassa Label']
        styCassaLabel.spaceBefore = 0
        styCassaLabel.spaceAfter = 0
        styCassaLabel.alignment = 2  # RIGHT
        styCassaLabel.leading = 25
        styCassaLabel.fontSize = 30

        stySitoLabel = styleSheet['Sito Label']
        stySitoLabel.spaceBefore = 0
        stySitoLabel.spaceAfter = 0
        stySitoLabel.alignment = 0  # LEFT
        stySitoLabel.leading = 25
        stySitoLabel.fontSize = 18
        stySitoLabel.fontStyle = 'bold'

        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 10
        styNormal.spaceAfter = 10
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 14
        styNormal.leading = 15

        # format labels
        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')
        logo = Image(logo_path)

        ##      if test_image.drawWidth < 800:

        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch

        num_cassa = Paragraph("<b>Box</b>" + str(self.cassa), styCassaLabel)
        sito = Paragraph("<b>Site: </b>" + str(self.sito), stySitoLabel)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>List N. Inv. / Material type</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>List N. Inv. / Material type</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>List SU/(Structure)</b>", styNormal)
        else:
            elenco_us = Paragraph("<b>List SU/(Structure)</b><br/>" + str(self.elenco_us), styNormal)

            # luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

            # schema
        cell_schema = [  # 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
            [logo, '01', '02', '03', '04', '05', num_cassa, '07', '08', '09'],
            [sito, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_us, '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            [elenco_inv_tip_rep, '01', '02', '03', '04', '05', '06', '07', '08', '09']

        ]

        # table style
        table_style = [

            ('GRID', (0, 0), (-1, -1), 0, colors.white),  # ,0.0,colors.black
            # 0 row
            ('SPAN', (0, 0), (5, 0)),  # elenco US
            ('SPAN', (6, 0), (9, 0)),  # elenco US
            ('HALIGN', (0, 0), (9, 0), 'LEFT'),
            ('VALIGN', (6, 0), (9, 0), 'TOP'),
            ('HALIGN', (6, 0), (9, 0), 'RIGHT'),

            ('SPAN', (0, 1), (9, 1)),  # elenco US
            ('HALIGN', (0, 1), (9, 1), 'LEFT'),

            ('SPAN', (0, 2), (9, 2)),  # intestazione
            ('VALIGN', (0, 2), (9, 2), 'TOP'),
            # 1 row
            ('SPAN', (0, 3), (9, 3)),  # elenco US
            ('VALIGN', (0, 3), (9, 3), 'TOP')

        ]

        colWidths = None
        rowHeights = None
        # colWidths=[80,80,80, 80,80, 80,80,80,80, 80]
        t = Table(cell_schema, colWidths, rowHeights, style=table_style)

        return t    
class CASSE_index_pdf_sheet(object):
    def __init__(self, data):
        self.cassa = data[0]  # 1 - Cassa
        self.elenco_inv_tip_rep = data[1]  # 2-  elenco US
        self.elenco_us = data[2]  # 3 - elenco Inventari
        self.luogo_conservazione = data[3]  # 4 - luogo conservazione

    def getTable(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 10

        # self.unzip_rapporti_stratigrafici()

        num_cassa = Paragraph("<b>Nr.</b><br/>" + str(self.cassa), styNormal)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>N. Inv./Tipo materiale</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>N. Inv./Tipo materiale</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>US(Struttura)</b><br/>", styNormal)
        else:
            elenco_us = Paragraph("<b>US(Struttura)</b><br/>" + str(self.elenco_us), styNormal)

        luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione), styNormal)

        data = [num_cassa,
                elenco_inv_tip_rep,
                elenco_us,
                luogo_conservazione]

        return data
        
    def getTable_de(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 10

        # self.unzip_rapporti_stratigrafici()

        num_cassa = Paragraph("<b>Nr.</b><br/>" + str(self.cassa), styNormal)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>Liste N. Inv. / Art material</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>Liste N. Inv. / Art material</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>SE(Struktur)</b><br/>", styNormal)
        else:
            elenco_us = Paragraph("<b>SE(Struktur)</b><br/>" + str(self.elenco_us), styNormal)

        luogo_conservazione = Paragraph("<b>Ort der Erhaltung</b><br/>" + str(self.luogo_conservazione), styNormal)

        data = [num_cassa,
                elenco_inv_tip_rep,
                elenco_us,
                luogo_conservazione]

        return data
        
    def getTable_en(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 10

        # self.unzip_rapporti_stratigrafici()

        num_cassa = Paragraph("<b>Nr.</b><br/>" + str(self.cassa), styNormal)

        if self.elenco_inv_tip_rep == None:
            elenco_inv_tip_rep = Paragraph("<b>N. Inv. / Material type</b><br/>", styNormal)
        else:
            elenco_inv_tip_rep = Paragraph("<b>N. Inv. / Material type</b><br/>" + str(self.elenco_inv_tip_rep),
                                           styNormal)

        if self.elenco_us == None:
            elenco_us = Paragraph("<b>SU(Structure)</b><br/>", styNormal)
        else:
            elenco_us = Paragraph("<b>SU(Structure)</b><br/>" + str(self.elenco_us), styNormal)

        luogo_conservazione = Paragraph("<b>Place of conservation</b><br/>" + str(self.luogo_conservazione), styNormal)

        data = [num_cassa,
                elenco_inv_tip_rep,
                elenco_us,
                luogo_conservazione]

        return data 
    def makeStyles(self):
        styles = TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.0, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP')])  # finale

        return styles


class FINDS_index_pdf_sheet(object):
    def __init__(self, data):
        self.sito = data[1]  # 1 - sito
        self.num_inventario = data[2]  # 2- numero_inventario
        self.tipo_reperto = data[3]  # 3 - tipo_reperto
        self.criterio_schedatura = data[4]  # 4 - criterio_schedatura
        self.definizione = data[5]  # 5 - definizione
        self.area = data[7]  # 7 - area
        self.us = data[8]  # 8 - us
        self.lavato = data[9]  # 9 - lavato
        self.numero_cassa = data[10]  # 10 - numero cassa
        self.repertato = data[21]  # 22 - repertato
        self.diagnostico = data[22]  # 23 - diagnostico

    def getTable(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 9

        # self.unzip_rapporti_stratigrafici()

        num_inventario = Paragraph("<b>N. Inv.</b><br/>" + str(self.num_inventario), styNormal)

        if self.tipo_reperto == None:
            tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>", styNormal)
        else:
            tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>" + str(self.tipo_reperto), styNormal)

        if self.criterio_schedatura == None:
            classe_materiale = Paragraph("<b>Classe materiale</b><br/>", styNormal)
        else:
            classe_materiale = Paragraph("<b>Classe materiale</b><br/>" + str(self.criterio_schedatura), styNormal)

        if self.definizione == None:
            definizione = Paragraph("<b>Definizione</b><br/>", styNormal)
        else:
            definizione = Paragraph("<b>Definizione</b><br/>" + str(self.definizione), styNormal)

        if str(self.area) == "None":
            area = Paragraph("<b>Area</b><br/>", styNormal)
        else:
            area = Paragraph("<b>Area</b><br/>" + str(self.area), styNormal)

        if str(self.us) == "None":
            us = Paragraph("<b>US</b><br/>", styNormal)
        else:
            us = Paragraph("<b>US</b><br/>" + str(self.us), styNormal)

        if self.lavato == None:
            lavato = Paragraph("<b>Lavato</b><br/>", styNormal)
        else:
            lavato = Paragraph("<b>Lavato</b><br/>" + str(self.lavato), styNormal)

        if self.repertato == None:
            repertato = Paragraph("<b>Repertato</b><br/>", styNormal)
        else:
            repertato = Paragraph("<b>Repertato</b><br/>" + str(self.repertato), styNormal)

        if self.diagnostico == None:
            diagnostico = Paragraph("<b>Diagnostico</b><br/>", styNormal)
        else:
            diagnostico = Paragraph("<b>Diagnostico</b><br/>" + str(self.diagnostico), styNormal)

        if str(self.numero_cassa) == "None":
            nr_cassa = Paragraph("<b>Nr. Cassa</b><br/>", styNormal)
        else:
            nr_cassa = Paragraph("<b>Nr. Cassa</b><br/>" + str(self.numero_cassa), styNormal)

        data = [num_inventario,
                tipo_reperto,
                classe_materiale,
                definizione,
                area,
                us,
                lavato,
                repertato,
                diagnostico,
                nr_cassa]

        return data
    
    def getTable_de(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 9

        # self.unzip_rapporti_stratigrafici()

        num_inventario = Paragraph("<b>Nr. Inv.</b><br/>" + str(self.num_inventario), styNormal)

        if self.tipo_reperto == None:
            tipo_reperto = Paragraph("<b>Funde Art</b><br/>", styNormal)
        else:
            tipo_reperto = Paragraph("<b>Funde Art</b><br/>" + str(self.tipo_reperto), styNormal)

        if self.criterio_schedatura == None:
            classe_materiale = Paragraph("<b>Materialklasse</b><br/>", styNormal)
        else:
            classe_materiale = Paragraph("<b>Materialklasse</b><br/>" + str(self.criterio_schedatura), styNormal)

        if self.definizione == None:
            definizione = Paragraph("<b>Definition</b><br/>", styNormal)
        else:
            definizione = Paragraph("<b>Definition</b><br/>" + str(self.definizione), styNormal)

        if str(self.area) == "None":
            area = Paragraph("<b>Areal</b><br/>", styNormal)
        else:
            area = Paragraph("<b>Areal</b><br/>" + str(self.area), styNormal)

        if str(self.us) == "None":
            us = Paragraph("<b>SE</b><br/>", styNormal)
        else:
            us = Paragraph("<b>SE</b><br/>" + str(self.us), styNormal)

        if self.lavato == None:
            lavato = Paragraph("<b>Gewaschen</b><br/>", styNormal)
        else:
            lavato = Paragraph("<b>Gewaschen</b><br/>" + str(self.lavato), styNormal)

        if self.repertato == None:
            repertato = Paragraph("<b>Abgerufen</b><br/>", styNormal)
        else:
            repertato = Paragraph("<b>Abgerufen</b><br/>" + str(self.repertato), styNormal)

        if self.diagnostico == None:
            diagnostico = Paragraph("<b>Diagnose</b><br/>", styNormal)
        else:
            diagnostico = Paragraph("<b>Diagnose</b><br/>" + str(self.diagnostico), styNormal)

        if str(self.numero_cassa) == "None":
            nr_cassa = Paragraph("<b>Nr. Box</b><br/>", styNormal)
        else:
            nr_cassa = Paragraph("<b>Nr. Box</b><br/>" + str(self.numero_cassa), styNormal)

        data = [num_inventario,
                tipo_reperto,
                classe_materiale,
                definizione,
                area,
                us,
                lavato,
                repertato,
                diagnostico,
                nr_cassa]

        return data
        
    def getTable_en(self):
        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styNormal.spaceBefore = 20
        styNormal.spaceAfter = 20
        styNormal.alignment = 0  # LEFT
        styNormal.fontSize = 9

        # self.unzip_rapporti_stratigrafici()

        num_inventario = Paragraph("<b>Inventary Nr.</b><br/>" + str(self.num_inventario), styNormal)

        if self.tipo_reperto == None:
            tipo_reperto = Paragraph("<b>Find Type</b><br/>", styNormal)
        else:
            tipo_reperto = Paragraph("<b>Find Type</b><br/>" + str(self.tipo_reperto), styNormal)

        if self.criterio_schedatura == None:
            classe_materiale = Paragraph("<b>Material Class</b><br/>", styNormal)
        else:
            classe_materiale = Paragraph("<b>Material Class</b><br/>" + str(self.criterio_schedatura), styNormal)

        if self.definizione == None:
            definizione = Paragraph("<b>Definition</b><br/>", styNormal)
        else:
            definizione = Paragraph("<b>Definition</b><br/>" + str(self.definizione), styNormal)

        if str(self.area) == "None":
            area = Paragraph("<b>Area</b><br/>", styNormal)
        else:
            area = Paragraph("<b>Area</b><br/>" + str(self.area), styNormal)

        if str(self.us) == "None":
            us = Paragraph("<b>SU</b><br/>", styNormal)
        else:
            us = Paragraph("<b>SU</b><br/>" + str(self.us), styNormal)

        if self.lavato == None:
            lavato = Paragraph("<b>Whashed</b><br/>", styNormal)
        else:
            lavato = Paragraph("<b>Whashed</b><br/>" + str(self.lavato), styNormal)

        if self.repertato == None:
            repertato = Paragraph("<b>Found</b><br/>", styNormal)
        else:
            repertato = Paragraph("<b>Found</b><br/>" + str(self.repertato), styNormal)

        if self.diagnostico == None:
            diagnostico = Paragraph("<b>Diagnostic</b><br/>", styNormal)
        else:
            diagnostico = Paragraph("<b>Diagnostic</b><br/>" + str(self.diagnostico), styNormal)

        if str(self.numero_cassa) == "None":
            nr_cassa = Paragraph("<b>Box Nr.</b><br/>", styNormal)
        else:
            nr_cassa = Paragraph("<b>Box Nr.</b><br/>" + str(self.numero_cassa), styNormal)

        data = [num_inventario,
                tipo_reperto,
                classe_materiale,
                definizione,
                area,
                us,
                lavato,
                repertato,
                diagnostico,
                nr_cassa]

        return data 
    def makeStyles(self):
        styles = TableStyle([('GRID', (0, 0), (-1, -1), 0.0, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP')
                             ])  # finale

        return styles


class generate_reperti_pdf(object):
    HOME = os.environ['PYARCHINIT_HOME']

    PDF_path = '{}{}{}'.format(HOME, os.sep, "pyarchinit_PDF_folder")

    def datestrfdate(self):
        now = date.today()
        today = now.strftime("%d-%m-%Y")
        return today

    def build_Finds_sheets(self, records):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = single_Finds_pdf_sheet(records[i])
            elements.append(single_finds_sheet.create_sheet())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep,'scheda_materiali.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f)
        doc.build(elements, canvasmaker=NumberedCanvas_Findssheet)
        f.close()
    def build_Finds_sheets_de(self, records):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = single_Finds_pdf_sheet(records[i])
            elements.append(single_finds_sheet.create_sheet_de())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'Formular_Finds.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f)
        doc.build(elements, canvasmaker=NumberedCanvas_Findssheet)
        f.close()
    def build_Finds_sheets_en(self, records):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = single_Finds_pdf_sheet(records[i])
            elements.append(single_finds_sheet.create_sheet_en())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'Finds_form.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f)
        doc.build(elements, canvasmaker=NumberedCanvas_Findssheet)
        f.close()   
    def build_index_Finds(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')

        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()

        lst = []
        lst.append(logo)
        lst.append(Paragraph("<b>ELENCO MATERIALI</b><br/><b>Scavo: %s,  Data: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FINDS_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable())

        styles = exp_index.makeStyles()
        colWidths = [70, 110, 110, 110, 35, 35, 60, 60, 60, 60]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'elenco_materiali.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    def build_index_Finds_de(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo_de.jpg')

        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()

        lst = []
        lst.append(logo)
        lst.append(Paragraph("<b>LISTE MATERIAL</b><br/><b>Ausgrabungsstätte: %s,  Datum: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FINDS_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_de())

        styles = exp_index.makeStyles()
        colWidths = [70, 110, 110, 110, 35, 35, 60, 60, 60, 60]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'liste_material.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()
    def build_index_Finds_en(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')

        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()

        lst = []
        lst.append(logo)
        lst.append(Paragraph("<b>LIST MATERIAL</b><br/><b>Site: %s,  Data: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = FINDS_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_en())

        styles = exp_index.makeStyles()
        colWidths = [70, 110, 110, 110, 35, 35, 60, 60, 60, 60]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'list_material.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

        f.close()   
    def build_index_Casse(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')

        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()
        lst = [logo]
        lst.append(Paragraph("<b>ELENCO CASSE MATERIALI</b><br/><b>Scavo: %s,  Data: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = CASSE_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable())

        styles = exp_index.makeStyles()
        colWidths = [20, 350, 250, 100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        # table_data_formatted.setStyle(styles)

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'elenco_casse.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        # doc.build(lst, canvasmaker=NumberedCanvas_Sindex)
        doc.build(lst)

        f.close()
    def build_index_Casse_de(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo_de.jpg')

        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()
        lst = [logo]
        lst.append(Paragraph("<b>LISTE BOX MATERIAL</b><br/><b>Scavo: %s,  Data: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = CASSE_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_de())

        styles = exp_index.makeStyles()
        colWidths = [20, 350, 250, 100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        # table_data_formatted.setStyle(styles)

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'liste_box.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        # doc.build(lst, canvasmaker=NumberedCanvas_Sindex)
        doc.build(lst)

        f.close()
    def build_index_Casse_en(self, records, sito):
        home = os.environ['PYARCHINIT_HOME']

        home_DB_path = '{}{}{}'.format(home, os.sep, 'pyarchinit_DB_folder')
        logo_path = '{}{}{}'.format(home_DB_path, os.sep, 'logo.jpg')

        logo = Image(logo_path)
        logo.drawHeight = 1.5 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.5 * inch
        logo.hAlign = "LEFT"

        styleSheet = getSampleStyleSheet()
        styNormal = styleSheet['Normal']
        styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
        styH1 = styleSheet['Heading3']

        data = self.datestrfdate()
        lst = [logo]
        lst.append(Paragraph("<b>LISTE BOX MATERIAL</b><br/><b>Scavo: %s,  Data: %s</b>" % (sito, data), styH1))

        table_data = []
        for i in range(len(records)):
            exp_index = CASSE_index_pdf_sheet(records[i])
            table_data.append(exp_index.getTable_en())

        styles = exp_index.makeStyles()
        colWidths = [20, 350, 250, 100]

        table_data_formatted = Table(table_data, colWidths, style=styles)
        table_data_formatted.hAlign = "LEFT"

        # table_data_formatted.setStyle(styles)

        lst.append(table_data_formatted)
        lst.append(Spacer(0, 0))

        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'list_box.pdf')
        f = open(filename, "wb")

        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0, topMargin=15, bottomMargin=40,
                                leftMargin=30, rightMargin=30)
        # doc.build(lst, canvasmaker=NumberedCanvas_Sindex)
        doc.build(lst)

        f.close()   
    def build_box_labels_Finds(self, records, sito):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = Box_labels_Finds_pdf_sheet(records[i], sito)
            elements.append(single_finds_sheet.create_sheet())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'etichette_casse_materiali.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0.0, topMargin=20, bottomMargin=20,
                                leftMargin=20, rightMargin=20)
        doc.build(elements)
        f.close()
    def build_box_labels_Finds_de(self, records, sito):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = Box_labels_Finds_pdf_sheet(records[i], sito)
            elements.append(single_finds_sheet.create_sheet_de())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'liste_box_material.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0.0, topMargin=20, bottomMargin=20,
                                leftMargin=20, rightMargin=20)
        doc.build(elements)
        f.close()
    def build_box_labels_Finds_en(self, records, sito):
        elements = []
        for i in range(len(records)):
            single_finds_sheet = Box_labels_Finds_pdf_sheet(records[i], sito)
            elements.append(single_finds_sheet.create_sheet_en())
            elements.append(PageBreak())
        filename = '{}{}{}'.format(self.PDF_path, os.sep, 'list_box_material.pdf')
        f = open(filename, "wb")
        doc = SimpleDocTemplate(f, pagesize=(29 * cm, 21 * cm), showBoundary=0.0, topMargin=20, bottomMargin=20,
                                leftMargin=20, rightMargin=20)
        doc.build(elements)
        f.close()   
