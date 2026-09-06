## Objectif de cette étape

Transformer les cas d’usage et les responsabilités identifiées précédemment en grands composants concrets à développer.

À ce stade, on ne définit pas encore toutes les fonctions, signatures ou classes. On cherche simplement à obtenir une carte suffisamment claire pour pouvoir commencer à coder sans devoir redécider constamment de l’organisation générale du projet.

## Méthode générale

À partir de l’ensemble des cas d’usage :

1. Identifier les concepts ou données principales manipulées.
2. Regrouper les opérations qui concernent le même domaine.
3. Isoler les opérations de persistance.
4. Isoler la logique métier.
5. Identifier la couche qui expose les fonctionnalités à l’extérieur.
6. Identifier les éléments techniques nécessaires au fonctionnement de l’application.
7. Transformer ces groupes en composants/modules potentiels.
8. Décider seulement ensuite si chaque composant sera implémenté avec des fonctions, des classes ou une combinaison des deux.

Raccourci mental :

cas d’usage
→ responsabilités
→ regroupements fonctionnels
→ composants
→ fichiers/modules
→ code

---

# Application au projet Sensor Monitoring API

## 1. Gestion des capteurs

Responsabilité :

Gérer les métadonnées des capteurs.

Doit permettre notamment :

* créer un capteur ;
* récupérer un capteur ;
* lister les capteurs ;
* supprimer un capteur ;
* vérifier l’existence d’un capteur.

Les informations décrivant un capteur sont persistées dans la base.

Il n’est pas nécessaire de créer une classe métier complexe `Sensor` si elle n’apporte aucun comportement utile.

---

## 2. Gestion des mesures

Responsabilité :

Gérer les mesures produites par les capteurs.

Doit permettre notamment :

* enregistrer une mesure ;
* récupérer les mesures d’un capteur ;
* récupérer les mesures sur une période ;
* gérer le cas d’un capteur sans mesure.

Une mesure reste enregistrable même si sa valeur est située hors de la plage normale du capteur.

---

## 3. Persistance / SQLite

Responsabilité :

Centraliser l’accès aux données persistantes.

Doit permettre notamment :

* initialiser la base SQLite ;
* définir les structures nécessaires pour les capteurs et les mesures ;
* gérer la relation entre une mesure et son capteur ;
* créer, lire et supprimer des capteurs ;
* créer et lire des mesures ;
* effectuer les requêtes nécessaires aux autres composants.

La logique métier ne doit pas dépendre directement des détails SQL lorsqu’il est raisonnable de les isoler.

---

## 4. Statistiques

Responsabilité :

Produire un résumé statistique des mesures d’un capteur, éventuellement sur une période.

Le résumé demandé contient au minimum :

* nombre de mesures ;
* minimum ;
* maximum ;
* moyenne.

Le composant doit également gérer explicitement le cas où aucune mesure n’est disponible.

Il n’est pas nécessaire de créer une méthode indépendante pour chaque statistique si un calcul de résumé unique suffit.

---

## 5. Détection des anomalies

Responsabilité :

Identifier les mesures qui violent les bornes métier définies pour un capteur.

Une mesure est anormale lorsque :

value < min_valid_value

ou

value > max_valid_value

Cette détection est distincte d’une détection statistique d’outliers.

Pour ce projet, on reste uniquement sur les bornes métier.

---

## 6. Validation des données

Responsabilité :

Définir les structures attendues par l’application et vérifier leur cohérence.

Doit notamment permettre de valider :

* création d’un capteur ;
* création d’une mesure ;
* types des champs ;
* champs obligatoires ;
* bornes du capteur ;
* paramètres temporels ;
* structures retournées par certains endpoints.

Une partie de cette validation pourra être assurée naturellement par FastAPI/Pydantic.

---

## 7. API / routes

Responsabilité :

Exposer les cas d’usage via HTTP.

Les grandes familles fonctionnelles seront :

* capteurs ;
* mesures ;
* statistiques ;
* anomalies.

Les routes doivent principalement :

1. recevoir la requête ;
2. récupérer les paramètres ;
3. appeler le composant approprié ;
4. transformer les erreurs métier en réponses HTTP adaptées ;
5. retourner le résultat.

La logique métier importante ne doit pas être écrite directement dans les routes si elle peut être isolée proprement.

---

## 8. Initialisation de l’application

Responsabilité :

Permettre à l’application de démarrer correctement.

Doit notamment gérer :

* création de l’application FastAPI ;
* connexion/configuration de SQLite ;
* initialisation des tables ;
* intégration des différentes routes.

Cette partie doit rester légère.

---

## 9. Tests

Responsabilité :

Vérifier que les comportements importants restent corrects.

Les tests devront couvrir notamment :

* gestion des capteurs ;
* enregistrement des mesures ;
* validations importantes ;
* récupération par période ;
* statistiques ;
* anomalies ;
* cas d’erreur principaux.

Les tests sont une responsabilité transverse : ils vérifient plusieurs composants plutôt que de constituer une fonctionnalité métier.

---

# Carte fonctionnelle simplifiée

API / routes
↓
validation
↓
gestion capteurs / gestion mesures
↓
stats / anomalies lorsque nécessaire
↓
persistance SQLite

Avec comme éléments transverses :

* initialisation/configuration ;
* tests.


