# Design notes — Sensor Monitoring API

Notes sur la démarche utilisée pour passer du cahier des charges à une première architecture.
---

# 1. Partir des cas d'usage

Avant de penser aux routes, fichiers ou classes, traduire le besoin en actions métier.

Pour chaque action :

1. Que veut faire l'utilisateur ?
2. Quelles informations sont nécessaires ?
3. Quel résultat doit être retourné ?

Raccourci :

`besoin → action → entrées → sortie`

## Application au projet

| Cas d'usage              | Entrées                        | Sortie                             |
| ------------------------ | ------------------------------ | ---------------------------------- |
| Créer un capteur         | informations du capteur        | capteur créé + ID                  |
| Consulter un capteur     | sensor ID                      | métadonnées                        |
| Lister les capteurs      | —                              | liste des capteurs                 |
| Supprimer un capteur     | sensor ID                      | confirmation / absence de résultat |
| Ajouter une mesure       | sensor ID, timestamp, valeur   | mesure créée / confirmation        |
| Récupérer les mesures    | sensor ID, période optionnelle | liste de mesures                   |
| Obtenir les statistiques | sensor ID, période optionnelle | résumé statistique                 |
| Récupérer les anomalies  | sensor ID, période optionnelle | mesures hors plage                 |

À ce stade, ne pas encore penser JSON, FastAPI, SQL ou structure des fichiers.

---

# 2. Définir validations et cas limites

Pour chaque cas d'usage, vérifier :

* les données sont-elles présentes et correctement typées ?
* la ressource existe-t-elle ?
* les règles métier sont-elles respectées ?
* que faire lorsqu'il n'y a aucun résultat ?

Raccourci :

`cas d'usage → données valides ? → ressource existe ? → règle métier ? → absence de résultat ?`

## Décisions du projet

### Capteurs

Création :

* champs obligatoires et types valides ;
* `min_valid_value <= max_valid_value` ;
* ID généré par le système ;
* décider si certains champs, par exemple `name`, doivent être uniques.

Consultation / suppression :

* le capteur doit exister ;
* sinon retourner une erreur explicite.

Liste :

* aucun capteur → liste vide.

Pour la suppression, décider ce qu'il advient des mesures associées.

### Mesures

Création :

* structure et types valides ;
* le capteur doit exister.

Une valeur hors plage **reste une mesure valide**. Elle doit pouvoir être enregistrée afin d'être détectée comme anomalie.

Consultation :

* le capteur doit exister ;
* une période éventuelle doit être cohérente ;
* aucune mesure → liste vide.

### Statistiques

* le capteur doit exister ;
* la période doit être valide ;
* gérer explicitement le cas sans mesure ;
* avec des données : `count`, `min`, `max`, `mean`.

### Anomalies

* le capteur doit exister ;
* la période doit être valide ;
* aucune anomalie → liste vide.

## Deux types de validation

**Validation structurelle**

Exemples : champ manquant, mauvais type, timestamp mal formé.

Une grande partie pourra être prise en charge par FastAPI/Pydantic.

**Validation métier**

Exemples : capteur inexistant, bornes incohérentes, période invalide.

Elle dépend des règles de l'application.

---

# 3. Identifier les responsabilités

Décomposer ensuite chaque cas d'usage en étapes et déterminer à quelle responsabilité appartient chaque étape.

Quatre grandes responsabilités :

### API / HTTP

* recevoir la requête ;
* lire les paramètres ;
* appeler le reste du système ;
* retourner la réponse ;
* traduire les erreurs en réponses HTTP adaptées.

### Validation

* structures et types ;
* identifiants ;
* périodes ;
* règles de cohérence.

### Persistance

* créer, lire et supprimer les données ;
* gérer SQLite et les relations entre données.

### Logique métier

* statistiques ;
* détection des anomalies ;
* autres règles propres au domaine.

Un cas d'usage traverse généralement plusieurs responsabilités.

Exemple :

`POST mesure`

