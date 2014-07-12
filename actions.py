#!/usr/bin/env python
#
# YEP-DESK PROJECT
#

__author__ = 'Didier Dulac'

import datetime
import logging
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from models import Application
from models import CategorieDemande
from models import CategorieIncident
from models import CommentaireDemande
from models import CommentaireIncident
from models import Contact
from models import Defaut
from models import Demande
from models import EtatDemande
from models import EtatIncident
from models import Fabricant
from models import FicheTest
from models import Fonction
from models import Groupe
from models import Imprimante
from models import Incident
from models import Membre
from models import MesureApplication
from models import Modele
from models import Ordinateur
from models import Organisation
from models import Responsable
from models import Site
from models import Statut
from models import SystemeExploitation
from models import Test
from models import VersionApplication

from forms import ApplicationForm
from forms import CategorieDemandeForm
from forms import CategorieIncidentForm
from forms import ContactForm
from forms import DemandeForm
from forms import EtatDemandeForm
from forms import EtatIncidentForm
from forms import FabricantForm
from forms import FicheTestForm
from forms import FonctionForm
from forms import GroupeForm
from forms import ImprimanteForm
from forms import IncidentForm
from forms import MesureApplicationForm
from forms import ModeleForm
from forms import OrdinateurForm
from forms import OrganisationForm
from forms import SiteForm
from forms import StatutForm
from forms import SystemeExploitationForm
from forms import VersionApplicationForm

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class BaseRequestHandler(webapp2.RequestHandler):
  def generate(self, template_name, template_values={}):
    values = {
      'request': self.request,
      'user': users.GetCurrentUser(),
      'admin': users.IsCurrentUserAdmin(),
      'login_url': users.CreateLoginURL(self.request.uri),
      'logout_url': users.CreateLogoutURL('http://' + self.request.host + '/'),
      'debug': self.request.get('deb'),
      'application_name': 'YeP-DesK'
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

class CheckImportMateriel(BaseRequestHandler):
  def post(self):
    logging.debug('Start materiel import checking request')

    materiels = []

    data = self.request.get('donnees')
    ligne = data.splitlines()

    for index in range(len(ligne)) :
      tab = ligne[index].split(';')
      logging.debug('Reading %s', tab)
      if len(tab) > 2 :
        c = tab[0]
        n = tab[1]
        m = None
        materiel = None
        try:
          m = Modele.gql("WHERE nom LIKE '"+tab[2]+"'")
          if m:
            logging.debug('Modele %s found', modele.nom)
            if m.type == 'Imprimante':
              materiel = Imprimante(code=c, no_serie=n, modele=m)
            else:
              materiel = Ordinateur(code=c, no_serie=n, modele=m)
            materiels.append(materiel)
        except:
          logging.error('Cannot find modele %s', tab[2])

    logging.debug('Finish materiel import checking')

    template_values = {
      'title': "Verification d'import",
      'materiels': materiels
      }

    self.generate('check.html', template_values)

class ImportMateriel(BaseRequestHandler):
  def post(self):
    logging.debug('Start materiel importing request')

    res = []

    logging.debug('Finish materiel importing')

    template_values = {
      'title': "Resultat d'import",
      'res': res
      }

    self.generate('result.html', template_values)

class AddMembre2Groupe(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start groupe membre adding request')
    g = self.request.get('groupe')
    c = self.request.get('contact')

    m = Membre()

    user = users.GetCurrentUser()
    if user:
      logging.info('membre added by user %s' % user.nickname())
      m.created_by = user
      m.updated_by = user
    else:
      logging.info('membre added by anonymous user')

    try:
      i = int(g)
      groupe = Groupe.get(db.Key.from_path('Groupe', i))
      m.groupe = groupe
    except:
      logging.error('There was an error retreiving groupe %s' % g)

    try:
      i = int(c)
      contact = Contact.get(db.Key.from_path('Contact', i))
      m.contact = contact
    except:
      logging.error('There was an error retreiving contact %s' % c)

    try:
      m.put()
    except:
      logging.error('There was an error adding membre')

    logging.debug('Finish groupe membre adding')
    self.redirect('/groupe/%s' % g)

class AddCommentaireDemande(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start demande commentaire adding request')

    id = self.request.get('id')
    texte = self.request.get('texte')

    c = CommentaireDemande(texte=texte)

    user = users.GetCurrentUser()
    if user:
      logging.info('commentaire added by user %s' % user.nickname())
      c.created_by = user
      c.updated_by = user
    else:
      logging.info('commentaire added by anonymous user')

    try:
      i = int(id)
      demande = Demande.get(db.Key.from_path('Demande', i))
      c.demande = demande
    except:
      logging.error('There was an error retreiving demande %s' % id)

    try:
      c.put()
    except:
      logging.error('There was an error adding commentaire demande')

    logging.debug('Finish demande commentaire adding')
    self.redirect('/demande/%s#item0' % id)

class AddCommentaireIncident(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start incident commentaire adding request')

    id = self.request.get('id')
    texte = self.request.get('texte')

    c = CommentaireIncident(texte=texte)

    user = users.GetCurrentUser()
    if user:
      logging.info('commentaire added by user %s' % user.nickname())
      c.created_by = user
      c.updated_by = user
    else:
      logging.info('commentaire added by anonymous user')

    try:
      i = int(id)
      incident = Incident.get(db.Key.from_path('Incident', i))
      c.incident = incident
    except:
      logging.error('There was an error retreiving incident %s' % id)

    try:
      c.put()
    except:
      logging.error('There was an error adding commentaire incident')

    logging.debug('Finish incident commentaire adding')
    self.redirect('/incident/%s#item0' % id)

class AddApplication(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start application adding request')

    n = self.request.get('nom')
    appli = Application(nom=n,commentaire='')

    user = users.GetCurrentUser()
    if user:
      logging.info('Application %s added by user %s' % (n, user.nickname()))
      appli.created_by = user
      appli.updated_by = user
    else:
      logging.info('Application %s added by anonymous user' % n)

    try:
      appli.put()
    except:
      logging.error('There was an error adding application %s' % n)

    logging.debug('Finish application adding')
    self.redirect('/applications')

class AddVersionApplication(BaseRequestHandler):
  def post(self):
    logging.debug('Start version application adding request')
    a = self.request.get('id')
    n = self.request.get('numero')
    obj = VersionApplication(numero=n,commentaire='...')
    user = users.GetCurrentUser()
    if user:
      logging.info('Version application %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Version application %s added by anonymous user' % n)

    try:
      i = int(a)
      application = Application.get(db.Key.from_path('Application', i))
      obj.application = application
    except:
      logging.error('There was an error retreiving application %s' % a)

    try:
      obj.put()
    except:
      logging.error('There was an error adding version application %s' % n)
    logging.debug('Finish version application adding')
    self.redirect('/application/%s#versions' % a)

class AddFicheTestApplication(BaseRequestHandler):
  def post(self):
    logging.debug('Start fiche test application adding request')
    a = self.request.get('id')
    n = self.request.get('nom')
    c = self.request.get('commentaire')
    obj = FicheTest(nom=n,code='',commentaire=c)
    user = users.GetCurrentUser()
    if user:
      logging.info('Fiche test application %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Fiche test application %s added by anonymous user' % n)

    try:
      i = int(a)
      application = Application.get(db.Key.from_path('Application', i))
      obj.application = application
    except:
      logging.error('There was an error retreiving application %s' % a)

    try:
      obj.put()
    except:
      logging.error('There was an error adding fiche test application %s' % n)
    logging.debug('Finish fiche test application adding')
    self.redirect('/application/%s#fiches' % a)

class AddCategorieDemande(BaseRequestHandler):
  def post(self):
    logging.debug('Start categorie demande adding request')
    n = self.request.get('nom')
    obj = CategorieDemande(nom=n,description='...')
    user = users.GetCurrentUser()
    if user:
      logging.info('Categorie Demande %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Categorie Demande %s added by anonymous user' % n)
    try:
      obj.put()
    except:
      logging.error('There was an error adding categorie demande %s' % n)
    logging.debug('Finish categorie demande adding')
    self.redirect('/categoriesDemande')

class AddCategorieIncident(BaseRequestHandler):
  def post(self):
    logging.debug('Start categorie incident adding request')
    n = self.request.get('nom')
    obj = CategorieIncident(nom=n,description='...')
    user = users.GetCurrentUser()
    if user:
      logging.info('Categorie Incident %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Categorie Incident %s added by anonymous user' % n)
    try:
      obj.put()
    except:
      logging.error('There was an error adding categorie incident %s' % n)
    logging.debug('Finish categorie incident adding')
    self.redirect('/categoriesIncident')

class AddContact(BaseRequestHandler):
  def post(self):
    logging.debug('Start contact adding request')
    n = self.request.get('nom')
    p = self.request.get('prenom')
    obj = Contact(prenom=p,nom=n)
    user = users.GetCurrentUser()
    if user:
      logging.info('Contact %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Application %s added by anonymous user' % n)
    try:
      obj.put()
    except:
      logging.error('There was an error adding contact %s' % n)
    logging.debug('Finish contact adding')
    self.redirect('/contacts')

class AddEtatDemande(BaseRequestHandler):
  def post(self):
    logging.debug('Start etat demande adding request')
    n = self.request.get('nom')
    obj = EtatDemande(nom=n,description='...')
    user = users.GetCurrentUser()
    if user:
      logging.info('Etat Demande %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Etat Demande %s added by anonymous user' % n)
    try:
      obj.put()
    except:
      logging.error('There was an error adding etat demande %s' % n)
    logging.debug('Finish etat demande adding')
    self.redirect('/etatsDemande')

class AddEtatIncident(BaseRequestHandler):
  def post(self):
    logging.debug('Start etat incident adding request')
    n = self.request.get('nom')
    obj = EtatIncident(nom=n,description='...')
    user = users.GetCurrentUser()
    if user:
      logging.info('Etat Incident %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Etat Incident %s added by anonymous user' % n)
    try:
      obj.put()
    except:
      logging.error('There was an error adding etat incident %s' % n)
    logging.debug('Finish etat incident adding')
    self.redirect('/etatsIncident')

class AddFabricant(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start fabricant adding request')

    n = self.request.get('nom')
    fab = Fabricant(nom=n,commentaire='')

    user = users.GetCurrentUser()
    if user:
      logging.info('Fabricant %s added by user %s' % (n, user.nickname()))
      fab.created_by = user
      fab.updated_by = user
    else:
      logging.info('Fabricant %s added by anonymous user' % n)

    try:
      fab.put()
    except:
      logging.error('There was an error adding fabricant %s' % n)

    logging.debug('Finish fabricant adding')
    self.redirect('/fabricants')

class AddFonction(BaseRequestHandler):
  def post(self):
    logging.debug('Start fonction adding request')
    n = self.request.get('nom')
    obj = Fonction(nom=n)
    user = users.GetCurrentUser()
    if user:
      logging.info('Fonction %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Fonction %s added by anonymous user' % n)
    try:
      obj.put()
    except:
      logging.error('There was an error adding fonction %s' % n)
    logging.debug('Finish fonction adding')
    self.redirect('/fonctions')

class AddGroupe(BaseRequestHandler):
  def post(self):
    logging.debug('Start groupe adding request')
    n = self.request.get('nom')
    obj = Groupe(nom=n,commentaire='')
    user = users.GetCurrentUser()
    if user:
      logging.info('Groupe %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Application %s added by anonymous user' % n)
    try:
      obj.put()
    except:
      logging.error('There was an error adding groupe %s' % n)
    logging.debug('Finish groupe adding')
    self.redirect('/groupes')

class AddImprimante(BaseRequestHandler):
  def post(self):
    logging.debug('Start imprimante adding request')
    c = self.request.get('code')
    m = self.request.get('modele')
    s = self.request.get('statut')
    obj = Imprimante(code=c)
    user = users.GetCurrentUser()
    if user:
      logging.info('Imprimante %s added by user %s' % (c, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Imprimante %s added by anonymous user' % c)

    try:
      i = int(m)
      modele = Modele.get(db.Key.from_path('Modele', i))
      obj.modele = modele
    except:
      logging.error('There was an error retreiving modele %s' % m)

    try:
      i = int(s)
      statut = Statut.get(db.Key.from_path('Statut', i))
      obj.statut = statut
    except:
      logging.error('There was an error retreiving statut %s' % s)

    try:
      obj.put()
    except:
      logging.error('There was an error adding imprimante %s' % c)
    logging.debug('Finish imprimante adding')
    self.redirect('/imprimantes')

class AddDemande(BaseRequestHandler):
  def post(self):
    logging.debug('Start demande adding request')
    r = self.request.get('reference')
    obj = Demande(reference=r,description='')
    user = users.GetCurrentUser()
    if user:
      logging.info('Demande %s added by user %s' % (r, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Demande %s added by anonymous user' % r)
    try:
      obj.put()
    except:
      logging.error('There was an error adding demande %s' % r)
    logging.debug('Finish demande adding')
    self.redirect('/demandes')

class AddIncident(BaseRequestHandler):
  def post(self):
    logging.debug('Start incident adding request')
    r = self.request.get('reference')
    obj = Incident(reference=r,description='')
    user = users.GetCurrentUser()
    if user:
      logging.info('Incident %s added by user %s' % (r, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Incident %s added by anonymous user' % r)
    try:
      obj.put()
    except:
      logging.error('There was an error adding incident %s' % r)
    logging.debug('Finish incident adding')
    self.redirect('/incidents')

class AddMesureApplication(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start mesure adding request')

    app = None
    id = self.request.get('id')
    m = self.request.get('mesure')

    try:
      i = int(id)
      app = Application.get(db.Key.from_path('Application', i))
      if app:
        tab = m.split(',')

        logging.debug('Reading %s,%s,%s for %s' % (tab[0], tab[1], tab[2], app.nom))

        q=datetime.datetime.strptime(tab[0], "%Y-%m-%d")
        d=float(tab[1])
        p=float(tab[2])
        t=float(tab[3])
        x=int(tab[4])
        s=int(tab[5])

        mes = MesureApplication(perfo=p, dispo=d, temps_moy=t, nb_sessions=s, nb_transactions=x)
        mes.quand=q.date() 
        mes.application = app
        mes.put()
    except:
      logging.error('There was an error adding mesure %s' % m)

    logging.debug('Finish mesure adding')
    self.redirect('/application/%s#bottom' % id)

class AddModele(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start modele adding request')

    n = self.request.get('nom')
    t = self.request.get('type')
    id = self.request.get('fabricant')
    mod = Modele(nom=n,type=t,commentaire='')

    user = users.GetCurrentUser()
    if user:
      logging.info('Modele %s added by user %s' % (n, user.nickname()))
      mod.created_by = user
      mod.updated_by = user
    else:
      logging.info('Modele %s added by anonymous user' % n)

    try:
      i = int(id)
      fab = Fabricant.get(db.Key.from_path('Fabricant', i))
      mod.fabricant = fab
    except:
      logging.error('There was an error retreiving fabricant %s' % id)

    try:
      mod.put()
    except:
      logging.error('There was an error adding modele %s' % n)

    logging.debug('Finish modele adding')
    self.redirect('/modeles')

class AddOrdinateur(BaseRequestHandler):
  def post(self):
    logging.debug('Start ordinateur adding request')
    c = self.request.get('code')
    m = self.request.get('modele')
    s = self.request.get('statut')
    obj = Ordinateur(code=c)
    user = users.GetCurrentUser()
    if user:
      logging.info('Ordinateur %s added by user %s' % (c, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Ordinateur %s added by anonymous user' % c)

    try:
      i = int(m)
      modele = Modele.get(db.Key.from_path('Modele', i))
      obj.modele = modele
    except:
      logging.error('There was an error retreiving modele %s' % m)

    try:
      i = int(s)
      statut = Statut.get(db.Key.from_path('Statut', i))
      obj.statut = statut
    except:
      logging.error('There was an error retreiving statut %s' % s)

    try:
      obj.put()
    except:
      logging.error('There was an error adding ordinateur %s' % c)
    logging.debug('Finish ordinateur adding')
    self.redirect('/ordinateurs')

class AddOrganisation(BaseRequestHandler):
  def post(self):
    logging.debug('Start organisation adding request')
    n = self.request.get('nom')
    obj = Organisation(nom=n,commentaire='')
    user = users.GetCurrentUser()
    if user:
      logging.info('Organisation %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('Organisation %s added by anonymous user' % n)
    try:
      obj.put()
    except:
      logging.error('There was an error adding organisation %s' % n)
    logging.debug('Finish organisation adding')
    self.redirect('/organisations')

class AddStatut(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start statut adding request')

    n = self.request.get('nom')
    s = Statut(nom=n,commentaire='')

    user = users.GetCurrentUser()
    if user:
      logging.info('Statut %s added by user %s' % (n, user.nickname()))
      s.created_by = user
      s.updated_by = user
    else:
      logging.info('Statut %s added by anonymous user' % n)

    try:
      s.put()
    except:
      logging.error('There was an error adding statut %s' % n)

    logging.debug('Finish statut adding')
    self.redirect('/statuts')

class AddSite(webapp2.RequestHandler):
  def post(self):
    logging.debug('Start site adding request')

    n = self.request.get('nom')
    s = Site(nom=n,adresse='quelque part')

    user = users.GetCurrentUser()
    if user:
      logging.info('Site %s added by user %s' % (n, user.nickname()))
      s.created_by = user
      s.updated_by = user
    else:
      logging.info('Site %s added by anonymous user' % n)

    try:
      s.put()
    except:
      logging.error('There was an error adding site %s' % n)

    logging.debug('Finish site adding')
    self.redirect('/sites')

class AddSystemeExploitation(BaseRequestHandler):
  def post(self):
    logging.debug('Start systeme adding request')
    n = self.request.get('nom')
    obj = SystemeExploitation(nom=n,commentaire='')
    user = users.GetCurrentUser()
    if user:
      logging.info('SystemeExploitation %s added by user %s' % (n, user.nickname()))
      obj.created_by = user
      obj.updated_by = user
    else:
      logging.info('SystemeExploitation %s added by anonymous user' % n)
    try:
      obj.put()
    except:
      logging.error('There was an error adding systeme %s' % n)
    logging.debug('Finish systeme adding')
    self.redirect('/systemes')

class ListApplications(BaseRequestHandler):
  def get(self):
    applications = []
    title = 'Applications'
    try:
      applications = Application.gql("ORDER BY nom")
      title = 'Applications'
    except:
      logging.error('There was an error retreiving applications from the datastore')

    template_values = {
      'title': title,
      'applications': applications,
      }

    self.generate('applications.html', template_values)

class ListCategoriesDemande(BaseRequestHandler):
  def get(self):
    categories = []
    title = 'Categories demande'
    try:
      categories = CategorieDemande.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving categories demande from the datastore')
    template_values = {
      'title': title,
      'categories': categories
    }
    self.generate('categoriesDemande.html', template_values)

class ListCategoriesIncident(BaseRequestHandler):
  def get(self):
    categories = []
    title = 'Categories incident'
    try:
      categories = CategorieIncident.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving categories incident from the datastore')
    template_values = {
      'title': title,
      'categories': categories
    }
    self.generate('categoriesIncident.html', template_values)

class ListContacts(BaseRequestHandler):
  def get(self):
    contacts = []
    title = 'Contacts'
    try:
      contacts = Contact.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving contacts from the datastore')
    template_values = {
      'title': title,
      'contacts': contacts,
    }
    self.generate('contacts.html', template_values)

class ListEtatsDemande(BaseRequestHandler):
  def get(self):
    etats = []
    title = 'Etats demande'
    try:
      etats = EtatDemande.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving etats demande from the datastore')
    template_values = {
      'title': title,
      'etats': etats
    }
    self.generate('etatsDemande.html', template_values)

class ListEtatsIncident(BaseRequestHandler):
  def get(self):
    etats = []
    title = 'Etats incident'
    try:
      etats = EtatIncident.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving etats incident from the datastore')
    template_values = {
      'title': title,
      'etats': etats
    }
    self.generate('etatsIncident.html', template_values)

class ListFabricants(BaseRequestHandler):
  def get(self):
    fabricants = []
    title = 'Fabricants'
    try:
      fabricants = Fabricant.gql("ORDER BY nom")
      title = 'Fabricants'
    except:
      logging.error('There was an error retreiving fabricants from the datastore')

    template_values = {
      'title': title,
      'fabricants': fabricants,
      }

    self.generate('fabricants.html', template_values)

class ListFonctions(BaseRequestHandler):
  def get(self):
    fonctions = []
    title = 'Fonctions'
    try:
      fonctions = Fonction.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving fonctions from the datastore')
    template_values = {
      'title': title,
      'fonctions': fonctions
    }
    self.generate('fonctions.html', template_values)

class ListGroupes(BaseRequestHandler):
  def get(self):
    groupes = []
    title = 'Groupes'
    try:
      groupes = Groupe.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving groupes from the datastore')
    template_values = {
      'title': title,
      'groupes': groupes,
    }
    self.generate('groupes.html', template_values)

class ListImprimantes(BaseRequestHandler):
  def get(self):
    imprimantes = []
    modeles = []
    statuts = []
    title = 'Imprimantes'
    try:
      imprimantes = Imprimante.gql("ORDER BY code")
      modeles = Modele.gql("WHERE type IN ('Imprimante') ORDER BY nom")
      statuts = Statut.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving imprimantes from the datastore')
    template_values = {
      'title': title,
      'imprimantes': imprimantes,
      'modeles': modeles,
      'statuts': statuts
    }
    self.generate('imprimantes.html', template_values)

class ListDemandes(BaseRequestHandler):
  def get(self):
    demandes = []
    title = 'Demandes'
    try:
      demandes = Demande.gql("ORDER BY reference")
    except:
      logging.error('There was an error retreiving demandes from the datastore')
    template_values = {
      'title': title,
      'demandes': demandes
    }
    self.generate('demandes.html', template_values)

class ListIncidents(BaseRequestHandler):
  def get(self):
    incidents = []
    title = 'Incidents'
    try:
      incidents = Incident.gql("ORDER BY reference")
    except:
      logging.error('There was an error retreiving incidents from the datastore')
    template_values = {
      'title': title,
      'incidents': incidents
    }
    self.generate('incidents.html', template_values)

class ListModeles(BaseRequestHandler):
  def get(self):
    fabricants = []
    modeles = []
    title = 'Modeles'
    try:
      fabricants = Fabricant.gql("ORDER BY nom")
      modeles = Modele.gql("ORDER BY nom")
      title = 'Modeles'
    except:
      logging.error('There was an error retreiving fabricants and modeles from the datastore')

    template_values = {
      'title': title,
      'fabricants': fabricants,
      'modeles': modeles,
      }

    self.generate('modeles.html', template_values)

class ListOrdinateurs(BaseRequestHandler):
  def get(self):
    ordinateurs = []
    modeles = []
    statuts = []
    title = 'Ordinateurs'
    try:
      ordinateurs = Ordinateur.gql("ORDER BY code")
      modeles = Modele.gql("WHERE type IN ('Ordinateur fixe', 'Ordinateur portable') ORDER BY nom")
      statuts = Statut.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving ordinateurs from the datastore')
    template_values = {
      'title': title,
      'ordinateurs': ordinateurs,
      'modeles': modeles,
      'statuts': statuts
    }
    self.generate('ordinateurs.html', template_values)

class ListOrganisations(BaseRequestHandler):
  def get(self):
    organisations = []
    title = 'Organisations'
    try:
      organisations = Organisation.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving organisations from the datastore')
    template_values = {
      'title': title,
      'organisations': organisations
    }
    self.generate('organisations.html', template_values)

class ListSites(BaseRequestHandler):
  def get(self):
    sites = []
    title = 'Sites'
    try:
      sites = Site.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving sites from the datastore')

    template_values = {
      'title': title,
      'sites': sites,
      }

    self.generate('sites.html', template_values)

class ListStatuts(BaseRequestHandler):
  def get(self):
    statuts = []
    title = 'Statuts'
    try:
      statuts = Statut.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving statuts from the datastore')

    template_values = {
      'title': title,
      'statuts': statuts,
      }

    self.generate('statuts.html', template_values)

class ListSystemeExploitations(BaseRequestHandler):
  def get(self):
    systemes = []
    title = 'Systemes exploitation'
    try:
      systemes = SystemeExploitation.gql("ORDER BY nom")
    except:
      logging.error('There was an error retreiving systemes from the datastore')
    template_values = {
      'title': title,
      'systemes': systemes
    }
    self.generate('systemes.html', template_values)

class ViewApplication(BaseRequestHandler):
  def get(self, arg):
    title = 'Application introuvable'
    application = None
    mesures = []
    # Get and displays the application informations
    try:
      id = int(arg)
      application = Application.get(db.Key.from_path('Application', id))
      if application:
        mesures = MesureApplication.gql("WHERE application = :1 ORDER BY quand DESC LIMIT 10", application)
    except:
      application = None
      logging.error('There was an error retreiving application and its informations from the datastore')

    if not application:
      self.error(403)
      return
    else:
      title = application.nom

    template_values = {
      'title': title,
      'application': application,
      'mesures': mesures
      }

    self.generate('application.html', template_values)

class ViewVersionApplication(BaseRequestHandler):
  def get(self, arg):
    title = 'Version introuvable'
    version = None
    # Get and displays the version application informations
    try:
      id = int(arg)
      version = VersionApplication.get(db.Key.from_path('VersionApplication', id))
    except:
      version = None
      logging.error('There was an error retreiving version application and its informations from the datastore')

    if not version:
      self.error(403)
      return
    else:
      title = version.numero

    template_values = {
      'title': title,
      'version': version
      }

    self.generate('version.html', template_values)

class ChartsApplication(BaseRequestHandler):
  def get(self, arg):
    title = 'Application introuvable'
    application = None
    mesures = []
    # Get and displays the application informations
    try:
      id = int(arg)
      application = Application.get(db.Key.from_path('Application', id))
      if application:
        mesures = MesureApplication.gql("WHERE application = :1 ORDER BY quand", application)
    except:
      application = None
      logging.error('There was an error retreiving application and its informations from the datastore')

    if not application:
      self.error(403)
      return
    else:
      title = application.nom

    template_values = {
      'title': title,
      'application': application,
      'mesures': mesures
      }

    self.generate('application_charts.html', template_values)

class ViewCategorieDemande(BaseRequestHandler):
  def get(self, arg):
    title = 'Categorie demande introuvable'
    categorie = None
    # Get and displays the categorie informations
    try:
      id = int(arg)
      categorie = CategorieDemande.get(db.Key.from_path('CategorieDemande', id))
    except:
      categorie = None
      logging.error('There was an error retreiving categorie demande and its informations from the datastore')
    if not categorie:
      self.error(403)
      return
    else:
      title = categorie.nom
    template_values = {
      'title': title,
      'categorie': categorie
    }
    self.generate('categorieDemande.html', template_values)

class ViewCategorieIncident(BaseRequestHandler):
  def get(self, arg):
    title = 'Categorie incident introuvable'
    categorie = None
    # Get and displays the categorie informations
    try:
      id = int(arg)
      categorie = CategorieIncident.get(db.Key.from_path('CategorieIncident', id))
    except:
      categorie = None
      logging.error('There was an error retreiving categorie incident and its informations from the datastore')
    if not categorie:
      self.error(403)
      return
    else:
      title = categorie.nom
    template_values = {
      'title': title,
      'categorie': categorie
    }
    self.generate('categorieIncident.html', template_values)

class ViewContact(BaseRequestHandler):
  def get(self, arg):
    title = 'Contact introuvable'
    contact = None
    groupes = []
    demandes = []
    incidents = []
    ordinateurs = []
    imprimantes = []
    # Get and displays the contact informations
    try:
      id = int(arg)
      contact = Contact.get(db.Key.from_path('Contact', id))
      if contact:
        groupes = Membre.gql("WHERE contact = :1", contact)
        demandes = Demande.gql("WHERE demandeur = :1 ORDER BY reference", contact)
        incidents = Incident.gql("WHERE utilisateur = :1 ORDER BY reference", contact)
        ordinateurs = Ordinateur.gql("WHERE utilisateur = :1 ORDER BY code", contact)
        imprimantes = Imprimante.gql("WHERE utilisateur = :1 ORDER BY code", contact)
    except:
      contact = None
      groupes = []
      demandes = []
      incidents = []
      ordinateurs = []
      imprimantes = []
      logging.error('There was an error retreiving contact and its informations from the datastore')
    if not contact:
      self.error(403)
      return
    else:
      title = contact.nom
    template_values = {
      'title': title,
      'contact': contact,
      'groupes': groupes,
      'demandes': demandes,
      'incidents': incidents,
      'ordinateurs': ordinateurs,
      'imprimantes': imprimantes,
    }
    self.generate('contact.html', template_values)

class ViewEtatDemande(BaseRequestHandler):
  def get(self, arg):
    title = 'Etat demande introuvable'
    etat = None
    # Get and displays the etat informations
    try:
      id = int(arg)
      etat = EtatDemande.get(db.Key.from_path('EtatDemande', id))
    except:
      etat = None
      logging.error('There was an error retreiving etat demande and its informations from the datastore')
    if not etat:
      self.error(403)
      return
    else:
      title = etat.nom
    template_values = {
      'title': title,
      'etat': etat
    }
    self.generate('etatDemande.html', template_values)

class ViewEtatIncident(BaseRequestHandler):
  def get(self, arg):
    title = 'Etat incident introuvable'
    etat = None
    # Get and displays the etat informations
    try:
      id = int(arg)
      etat = EtatIncident.get(db.Key.from_path('EtatIncident', id))
    except:
      etat = None
      logging.error('There was an error retreiving etat incident and its informations from the datastore')
    if not etat:
      self.error(403)
      return
    else:
      title = etat.nom
    template_values = {
      'title': title,
      'etat': etat
    }
    self.generate('etatIncident.html', template_values)

class ViewFabricant(BaseRequestHandler):
  def get(self, arg):
    title = 'Fabricant introuvable'
    fabricant = None
    modeles = []
    # Get and displays the fabricant informations
    try:
      id = int(arg)
      fabricant = Fabricant.get(db.Key.from_path('Fabricant', id))
      if fabricant:
        modeles = Modele.gql("WHERE fabricant = :1 ORDER BY nom", fabricant)
    except:
      fabricant = None
      logging.error('There was an error retreiving fabricant and its informations from the datastore')

    if not fabricant:
      self.error(403)
      return
    else:
      title = fabricant.nom

    template_values = {
      'title': title,
      'fabricant': fabricant,
      'modeles': modeles
      }

    self.generate('fabricant.html', template_values)

class ViewFicheTest(BaseRequestHandler):
  def get(self, arg):
    title = 'Fiche de test introuvable'
    fiche = None
    # Get and displays the fiche informations
    try:
      id = int(arg)
      fiche = FicheTest.get(db.Key.from_path('FicheTest', id))
    except:
      fiche = None
      logging.error('There was an error retreiving fiche and its informations from the datastore')

    if not fiche:
      self.error(403)
      return
    else:
      title = fiche.nom

    template_values = {
      'title': title,
      'fiche': fiche
      }

    self.generate('fiche.html', template_values)

class ViewFonction(BaseRequestHandler):
  def get(self, arg):
    title = 'Fonction introuvable'
    fonction = None
    # Get and displays the fonction informations
    try:
      id = int(arg)
      fonction = Fonction.get(db.Key.from_path('Fonction', id))
    except:
      fonction = None
      logging.error('There was an error retreiving fonction and its informations from the datastore')
    if not fonction:
      self.error(403)
      return
    else:
      title = fonction.nom
    template_values = {
      'title': title,
      'fonction': fonction
    }
    self.generate('fonction.html', template_values)

class ViewGroupe(BaseRequestHandler):
  def get(self, arg):
    title = 'Groupe introuvable'
    groupe = None
    contacts = []
    membres = []
    incidents = []
    demandes = []
    # Get and displays the groupe informations
    try:
      id = int(arg)
      groupe = Groupe.get(db.Key.from_path('Groupe', id))
      contacts = Contact.gql("ORDER BY nom")
      membres = Membre.gql("WHERE groupe = :1", groupe)
      if groupe:
        incidents = Incident.gql("WHERE affecte = :1 ORDER BY reference", groupe)
        demandes = Demande.gql("WHERE affecte = :1 ORDER BY reference", groupe)
    except:
      groupe = None
      contacts = []
      membres = []
      incidents = []
      demandes = []
      logging.error('There was an error retreiving groupe and its informations from the datastore')
    if not groupe:
      self.error(403)
      return
    else:
      title = groupe.nom
    template_values = {
      'title': title,
      'groupe': groupe,
      'contacts': contacts,
      'membres': membres,
      'incidents': incidents,
      'demandes': demandes,
    }
    self.generate('groupe.html', template_values)

class ViewImprimante(BaseRequestHandler):
  def get(self, arg):
    title = 'Imprimante introuvable'
    imprimante = None
    # Get and displays the imprimante informations
    try:
      id = int(arg)
      imprimante = Imprimante.get(db.Key.from_path('Imprimante', id))
    except:
      imprimante = None
      logging.error('There was an error retreiving imprimante and its informations from the datastore')
    if not imprimante:
      self.error(403)
      return
    else:
      title = imprimante.code
    template_values = {
      'title': title,
      'imprimante': imprimante
    }
    self.generate('imprimante.html', template_values)

class ViewDemande(BaseRequestHandler):
  def get(self, arg):
    title = 'Demande introuvable'
    demande = None
    # Get and displays the demande informations
    try:
      id = int(arg)
      demande = Demande.get(db.Key.from_path('Demande', id))
    except:
      demande = None
      logging.error('There was an error retreiving demande and its informations from the datastore')
    if not demande:
      self.error(403)
      return
    else:
      title = demande.reference
    template_values = {
      'title': title,
      'demande': demande
    }
    self.generate('demande.html', template_values)

class ViewIncident(BaseRequestHandler):
  def get(self, arg):
    title = 'Incident introuvable'
    incident = None
    # Get and displays the incident informations
    try:
      id = int(arg)
      incident = Incident.get(db.Key.from_path('Incident', id))
    except:
      incident = None
      logging.error('There was an error retreiving incident and its informations from the datastore')
    if not incident:
      self.error(403)
      return
    else:
      title = incident.reference
    template_values = {
      'title': title,
      'incident': incident
    }
    self.generate('incident.html', template_values)

class ViewModele(BaseRequestHandler):
  def get(self, arg):
    title = 'Modele introuvable'
    modele = None
    ordinateurs = []
    imprimantes = []
    # Get and displays the modele informations
    try:
      id = int(arg)
      modele = Modele.get(db.Key.from_path('Modele', id))
      if modele:
        ordinateurs = Ordinateur.gql("WHERE modele = :1 ORDER BY code", modele)
        imprimantes = Imprimante.gql("WHERE modele = :1 ORDER BY code", modele)
    except:
      modele = None
      ordinateurs = []
      imprimantes = []
      logging.error('There was an error retreiving modele and its informations from the datastore')

    if not modele:
      self.error(403)
      return
    else:
      title = modele.nom

    template_values = {
      'title': title,
      'modele': modele,
      'ordinateurs': ordinateurs,
      'imprimantes': imprimantes
      }

    self.generate('modele.html', template_values)

class ViewOrdinateur(BaseRequestHandler):
  def get(self, arg):
    title = 'Ordinateur introuvable'
    ordinateur = None
    # Get and displays the ordinateur informations
    try:
      id = int(arg)
      ordinateur = Ordinateur.get(db.Key.from_path('Ordinateur', id))
    except:
      ordinateur = None
      logging.error('There was an error retreiving ordinateur and its informations from the datastore')
    if not ordinateur:
      self.error(403)
      return
    else:
      title = ordinateur.code
    template_values = {
      'title': title,
      'ordinateur': ordinateur,
    }
    self.generate('ordinateur.html', template_values)

class ViewOrganisation(BaseRequestHandler):
  def get(self, arg):
    title = 'Organisation introuvable'
    organisation = None
    contacts = []
    ordinateurs = []
    imprimantes = []
    # Get and displays the organisation informations
    try:
      id = int(arg)
      organisation = Organisation.get(db.Key.from_path('Organisation', id))
      if organisation:
        contacts = Contact.gql("WHERE organisation = :1 ORDER BY nom", organisation)
    except:
      organisation = None
      contacts = []
      logging.error('There was an error retreiving organisation and its informations from the datastore')
    if not organisation:
      self.error(403)
      return
    else:
      title = organisation.nom
    template_values = {
      'title': title,
      'organisation': organisation,
      'contacts': contacts,
      'ordinateurs': ordinateurs,
      'imprimantes': imprimantes
    }
    self.generate('organisation.html', template_values)

class ViewSite(BaseRequestHandler):
  def get(self, arg):
    title = 'Site introuvable'
    site = None
    # Get and displays the statut informations
    try:
      id = int(arg)
      site = Site.get(db.Key.from_path('Site', id))
    except:
      site = None
      logging.error('There was an error retreiving site and its informations from the datastore')

    if not site:
      self.error(403)
      return
    else:
      title = site.nom

    template_values = {
      'title': title,
      'site': site
      }

    self.generate('site.html', template_values)

class ViewStatut(BaseRequestHandler):
  def get(self, arg):
    title = 'Statut introuvable'
    statut = None
    # Get and displays the statut informations
    try:
      id = int(arg)
      statut = Statut.get(db.Key.from_path('Statut', id))
    except:
      statut = None
      logging.error('There was an error retreiving statut and its informations from the datastore')

    if not statut:
      self.error(403)
      return
    else:
      title = statut.nom

    template_values = {
      'title': title,
      'statut': statut
      }

    self.generate('statut.html', template_values)

class ViewSystemeExploitation(BaseRequestHandler):
  def get(self, arg):
    title = 'SystemeExploitation introuvable'
    systeme = None
    # Get and displays the systeme informations
    try:
      id = int(arg)
      systeme = SystemeExploitation.get(db.Key.from_path('SystemeExploitation', id))
    except:
      systeme = None
      logging.error('There was an error retreiving systeme and its informations from the datastore')
    if not systeme:
      self.error(403)
      return
    else:
      title = systeme.nom
    template_values = {
      'title': title,
      'systeme': systeme
    }
    self.generate('systeme.html', template_values)

class EditApplication(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de application",
      'action': "/editApplication",
      'id': id,
      'form': form
    }
    self.generate('editApplication.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Application.get(db.Key.from_path('Application', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, ApplicationForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Application.get(db.Key.from_path('Application', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = ApplicationForm(self.request.POST, obj)
    if form.validate():
      logging.info('Application %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating application %s' % self.request.get('nom'))
      self.redirect('/application/%s' % id)
    else:
      self.go(id, form)

class EditCategorieDemande(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de categorie",
      'action': "/editCategorieDemande",
      'id': id,
      'form': form
    }
    self.generate('editCategorieDemande.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = CategorieDemande.get(db.Key.from_path('CategorieDemande', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, CategorieDemandeForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = CategorieDemande.get(db.Key.from_path('CategorieDemande', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = CategorieDemandeForm(self.request.POST, obj)
    if form.validate():
      logging.info('CategorieDemande %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating categorie demande %s' % self.request.get('nom'))
      self.redirect('/categorieDemande/%s' % id)
    else:
      self.go(id, form)

class EditCategorieIncident(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de categorie",
      'action': "/editCategorieIncident",
      'id': id,
      'form': form
    }
    self.generate('editCategorieIncident.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = CategorieIncident.get(db.Key.from_path('CategorieIncident', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, CategorieIncidentForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = CategorieIncident.get(db.Key.from_path('CategorieIncident', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = CategorieIncidentForm(self.request.POST, obj)
    if form.validate():
      logging.info('CategorieIncident %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating categorie incident %s' % self.request.get('nom'))
      self.redirect('/categorieIncident/%s' % id)
    else:
      self.go(id, form)

class EditContact(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de contact",
      'action': "/editContact",
      'id': id,
      'form': form
    }
    self.generate('editContact.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Contact.get(db.Key.from_path('Contact', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, ContactForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Contact.get(db.Key.from_path('Contact', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = ContactForm(self.request.POST, obj)
    if form.validate():
      logging.info('Contact %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating contact %s' % self.request.get('nom'))
      self.redirect('/contact/%s' % id)
    else:
      self.go(id, form)

class EditEtatDemande(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition d'etat",
      'action': "/editEtatDemande",
      'id': id,
      'form': form
    }
    self.generate('editEtatDemande.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = EtatDemande.get(db.Key.from_path('EtatDemande', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, EtatDemandeForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = EtatDemande.get(db.Key.from_path('EtatDemande', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = EtatDemandeForm(self.request.POST, obj)
    if form.validate():
      logging.info('EtatDemande %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating etat demande %s' % self.request.get('nom'))
      self.redirect('/etatDemande/%s' % id)
    else:
      self.go(id, form)

class EditEtatIncident(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition d'etat",
      'action': "/editEtatIncident",
      'id': id,
      'form': form
    }
    self.generate('editEtatIncident.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = EtatIncident.get(db.Key.from_path('EtatIncident', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, EtatIncidentForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = EtatIncident.get(db.Key.from_path('EtatIncident', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = EtatIncidentForm(self.request.POST, obj)
    if form.validate():
      logging.info('EtatIncident %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating etat incident %s' % self.request.get('nom'))
      self.redirect('/etatIncident/%s' % id)
    else:
      self.go(id, form)

class EditFabricant(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de fabricant",
      'action': "/editFabricant",
      'id': id,
      'form': form
    }
    self.generate('editFabricant.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Fabricant.get(db.Key.from_path('Fabricant', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, FabricantForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Fabricant.get(db.Key.from_path('Fabricant', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = FabricantForm(self.request.POST, obj)
    if form.validate():
      logging.info('Fabricant %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating fabricant %s' % self.request.get('nom'))
      self.redirect('/fabricant/%s' % id)
    else:
      self.go(id, form)

class EditFonction(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de fonction",
      'action': "/editFonction",
      'id': id,
      'form': form
    }
    self.generate('editFonction.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Fonction.get(db.Key.from_path('Fonction', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, FonctionForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Fonction.get(db.Key.from_path('Fonction', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = FonctionForm(self.request.POST, obj)
    if form.validate():
      logging.info('Fonction %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating fonction %s' % self.request.get('nom'))
      self.redirect('/fonction/%s' % id)
    else:
      self.go(id, form)

class EditGroupe(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de groupe",
      'action': "/editGroupe",
      'id': id,
      'form': form
    }
    self.generate('editGroupe.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Groupe.get(db.Key.from_path('Groupe', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, GroupeForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Groupe.get(db.Key.from_path('Groupe', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = GroupeForm(self.request.POST, obj)
    if form.validate():
      logging.info('Groupe %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating groupe %s' % self.request.get('nom'))
      self.redirect('/groupe/%s' % id)
    else:
      self.go(id, form)

class EditImprimante(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de imprimante",
      'action': "/editImprimante",
      'id': id,
      'form': form
    }
    self.generate('editImprimante.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Imprimante.get(db.Key.from_path('Imprimante', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, ImprimanteForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Imprimante.get(db.Key.from_path('Imprimante', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = ImprimanteForm(self.request.POST, obj)
    if form.validate():
      logging.info('Imprimante %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating imprimante %s' % self.request.get('nom'))
      self.redirect('/imprimante/%s' % id)
    else:
      self.go(id, form)

class EditDemande(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de demande",
      'action': "/editDemande",
      'id': id,
      'form': form
    }
    self.generate('editDemande.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Demande.get(db.Key.from_path('Demande', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, DemandeForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Demande.get(db.Key.from_path('Demande', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = DemandeForm(self.request.POST, obj)
    if form.validate():
      logging.info('Demande %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating demande %s' % self.request.get('nom'))
      self.redirect('/demande/%s' % id)
    else:
      self.go(id, form)

class EditIncident(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de incident",
      'action': "/editIncident",
      'id': id,
      'form': form
    }
    self.generate('editIncident.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Incident.get(db.Key.from_path('Incident', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, IncidentForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Incident.get(db.Key.from_path('Incident', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = IncidentForm(self.request.POST, obj)
    if form.validate():
      logging.info('Incident %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating incident %s' % self.request.get('nom'))
      self.redirect('/incident/%s' % id)
    else:
      self.go(id, form)

class EditModele(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de modele",
      'action': "/editModele",
      'id': id,
      'form': form
    }
    self.generate('editModele.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Modele.get(db.Key.from_path('Modele', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, ModeleForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Modele.get(db.Key.from_path('Modele', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = ModeleForm(self.request.POST, obj)
    if form.validate():
      logging.info('Modele %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating modele %s' % self.request.get('nom'))
      self.redirect('/modele/%s' % id)
    else:
      self.go(id, form)

class EditOrdinateur(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de ordinateur",
      'action': "/editOrdinateur",
      'id': id,
      'form': form
    }
    self.generate('editOrdinateur.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Ordinateur.get(db.Key.from_path('Ordinateur', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, OrdinateurForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Ordinateur.get(db.Key.from_path('Ordinateur', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = OrdinateurForm(self.request.POST, obj)
    if form.validate():
      logging.info('Ordinateur %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating ordinateur %s' % self.request.get('nom'))
      self.redirect('/ordinateur/%s' % id)
    else:
      self.go(id, form)

class EditOrganisation(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de organisation",
      'action': "/editOrganisation",
      'id': id,
      'form': form
    }
    self.generate('editOrganisation.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Organisation.get(db.Key.from_path('Organisation', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, OrganisationForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Organisation.get(db.Key.from_path('Organisation', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = OrganisationForm(self.request.POST, obj)
    if form.validate():
      logging.info('Organisation %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating organisation %s' % self.request.get('nom'))
      self.redirect('/organisation/%s' % id)
    else:
      self.go(id, form)

class EditSite(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de site",
      'action': "/editSite",
      'id': id,
      'form': form
    }
    self.generate('editSite.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Site.get(db.Key.from_path('Site', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, SiteForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Site.get(db.Key.from_path('Site', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = SiteForm(self.request.POST, obj)
    if form.validate():
      logging.info('Site %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating site %s' % self.request.get('nom'))
      self.redirect('/site/%s' % id)
    else:
      self.go(id, form)

class EditStatut(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de statut",
      'action': "/editStatut",
      'id': id,
      'form': form
    }
    self.generate('editStatut.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = Statut.get(db.Key.from_path('Statut', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, StatutForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = Statut.get(db.Key.from_path('Statut', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = StatutForm(self.request.POST, obj)
    if form.validate():
      logging.info('Statut %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating statut %s' % self.request.get('nom'))
      self.redirect('/statut/%s' % id)
    else:
      self.go(id, form)

class EditSystemeExploitation(BaseRequestHandler):
  def go(self, id, form):
    values = {
      'title': "Edition de systeme",
      'action': "/editSysteme",
      'id': id,
      'form': form
    }
    self.generate('editSystemeExploitation.html', values)

  def get(self):
    obj = None
    try:
      id = int(self.request.get('id'))
      obj = SystemeExploitation.get(db.Key.from_path('SystemeExploitation', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    self.go(id, SystemeExploitationForm(None, obj))

  def post(self):
    obj = None
    try:
      id = int(self.request.get('_id'))
      obj = SystemeExploitation.get(db.Key.from_path('SystemeExploitation', id))
    except:
      obj = None
    if not obj:
      self.error(403)
      return
    form = SystemeExploitationForm(self.request.POST, obj)
    if form.validate():
      logging.info('SystemeExploitation %d updated by user %s' % (id, users.GetCurrentUser().nickname()))
      form.populate_obj(obj)
      obj.updated_by = users.GetCurrentUser()
      try:
        obj.put()
      except:
        logging.error('There was an error updating systeme %s' % self.request.get('nom'))
      self.redirect('/systeme/%s' % id)
    else:
      self.go(id, form)
