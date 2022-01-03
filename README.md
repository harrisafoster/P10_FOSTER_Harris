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

## Prérequis de base
- Une application de type 'terminal' - GitBash, Mintty, Cygwin (si vous êtes sur Windows) 
   ou les terminaux par défaut si vous utilisez Macintosh ou Linux. 
- Python 3.9

## Installation
### Pour les développeurs et utilisateurs (windows 10, mac, linux) :
#### Clonez la source de SoftDesk localement (en utilisant votre terminal) :
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
#### Générez votre propre SECRET_KEY :
Vous allez remarquer que vous n'avez pas de fichier secret_settings.py et c'est normal. Cette étape permet de
protéger la clé secrète de l'API. Pour créer, renseigner et utiliser votre nouvelle clé secrète veuillez suivre les 
étapes ci-dessous :
```sh
$ cd SoftDesk
$ touch secret_settings.py
$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Une fois que vous aurez votre nouvelle clé secrète générée, mettez-la dans votre secret_settings.py exactement comme ceci:  
key = votre_nouvelle_clé  
Après avoir fait cela, les imports dans votre settings.py vont fonctionner correctement
#### Créez votre utilisateur admin avec :
```sh
$ python manage.py createsuperuser
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

Django API REST - 3.12.4

Django JWT Authentication - 5.0.0

Django drf Extensions - 0.7.1
