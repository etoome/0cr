0CR Backend
============

Partie backend du projet **0CR**. Codée grâce à [Flask](https://flask.palletsprojects.com/).

# Setup

## Dépendances:

```bash
virtualenv -p python3.8 venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## ENV:

Commande pour que flask sache où trouver le code a démarrer.

```bash
export FLASK_APP=flaskr
```

## Initialisation database:
```bash
flask init-db
```

## Compilation des modèles
```bash
python cnn/cnn.py compile
python cnn/cnn_chinese.py compile
```
Les informations des modèles se trouveront dans le fichier `models/`

# Démarrage:

## Dev mode:
```bash
export FLASK_ENV=developpement
flask run
```

## Prod:

TODO
