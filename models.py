#!/usr/bin/env python
#
# YEP-DESK PROJECT
#

__author__ = 'Didier Dulac'

import datetime
import logging

from google.appengine.ext import db

class Objet(db.Model):
  created_by = db.UserProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  updated_by = db.UserProperty()
  updated = db.DateTimeProperty(auto_now=True)

class Site(Objet):
  nom = db.StringProperty()
  adresse = db.PostalAddressProperty()
  position = db.GeoPtProperty()
  def __str__(self):
    return self.nom

class Fonction(Objet):
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class Organisation(Objet):
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class Contact(Objet):
  organisation = db.ReferenceProperty(Organisation, collection_name='membres')
  site = db.ReferenceProperty(Site)
  fonction = db.ReferenceProperty(Fonction)
  nom = db.StringProperty()
  prenom = db.StringProperty()
  userid = db.StringProperty()
  email = db.EmailProperty()
  telephone = db.PhoneNumberProperty()
  actif = db.BooleanProperty(default=True)
  def __str__(self):
    return self.prenom+" "+self.nom

class Groupe(Objet):
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class Membre(Objet):
  personne = db.ReferenceProperty(Contact)
  groupe = db.ReferenceProperty(Groupe)

class Responsable(Objet):
  personne = db.ReferenceProperty(Contact)
  organisation = db.ReferenceProperty(Organisation)

class Statut(Objet):
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class EtatDemande(Objet):
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class EtatIncident(Objet):
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class CategorieDemande(Objet):
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class CategorieIncident(Objet):
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class SystemeExploitation(Objet):
  code = db.StringProperty()
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class Fabricant(Objet):
  nom = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class Modele(Objet):
  fabricant = db.ReferenceProperty(Fabricant, collection_name='modeles')
  nom = db.StringProperty()
  type = db.StringProperty(choices=set(["Ordinateur fixe", "Ordinateur portable", "Tablette", "Imprimante"]))
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class Materiel(Objet):
  no_serie = db.StringProperty()
  achat = db.DateProperty()
  garantie = db.IntegerProperty()
  maintenu = db.BooleanProperty(default=True)

class Imprimante(Materiel):
  organisation = db.ReferenceProperty(Organisation, collection_name='imprimantes')
  modele = db.ReferenceProperty(Modele)
  statut = db.ReferenceProperty(Statut)
  utilisateur = db.ReferenceProperty(Contact)
  code = db.StringProperty()
  def __str__(self):
    return self.code

class Tablette(Materiel):
  organisation = db.ReferenceProperty(Organisation, collection_name='tablettes')
  modele = db.ReferenceProperty(Modele)
  statut = db.ReferenceProperty(Statut)
  utilisateur = db.ReferenceProperty(Contact)
  code = db.StringProperty()
  def __str__(self):
    return self.code

class Ordinateur(Materiel):
  organisation = db.ReferenceProperty(Organisation, collection_name='ordinateurs')
  modele = db.ReferenceProperty(Modele)
  statut = db.ReferenceProperty(Statut)
  utilisateur = db.ReferenceProperty(Contact)
  systeme = db.ReferenceProperty(SystemeExploitation)
  code = db.StringProperty()
  def __str__(self):
    return self.code

class Demande(Objet):
  etat = db.ReferenceProperty(EtatDemande)
  categorie = db.ReferenceProperty(CategorieDemande)
  demandeur = db.ReferenceProperty(Contact)
  affecte = db.ReferenceProperty(Groupe)
  reference = db.StringProperty()
  resume = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.reference

class Incident(Objet):
  etat = db.ReferenceProperty(EtatIncident)
  categorie = db.ReferenceProperty(CategorieIncident)
  utilisateur = db.ReferenceProperty(Contact)
  affecte = db.ReferenceProperty(Groupe)
  reference = db.StringProperty()
  resume = db.StringProperty()
  description = db.TextProperty()
  def __str__(self):
    return self.reference

class Application(Objet):
  nom = db.StringProperty()
  actif = db.BooleanProperty(default=True)
  description = db.TextProperty()
  def __str__(self):
    return self.nom

class MesureApplication(db.Model):
  application = db.ReferenceProperty(Application)
  quand = db.DateProperty()
  dispo = db.FloatProperty()
  perfo = db.FloatProperty()
  temps_moy = db.FloatProperty()
  nb_transactions = db.IntegerProperty()
  nb_sessions = db.IntegerProperty()

class MesureHebdoAppli(db.Model):
  application = db.ReferenceProperty(Application)
  annee = db.IntegerProperty()
  semaine = db.IntegerProperty()
  dispo = db.FloatProperty()
  perfo = db.FloatProperty()
  temps_moy = db.FloatProperty()
  nb_transactions = db.IntegerProperty()
  nb_sessions = db.IntegerProperty()
  nb_appels = db.IntegerProperty()
  nb_g1 = db.IntegerProperty()
  nb_g2 = db.IntegerProperty()
  nb_g3 = db.IntegerProperty()
  nb_g4 = db.IntegerProperty()

class VersionApplication(db.Model):
  application = db.ReferenceProperty(Application, collection_name='versions')
  numero = db.StringProperty()
  commentaire = db.TextProperty()
