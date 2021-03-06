#!/usr/bin/env python
#
# YEP-DESK PROJECT
#

__author__ = 'Didier Dulac'

import webapp2

from actions import BaseRequestHandler
from actions import CheckImportMateriel
from actions import ImportMateriel
from actions import AddMembre2Groupe
from actions import AddTransfert
from actions import AddApplication
from actions import AddCategorieDemande
from actions import AddCategorieIncident
from actions import AddCommentaireDemande
from actions import AddCommentaireIncident
from actions import AddContact
from actions import AddDefaut
from actions import AddDemande
from actions import AddEtatDemande
from actions import AddEtatIncident
from actions import AddFabricant
from actions import AddFicheTestApplication
from actions import AddFonction
from actions import AddGroupe
from actions import AddImprimante
from actions import AddIncident
from actions import AddMesureApplication
from actions import AddModele
from actions import AddOrdinateur
from actions import AddOrganisation
from actions import AddSite
from actions import AddStatut
from actions import AddSystemeExploitation
from actions import AddTest
from actions import AddVersionApplication
from actions import EditApplication
from actions import EditCategorieDemande
from actions import EditCategorieIncident
from actions import EditContact
from actions import EditDemande
from actions import EditEtatDemande
from actions import EditEtatIncident
from actions import EditFabricant
from actions import EditFicheTest
from actions import EditFonction
from actions import EditGroupe
from actions import EditImprimante
from actions import EditIncident
from actions import EditModele
from actions import EditOrdinateur
from actions import EditOrganisation
from actions import EditSite
from actions import EditStatut
from actions import EditSystemeExploitation
from actions import EditTest
from actions import EditVersionApplication
from actions import ListApplications
from actions import ListCategoriesDemande
from actions import ListCategoriesIncident
from actions import ListContacts
from actions import ListDefauts
from actions import ListDemandes
from actions import ListEtatsDemande
from actions import ListEtatsIncident
from actions import ListFabricants
from actions import ListFonctions
from actions import ListGroupes
from actions import ListImprimantes
from actions import ListIncidents
from actions import ListModeles
from actions import ListOrdinateurs
from actions import ListOrganisations
from actions import ListSites
from actions import ListStatuts
from actions import ListSystemeExploitations
from actions import ListTests
from actions import ChartsApplication
from actions import ViewApplication
from actions import ViewCategorieDemande
from actions import ViewCategorieIncident
from actions import ViewContact
from actions import ViewDefaut
from actions import ViewDemande
from actions import ViewEtatDemande
from actions import ViewEtatIncident
from actions import ViewFabricant
from actions import ViewFicheTest
from actions import ViewFonction
from actions import ViewGroupe
from actions import ViewImprimante
from actions import ViewIncident
from actions import ViewModele
from actions import ViewOrdinateur
from actions import ViewOrganisation
from actions import ViewSite
from actions import ViewStatut
from actions import ViewSystemeExploitation
from actions import ViewTest
from actions import ViewVersionApplication

class MainPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('index.html', template_values)

class AProposPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('apropos.html', template_values)

class AdminPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('admin.html', template_values)

class HelpdeskPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('helpdesk.html', template_values)

class CMDBPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('cmdb.html', template_values)

class ImportPage(BaseRequestHandler):
  def get(self):
    template_values = {
      }
    self.generate('import.html', template_values)

