'''
Created on 19 feb 2018

@author: Serena Sensini
'''



class ARCHEOZOOLOGY(object):
	#def __init__"
	def __init__(self,
	id_,
	code,
	n_rilievo,
	n_codice,
	anno,
	sito,
	quadrato, 
	us,
	periodo,
	fase, 
	specie,
	classe,
	ordine,
	famiglia,
	elemnto_anat_generico,
	elem_specifici,
	taglia,
	eta,
	lato,
	lunghezza,
	larghezza,
	spessore,
	porzione,
	peso,
	coord_x,
	coord_y,
	coord_z,
	azione,
	modulo_osso
	):
		self.id_=id_
		self.code=code
		self.n_rilievo=n_rilievo
		self.n_codice=n_codice
		self.anno=anno
		self.sito=sito
		self.quadrato=quadrato 
		self.us=us
		self.periodo=periodo
		self.fase=fase
		self.specie=specie
		self.classe=classe
		self.ordine=ordine
		self.famiglia=famiglia
		self.elemnto_anat_generico=elemnto_anat_generico
		self.elem_specifici=elem_specifici
		self.taglia=taglia
		self.eta=eta
		self.lato=lato
		self.lunghezza=lunghezza
		self.larghezza=larghezza
		self.spessore=spessore
		self.porzione=porzione
		self.peso=peso
		self.coord_x=coord_x
		self.coord_y=coord_y
		self.coord_z=coord_z
		self.azione=azione
		self.modulo_osso=modulo_osso

	#def __repr__"
	def __repr__(self):
		return "<ARCHEOZOOLOGY('%d', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%r', '%r', '%r', '%r', '%s', '%s')>" % (
		self.id_,
		self.code,
		self.n_rilievo,
		self.n_codice,
		self.anno,
		self.sito,
		self.quadrato, 
		self.us,
		self.periodo,
		self.fase, 
		self.specie,
		self.classe,
		self.ordine,
		self.famiglia,
		self.elemnto_anat_generico,
		self.elem_specifici,
		self.taglia,
		self.eta,
		self.lato,
		self.lunghezza,
		self.larghezza,
		self.spessore,
		self.porzione,
		self.peso,
		self.coord_x,
		self.coord_y,
		self.coord_z,
		self.azione,
		self.modulo_osso
		)
