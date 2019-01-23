# Just Code IT : Site

## Expliquation des dossiers et fichiers.

**Merci de ne pas toucher au dossier `venv/`**

* Le dossier `jci_site/template/` contient tous les templates des pages webs.
* Le dossier `jci_site/static/` contient le css et les fichies fixes du site.
* Le fichier `jci_site/__init__.py` contient les initialisations de l'application web.
* Le fichier `jci_site/forms.py` contient les formulaires du site.
* Le fichier `jci_site/models.py` contient les modèles de la base de donnée.
* Le fichier `jci_site/routes.py` contient les routes du site.
* Le fichier `jci_site/site.db` est la base de donnée.

## Comment utiliser le projet ?

1. Tout d'abord, pensez à clone le projet.
2. Pensez à créer un "environnement virtuel", en tappant :
Si 2 versions de python sont installées

```shell
python3 -m venv venv
```
Sinon:
```shell
python -m venv venv
```
Si aucun ne marche:
```shell
py -m venv venv
```
4. Il vous faut activer l'environnement virtuel maintenant
```shell
# Si vous êtes sur linu / mac ?
source venv/bin/activate 

# Sur windows
./venv/Scripts/activate
```

4. Enfin, installez les dépendances
```shell
pip install flask flask_sqlalchemy flask_bcrypt flask_login flask_wtf Pillow
```
5. Il ne rest plus qu'a lancez en tappant
```shell
python run.py
```
