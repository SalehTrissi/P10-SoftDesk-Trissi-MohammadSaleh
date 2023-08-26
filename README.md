# P10-SoftDesk-Trissi-MohammadSaleh
OpenClassRooms - Créez une API sécurisée RESTful en utilisant Django REST

SoftDesk,

Est une société d'édition de logiciels de collaboration.
Il s'agit d'une API réalisée avec Django.
L'application permet de remonter et suivre des problèmes techniques (issue tracking system).

## Caractéristiques

## Installation & lancement
Commencez tout d'abord par installer Python.

Lancez la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/SalehTrissi/P10-SoftDesk-Trissi-MohammadSaleh.git
```
Placez vous dans le dossier P10-SoftDesk-Trissi-MohammadSaleh, puis créez un nouvel environnement virtuel:
```
python -m venv env
```
Ensuite, active-le:
Sur WINDOWS:
```
env\scripts\activate
```
Sur LINUX:
```
source env/bin/activate
```
Installez ensuite les packages requis:
```
pip install -r requirements.txt
```
Ensuite, placez vous à la racine du projet (là ou se trouve le fichier manage.py), puis effectuez les migrations:
```
python manage.py makemigrations
```
Puis: 
```
python manage.py migrate
```
Il ne vous reste plus qu'à lancer le serveur: 
```
python manage.py runserver
```
Vous pouvez ensuite utiliser l'applicaton à l'adresse suivante:
```
http://127.0.0.1:8000
```