application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/apropos', AProposPage),
  ('/admin', AdminPage),
  ('/cmdb', CMDBPage),
  ('/helpdesk', HelpdeskPage),
  ('/import', ImportPage),
  ('/check_import', CheckImportMateriel),
  ('/import_materiel', ImportMateriel),
  ('/addMembre2Groupe', AddMembre2Groupe),
  ('/addTransfert', AddTransfert),
  ('/addMesure', AddMesureApplication),
  ('/addApplication', AddApplication),
  ('/editApplication', EditApplication),
  ('/application/([-\w]+)', ViewApplication),
  ('/application_charts/([-\w]+)', ChartsApplication),
  ('/applications', ListApplications),
  ('/addCategorieDemande', AddCategorieDemande),
  ('/editCategorieDemande', EditCategorieDemande),
  ('/categorieDemande/([-\w]+)', ViewCategorieDemande),
  ('/categoriesDemande', ListCategoriesDemande),
  ('/addCategorieIncident', AddCategorieIncident),
  ('/editCategorieIncident', EditCategorieIncident),
  ('/categorieIncident/([-\w]+)', ViewCategorieIncident),
  ('/categoriesIncident', ListCategoriesIncident),
  ('/addCommentaireDemande', AddCommentaireDemande),
  ('/addCommentaireIncident', AddCommentaireIncident),
  ('/addContact', AddContact),
  ('/editContact', EditContact),
  ('/contact/([-\w]+)', ViewContact),
  ('/contacts', ListContacts),
  ('/addDemande', AddDemande),
  ('/editDemande', EditDemande),
  ('/demande/([-\w]+)', ViewDemande),
  ('/demandes', ListDemandes),
  ('/addDefaut', AddDefaut),
  ('/defaut/([-\w]+)', ViewDefaut),
  ('/defauts', ListDefauts),
  ('/addEtatDemande', AddEtatDemande),
  ('/editEtatDemande', EditEtatDemande),
  ('/etatDemande/([-\w]+)', ViewEtatDemande),
  ('/etatsDemande', ListEtatsDemande),
  ('/addEtatIncident', AddEtatIncident),
  ('/addFicheTestApplication', AddFicheTestApplication),
  ('/editEtatIncident', EditEtatIncident),
  ('/etatIncident/([-\w]+)', ViewEtatIncident),
  ('/etatsIncident', ListEtatsIncident),
  ('/editFicheTest', EditFicheTest),
  ('/fiche/([-\w]+)', ViewFicheTest),
  ('/addFabricant', AddFabricant),
  ('/editFabricant', EditFabricant),
  ('/fabricant/([-\w]+)', ViewFabricant),
  ('/fabricants', ListFabricants),
  ('/addFonction', AddFonction),
  ('/editFonction', EditFonction),
  ('/fonction/([-\w]+)', ViewFonction),
  ('/fonctions', ListFonctions),
  ('/addGroupe', AddGroupe),
  ('/editGroupe', EditGroupe),
  ('/groupe/([-\w]+)', ViewGroupe),
  ('/groupes', ListGroupes),
  ('/addImprimante', AddImprimante),
  ('/editImprimante', EditImprimante),
  ('/imprimante/([-\w]+)', ViewImprimante),
  ('/imprimantes', ListImprimantes),
  ('/addIncident', AddIncident),
  ('/editIncident', EditIncident),
  ('/incident/([-\w]+)', ViewIncident),
  ('/incidents', ListIncidents),
  ('/addModele', AddModele),
  ('/editModele', EditModele),
  ('/modele/([-\w]+)', ViewModele),
  ('/modeles', ListModeles),
  ('/addOrdinateur', AddOrdinateur),
  ('/editOrdinateur', EditOrdinateur),
  ('/ordinateur/([-\w]+)', ViewOrdinateur),
  ('/ordinateurs', ListOrdinateurs),
  ('/addOrganisation', AddOrganisation),
  ('/editOrganisation', EditOrganisation),
  ('/organisation/([-\w]+)', ViewOrganisation),
  ('/organisations', ListOrganisations),
  ('/addSite', AddSite),
  ('/editSite', EditSite),
  ('/site/([-\w]+)', ViewSite),
  ('/sites', ListSites),
  ('/addStatut', AddStatut),
  ('/editStatut', EditStatut),
  ('/statut/([-\w]+)', ViewStatut),
  ('/statuts', ListStatuts),
  ('/addSysteme', AddSystemeExploitation),
  ('/editSysteme', EditSystemeExploitation),
  ('/systeme/([-\w]+)', ViewSystemeExploitation),
  ('/systemes', ListSystemeExploitations),
  ('/addTest', AddTest),
  ('/editTest', EditTest),
  ('/test/([-\w]+)', ViewTest),
  ('/tests', ListTests),
  ('/addVersionApplication', AddVersionApplication),
  ('/editVersionApplication', EditVersionApplication),
  ('/version/([-\w]+)', ViewVersionApplication)
], debug=True)
