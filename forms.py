#!/usr/bin/env python
#
# YEP-DESK PROJECT
#

__author__ = 'Didier Dulac'

from wtforms import Form, BooleanField, DateField, FloatField, IntegerField, SelectField, TextField, TextAreaField, validators
from wtforms.ext.appengine.fields import ReferencePropertyField

from models import Application
from models import CategorieDemande
from models import CategorieIncident
from models import CommentaireDemande
from models import CommentaireIncident
from models import Contact
from models import Demande
from models import EtatDemande
from models import EtatIncident
from models import Fabricant
from models import FicheTest
from models import Fonction
from models import Groupe
from models import Imprimante
from models import Incident
from models import MesureApplication
from models import Modele
from models import Ordinateur
from models import Organisation
from models import Site
from models import Statut
from models import SystemeExploitation
from models import Tablette
from models import VersionApplication

class ApplicationForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  actif = BooleanField(u'Actif')
  description = TextAreaField(u'Description', validators=[validators.optional()])

class CategorieDemandeForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class CategorieIncidentForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class ContactForm(Form):
  organisation = ReferencePropertyField(u'Organisation', reference_class=Organisation)
  site = ReferencePropertyField(u'Site', reference_class=Site)
  fonction = ReferencePropertyField(u'Fonction', reference_class=Fonction)
  nom = TextField(u'Nom', validators=[validators.required()])
  prenom = TextField(u'Prenom', validators=[validators.required()])
  userid = TextField(u'Userid', validators=[validators.required()])
  email = TextField(u'Email', validators=[validators.Email()])
  telephone = TextField(u'Telephone')
  actif = BooleanField(u'Actif')

class EtatDemandeForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class EtatIncidentForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class FabricantForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class FicheTestForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  code = TextField(u'Code', validators=[validators.optional()])
  commentaire = TextAreaField(u'Commentaire', validators=[validators.optional()])

class FonctionForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class GroupeForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class ImprimanteForm(Form):
  organisation = ReferencePropertyField(u'Organisation', reference_class=Organisation)
  modele = ReferencePropertyField(u'Modele', reference_class=Modele)
  statut = ReferencePropertyField(u'Statut', reference_class=Statut)
  utilisateur = ReferencePropertyField(u'Utilisateur', reference_class=Contact)
  code = TextField(u'Code', validators=[validators.required()])
  no_serie = TextField(u'No serie', validators=[validators.required()])
  achat = DateField(u'Achat')
  garantie = IntegerField(u'Garantie')
  maintenu = BooleanField(u'Maintenu')

class DemandeForm(Form):
  etat = ReferencePropertyField(u'Etat', reference_class=EtatDemande)
  categorie = ReferencePropertyField(u'Categorie', reference_class=CategorieDemande)
  demandeur = ReferencePropertyField(u'Demandeur', reference_class=Contact)
  affecte = ReferencePropertyField(u'Affecte', reference_class=Groupe)
  reference = TextField(u'Reference', validators=[validators.required()])
  resume = TextField(u'Resume')
  description = TextAreaField(u'Description', validators=[validators.optional()])

class IncidentForm(Form):
  etat = ReferencePropertyField(u'Etat', reference_class=EtatIncident)
  categorie = ReferencePropertyField(u'Categorie', reference_class=CategorieIncident)
  utilisateur = ReferencePropertyField(u'Utilisateur', reference_class=Contact)
  affecte = ReferencePropertyField(u'Affecte', reference_class=Groupe)
  reference = TextField(u'Reference', validators=[validators.required()])
  resume = TextField(u'Resume')
  description = TextAreaField(u'Description', validators=[validators.optional()])

class MesureApplicationForm(Form):
  application = ReferencePropertyField(u'Application', reference_class=Application)
  quand = DateField(u'Date')
  dispo = FloatField(u'Disponibilite')
  perfo = FloatField(u'Performance')
  temps_moy = FloatField(u'Temps moy.')
  nb_transactions = IntegerField(u'Nombre trans.')
  nb_sessions = IntegerField(u'Nombre sessions')

class VersionApplicationForm(Form):
  application = ReferencePropertyField(u'Application', reference_class=Application)
  numero = TextField(u'Numero', validators=[validators.required()])
  commentaire = TextAreaField(u'Commentaire', validators=[validators.optional()])

class ModeleForm(Form):
  fabricant = ReferencePropertyField(u'Fabricant', reference_class=Fabricant)
  nom = TextField(u'Nom', validators=[validators.required()])
  type = SelectField(u'Type', choices=[('Ordinateur fixe', 'Ordinateur fixe'), ('Ordinateur portable', 'Ordinateur portable'), ('Tablette', 'Tablette'), ('Imprimante', 'Imprimante')])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class OrdinateurForm(Form):
  organisation = ReferencePropertyField(u'Organisation', reference_class=Organisation)
  modele = ReferencePropertyField(u'Modele', reference_class=Modele)
  statut = ReferencePropertyField(u'Statut', reference_class=Statut)
  utilisateur = ReferencePropertyField(u'Utilisateur', reference_class=Contact)
  systeme = ReferencePropertyField(u'O.S.', reference_class=SystemeExploitation)
  code = TextField(u'Code', validators=[validators.required()])
  no_serie = TextField(u'No serie', validators=[validators.required()])
  achat = DateField(u'Achat')
  garantie = IntegerField(u'Garantie')
  maintenu = BooleanField(u'Maintenu')

class OrganisationForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class SiteForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  adresse = TextField(u'Adresse', validators=[validators.required()])
  position = TextField(u'Position', validators=[validators.optional()])

class StatutForm(Form):
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class SystemeExploitationForm(Form):
  code = TextField(u'Code', validators=[validators.required()])
  nom = TextField(u'Nom', validators=[validators.required()])
  description = TextAreaField(u'Description', validators=[validators.optional()])

class TabletteForm(Form):
  organisation = ReferencePropertyField(u'Organisation', reference_class=Organisation)
  modele = ReferencePropertyField(u'Modele', reference_class=Modele)
  statut = ReferencePropertyField(u'Statut', reference_class=Statut)
  utilisateur = ReferencePropertyField(u'Utilisateur', reference_class=Contact)
  code = TextField(u'Code', validators=[validators.required()])
  no_serie = TextField(u'No serie', validators=[validators.required()])
  achat = DateField(u'Achat')
  garantie = IntegerField(u'Garantie')
  maintenu = BooleanField(u'Maintenu')
