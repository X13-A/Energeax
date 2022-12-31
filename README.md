# User guide
Cette application permet de générer différents graphiques sur la consommation annuelle d’électricité et de gaz par région en France.

## Installation :
1. Pour commencer, rendez vous dans le répertoire principal du projet et exécutez la commande suivante: 'pip install -r ./requirements.txt'
3. Une fois l'installation des modules terminée, éxecutez la commande suivante, toujours dans le répertoire principal : 'python main.py'
4. Ouvrez votre navigateur internet et rendez vous à l'adresse suivante: http://127.0.0.1:8050

## Utilisation du dashboard:
### Pour afficher les données:
1. Choisissez le type d'affichage que vous voulez
2. Configurez vos filtres
3. Cliquez sur update
4. Quand le traitement des données est terminé, cliquez sur "Afficher"
### Si rien n'est spécifié dans le filtre:
- Pour les secteurs: Tout est selectionné
- Pour les régions: Tout est selectionné
- Pour la période: L'année 2021 est selectionnée
### Fonctionnement du filtre début / fin:
- Si une seule valeur est choisie, elle seule sera retenue
- Si deux valeurs sont choisies, un intervalle entre le début et la fin sera utilisé
- Les données ne s'actualiseront pas si l'intervalle est invalide (début > fin)
- Pour l'histogramme, seul la date de fin est retenue
### Les 3 types d'affichages:
- Le graphique permet d'étudier l'évolution de la consommation de plusieurs régions de façon superposée
- La carte affiche la moyenne de consommation de chaque région pour la période choisie
- L'histogramme compte le nombre de lieux dans chaque tranche de consommation

#  Rapport d'analyse
## Introduction :
Ce rapport présente les résultats d'une analyse de la consommation annuelle d'électricité et de gaz par région en France. Les données ont été collectées à l'aide d'une API du site data.gouv et ont été analysées en utilisant des outils tels que pandas et plotly pour générer des graphiques et une carte de la France. L'objectif de cette analyse est de comprendre les tendances de consommation d'énergie dans les différentes régions de France et de fournir des informations utiles pour la prise de décision.

## Méthodologie :
Les données ont été collectées à l'aide d'une API du site data.gouv, qui fournit des données sur la consommation annuelle d'électricité et de gaz par région en France. Nous avons utilisé un dashboard pour permettre à l'utilisateur de sélectionner la configuration de son choix (année, régions, industrie, etc.) et de générer des graphiques et une carte de la France pour visualiser les données.

## Conclusion :
L'analyse des données de consommation d'énergie par région en France montre des différences significatives dans les niveaux de consommation d'électricité et de gaz. Les régions du nord et de l'est de la France ont généralement des niveaux de consommation plus élevés, tandis que les régions du sud et de l'ouest ont des niveaux de consommation plus faibles. Cette information peut être utilisée pour cibler les efforts de réduction de la consommation d'énergie et pour élaborer des stratégies de développement durable adaptées aux besoins de chaque région. D'autre part, la tendance de consommation semble être restée relativement stable, avec une légère chute pendant la période du COVID-19 et une légère hausse de façon générale chaque année.

## Pistes d'amélioration :
Il aurait été intéressant de croiser ces données avec le coût de l'électricité en France, afin de voir la coût annuel moyen d'un foyer ou autres statistiques similaires.
Il serait également utile d'explorer d'autres sources de données pour obtenir une vision plus complète de la consommation d'énergie en France et de ses déterminants.


# Developper Guide

## Architecture du projet
- Les données sont récupérées à l'aide de l'API et de requêtes HTML.
- Toutes les requêtes et le formattage de données sont concentrées dans les fichiers contenus dans le dossier "requests".
- Chaque fichier du dossier "requests" permet la construction d'un type d'affichage (carte, graphique, histogramme).
- Le fichier build_url.py permet de générer un URL à partir de filtres pour faire une requête à l'API.
- Le dashboard est créé dans le fichier main.py.
- Les constantes sont stockés dans le fichier constants.py pour un usage global.
- Le CSS et les assets sont stockés dans le dossier "assets".

## Ajout de données
1. Pour récupérer des données et pouvoir les traiter, il est nécéssaire de générer un URL à l'aide du fichier build_url.py et d'un dictionnaire de filtres.
2. Pour formatter les données, utiliser les dictionnaires python et le module pandas.
3. Pour créer un affichage, utiliser le module plotly et dash.
4. Pour rendre le tout visible sur le dashboard, ajouter l'affichage au layout dans main.py.

## Modification du dashboard
- Le dashboard peut être modifié dans le fichier main.py.
- Les interactions sont gérées à l'aide des callbacks de python dash, toujours dans main.py.
- L'apparance du dashboard peut être modifiée dans le fichier "assets/styles.css".
- Si un module est ajouté, le préciser dans le fichier requirements.txt.