→ HTTP reçoit la requête
→ validation de l'entrée
→ vérification du capteur en base
→ enregistrement de la mesure
→ réponse HTTP

---

# 4. Passer des responsabilités aux composants

Une fois les cas d'usage et responsabilités compris :

1. identifier les données/concepts principaux ;
2. regrouper les opérations liées ;
3. isoler la persistance ;
4. isoler la logique métier ;
5. identifier la couche API ;
6. ajouter les besoins techniques ;
7. transformer ces groupes en modules ;
8. décider seulement ensuite si fonctions ou classes sont nécessaires.

Raccourci :

`cas d'usage → responsabilités → composants → modules → code`

Ne pas créer une classe simplement parce qu'un concept métier existe. Une classe doit apporter quelque chose : état, comportement, encapsulation, etc.

---

# 5. Composants retenus pour le projet

## Gestion des capteurs

Gère les métadonnées des capteurs :

* création ;
* récupération ;
* liste ;
* suppression ;
* vérification d'existence.

Pas besoin a priori d'une classe métier `Sensor` complexe.

## Gestion des mesures

* enregistrer une mesure ;
* récupérer les mesures d'un capteur ;
* filtrer par période ;
* gérer l'absence de mesures.

Une mesure hors plage reste enregistrable.

## Persistance / SQLite

Centralise l'accès aux données :

* configuration et initialisation SQLite ;
* structures capteurs/mesures ;
* relation mesure → capteur ;
* opérations de lecture/écriture nécessaires.

Éviter de disperser les détails SQL dans la logique métier.

## Statistiques

Produit pour un capteur et éventuellement une période :

* `count`
* `min`
* `max`
* `mean`

Gère également le cas sans données.

Pas besoin d'une fonction ou méthode différente pour chaque statistique si un résumé unique suffit.

## Anomalies

Règle métier :

`value < min_valid_value`
ou
`value > max_valid_value`

Il s'agit d'une détection par **bornes métier**, pas d'une détection statistique d'outliers.

## Validation

Définit et contrôle notamment :

* création des capteurs ;
* création des mesures ;
* champs et types ;
* bornes ;
* périodes ;
* structures de sortie.

FastAPI/Pydantic prendra en charge une partie de ce travail.

## API / routes

Familles principales :

* capteurs ;
* mesures ;
* statistiques ;
* anomalies.

Une route doit rester légère :

`requête → paramètres → appel du composant → gestion erreur HTTP → réponse`

La logique métier importante ne doit pas vivre directement dans les routes.

## Initialisation

Partie légère chargée de :

* créer l'application FastAPI ;
* configurer SQLite ;
* initialiser les tables ;
* intégrer les routes.

## Tests

Responsabilité transverse couvrant :

* capteurs ;
* mesures ;
* validations ;
* périodes ;
* statistiques ;
* anomalies ;
* erreurs principales.

---

# 6. Vue globale

Flux simplifié :

```text
API / routes
      ↓
validation
      ↓
gestion capteurs / mesures
      ↓
logique métier (stats / anomalies)
      ↓
persistance SQLite
```

Ce schéma est une vue conceptuelle, pas une obligation de faire exactement un fichier ou une classe par bloc.

---

# 7. Plan d'implémentation

1. Repo + environnement Python
2. Dépendances
3. Structure minimale du projet
4. SQLite
5. Modèles/structures capteurs et mesures
6. Gestion des capteurs
7. Routes capteurs
8. Gestion des mesures
9. Routes mesures
10. Statistiques
11. Détection des anomalies
12. Routes stats/anomalies
13. Tests
14. Génération de données de démonstration
15. Nettoyage + README

---

# Méthode à retenir

Pour un futur projet similaire :

```text
Cahier des charges
        ↓
Cas d'usage
        ↓
Entrées / sorties
        ↓
Validations et cas limites
        ↓
Responsabilités
        ↓
Composants
        ↓
Modules / architecture
        ↓
Implémentation
        ↓
Tests
```

