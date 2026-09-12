# Sensor Monitoring API

Mini-projet backend en **Python + FastAPI + SQLite**.

Objectif : construire une API simple de suivi de capteurs industriels, avec persistance, statistiques, détection d'anomalies et tests.

## Données

### Capteur

* `id`
* `name`
* `sensor_type`
* `unit`
* `min_valid_value`
* `max_valid_value`

### Mesure

* `id`
* `sensor_id`
* `timestamp`
* `value`

Le modèle peut être légèrement enrichi si nécessaire.

## Fonctionnalités

### Capteurs

L'API doit permettre de :

* créer un capteur ;
* récupérer un capteur par ID ;
* lister les capteurs ;
* supprimer un capteur.

Les entrées invalides et les capteurs inexistants doivent être gérés correctement.

### Mesures

Permettre :

* d'ajouter une mesure à un capteur existant ;
* de récupérer les mesures d'un capteur ;
* de filtrer les mesures par période ;
* de retourner les mesures dans l'ordre chronologique.

Une mesure ne peut pas référencer un capteur inexistant.

### Statistiques

Pour un capteur et une période, retourner au minimum :

* nombre de mesures ;
* minimum ;
* maximum ;
* moyenne.

Le cas où aucune mesure n'existe doit être géré explicitement.

### Anomalies

Une mesure est hors plage si :

`value < min_valid_value` ou `value > max_valid_value`.

L'API doit permettre de récupérer ces mesures sur une période.

Une mesure hors plage reste **une mesure valide et enregistrable**. La validation des entrées et la détection métier des anomalies sont deux choses différentes.

## Persistance

Utiliser **SQLite** avec une vraie persistance entre les redémarrages.

Le choix de la couche d'accès aux données ou de l'ORM est libre.

Pas de PostgreSQL, Redis ou infrastructure distribuée.

## Validation et erreurs

Gérer au minimum :

* capteur inexistant ;
* entrée invalide ;
* bornes de capteur incohérentes ;
* période temporelle incohérente ;
* absence de données lorsque nécessaire.

Utiliser des codes HTTP adaptés.

## Tests

Tests automatisés avec `pytest` ou équivalent.

Cas minimum :

* création valide/invalide d'un capteur ;
* récupération d'un capteur existant/inexistant ;
* ajout valide d'une mesure ;
* ajout sur un capteur inexistant ;
* récupération des mesures par période ;
* statistiques sur des valeurs connues ;
* statistiques sans mesure ;
* anomalies sous la borne, au-dessus de la borne et exactement sur les bornes.

## Données de démonstration

Prévoir un moyen simple de générer environ :

* 4 à 6 capteurs ;
* 100 à 500 mesures.

Pas besoin d'un générateur statistique complexe.

## Contraintes techniques

Le projet doit utiliser :

* Python moderne ;
* annotations de types raisonnables ;
* FastAPI ;
* SQLite ;
* persistance réelle ;
* tests automatisés ;
* gestion explicite des erreurs ;
* dépendances déclarées.

Hors scope :

* frontend ;
* authentification/utilisateurs ;
* permissions ;
* cloud ;
* microservices ;
* Docker obligatoire ;
* async sans nécessité.

## Architecture

L'architecture est à concevoir pendant le projet.

Elle doit séparer raisonnablement :

* routes API ;
* accès aux données ;
* logique métier ;
* modèles/validation ;
* tests.

Éviter aussi bien le `main.py` géant que la surarchitecture inutile.

## README

Le repo doit expliquer brièvement :

* le but du projet ;
* l'installation ;
* le lancement de l'API ;
* le lancement des tests ;
* si nécessaire, la génération des données de démonstration.

## Projet terminé si

Le projet est considéré terminé si :

1. le repo peut être cloné et l'environnement recréé ;
2. l'API démarre et SQLite fonctionne ;
3. les capteurs peuvent être créés, listés, récupérés et supprimés ;
4. les mesures peuvent être enregistrées et interrogées par période ;
5. les statistiques fonctionnent ;
6. les anomalies sont détectées ;
7. les erreurs principales sont gérées ;
8. les tests essentiels passent ;
9. l'architecture du code est claire et justifiable.