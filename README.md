# User guide
Cette application permet de générer différents graphiques sur la consommation annuelle d’électricité et gaz par région.

1. Pour commencer, veuillez ouvrir le dossier se "Projet" dans Visual Studio Code.
2. Ensuite, rendez-vous dans le terminale de VS Code et veuillez exécuter le commande suivante (ctrl+j si console fermée) : 'pip install -r ./requirements.txt'
3. Une fois l'installation terminée, allez dans le fichier Dashboard.py et exécuter le code à l'aide du boutton Run en haut à droite.
4. Ouvrez votre navigateur internet et rechercher le site suivant : http://127.0.0.1:8050


#  Rapport d'analyse
## Introduction :
Ce rapport présente les résultats d'une analyse de la consommation annuelle d'électricité et de gaz par région en France. Les données ont été collectées à l'aide d'une API du site data.gouv et ont été analysées en utilisant des outils tels que pandas et plotly pour générer des graphiques et une carte de la France. L'objectif de cette analyse est de comprendre les tendances de consommation d'énergie dans les différentes régions de France et de fournir des informations utiles pour la prise de décision.

## Méthodologie :
Les données ont été collectées à l'aide d'une API du site data.gouv, qui fournit des données sur la consommation annuelle d'électricité et de gaz par région en France. Nous avons utilisé un dashboard pour permettre à l'utilisateur de sélectionner les paramètres de son choix (année, régions, industrie, etc.) et de générer des graphiques et une carte de la France.

## Conclusion :
L'analyse des données de consommation d'énergie par région en France montre des différences significatives dans les niveaux de consommation d'électricité et de gaz. Les régions du nord et de l'est de la France ont généralement des niveaux de consommation plus élevés, tandis que les régions du sud et de l'ouest ont des niveaux de consommation plus faibles. Cette information peut être utilisée pour cibler les efforts de réduction de la consommation d'énergie et pour élaborer des stratégies de développement durable adaptées aux besoins de chaque région.

## Recommandations :
Il serait intéressant de suivre l'évolution de la consommation d'énergie par région au fil du temps. Il serait également utile d'explorer d'autres sources de données pour obtenir une vision plus complète de la consommation d'énergie en France et de ses déterminants.


# Developper Guide
1. Récupération des données :
Télécharger l'API du site data.gouv.
Utiliser l'API pour récupérer les données de consommation annuelle d'électricité et de gaz par région en France.

2. Création du dashboard :
Utilisation de l'outil de création de dashboard, tel que plotly, pour créer un interface permettant à l'utilisateur de sélectionner les années et les régions qu'il souhaite afficher.
Récupérer à l'aide de callback les paramètres fournit par l'utilisateur.
Faire une reqête à avec les nouveaux paramètres, en rendant l'URL dynamique.

3. Analyse des données :
Utiliser pandas pour analyser les données de consommation d'électricité et de gaz par région.
Générez des graphiques à l'aide de Plotly pour illustrer les résultats de l'analyse.