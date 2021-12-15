# P10_FOSTER_Harris
SoftDesk

Projet 10 OpenClassrooms

## API RESTful (back-end) de collaboration qui permet aux utilisateurs de :
- S'inscrire au service
- S'authentifier grâce à leurs informations de compte
- Créer/modifier/supprimer leurs propres projets
- Ajouter/modifier/supprimer les contributors (collaborateurs) de leurs propres projects
- Ajouter/modifier/supprimer des issues (problèmes) aux projets dont ils sont 'contributor' et/ou auteur
- Ajouter/modifier/supprimer des comments (commentaires) aux issues dont ils sont auteur/assignee
- Lire les informations associées aux projets dont ils sont contributor/auteur

### Documentation de l'API
- Documentation Postman disponible [ici](https://documenter.getpostman.com/view/14998980/UVR8nmcV)
- Tous les endpoints sont inclus et documentés

### Conditions de connexion et tests
Il y a déjà une base de données pré-renseignée qui contient les utilisateurs suivants :
- admin (mot de passe : password)
- staff (mot de passe : password)
- user (mot de passe : password)

Il y a donc aussi des projects, issues et commentaires. 
Vous pouvez tester les endpoints en utilisant ces utilisateurs de test.


## Prérequis de base
- Une application de type 'terminal' - GitBash, Mintty, Cygwin (si vous êtes sur Windows) 
   ou les terminaux par défaut si vous utilisez Macintosh ou Linux. 
- Python 3.9

## Installation
### Pour les développeurs et utilisateurs (windows 10, mac, linux) :
#### Clonez la source de LitReview localement (en utilisant votre terminal) :
```sh
$ git clone https://github.com/harrisafoster/P10_FOSTER_Harris
$ cd P10_FOSTER_Harris
```
##### Dans votre terminal dans le dossier P10_FOSTER_Harris/ : Créer et activer un environnement virtuel avec (windows 10) :
```sh
$ python -m venv env
$ source ./env/Scripts/activate
```
##### Créer et activer un environnement virtuel avec (mac & linux) :
```sh
$ virtualenv venv
$ source venv/bin/activate
```
##### Installez les packages requis avec :
```sh
$ pip install -r requirements.txt
```
##### Et faites les migrations nécessaires avec :
```sh
$ python manage.py migrate
```
## Utilisation
### Vous pouvez mettre l'API SoftDesk en route depuis votre terminal avec :
```sh
$ python manage.py runserver
```
Puis accédez à l'API via le port 8000 sur votre navigateur sur http://127.0.0.1:8000/api/

## Built with
Python 3.9 

Django 3.2.9