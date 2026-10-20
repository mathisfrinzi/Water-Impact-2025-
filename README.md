# Water-Impact 🌊

**Logiciel de modélisation du rafraîchissement urbain apporté par la végétation et la présence d'eau.**

Projet réalisé dans le cadre du **PAI** (Projet d'Application Industriel) à **Centrale Lyon**. Le cabinet d'architectes **UrbanWater** a commandité à notre groupe de 6 élèves un outil permettant d'évaluer le critère de rafraîchissement qu'apporterait la présence d'eau et de végétation dans les quartiers.

## Objectif

L'outil permet de :

- **construire une carte de quartier** sur un maillage personnalisable (taille, résolution) ;
- y placer des **bâtiments**, des **surfaces d'eau** et de la **végétation** (arbres paramétrables : hauteur, rayon, coefficient d'échange…) ;
- définir les **matériaux de revêtement** du sol (albédo, conductivité et diffusivité thermique, émissivité, porosité, perméabilité, capacité thermique…) ;
- régler les **conditions météorologiques** (température, humidité relative, vent, irradiance solaire) ;
- **lancer une simulation** du microclimat local et visualiser la contribution de chaque élément du quadrillage au **réchauffement** ou au **rafraîchissement** (en °C).

## Modélisation physique

La simulation s'appuie sur un bilan thermique par maille, incluant notamment :

- l'**évapotranspiration** de la végétation et des matériaux poreux (en mm/jour), calculée via la pente de vapeur saturante et des grandeurs psychrométriques ;
- l'**ombrage** des bâtiments et des arbres sur l'irradiance reçue au sol (W/m²) ;
- les **propriétés radiatives et thermiques** des matériaux (albédo, émissivité, diffusivité, conductivité, masse volumique, capacité thermique) ;
- la **température de l'eau** et les échanges avec l'atmosphère ;
- la résolution d'équilibres par **`scipy.optimize.fsolve`**.

Chaque grandeur physique est documentée dans le logiciel (unités et signification : température en K, humidité en %, pression en Pa, vent en m/s, etc.).

## Aperçu du logiciel

L'interface (Tkinter) s'organise en trois volets : la carte maillée du quartier, les paramètres de simulation et les résultats.


## Démarrage rapide

### Prérequis

- Python 3.8+
- Les dépendances listées dans `requirements.txt` :

```bash
pip install -r requirements.txt
```

### Lancer le logiciel

```bash
python Logiciel.py
```

Une carte par défaut est chargée au démarrage (`RessourceLogiciel/defaut.txt`). Elle peut être modifiée ou remplacée directement dans l'interface.

## 📖 Guide d'utilisation

1. **Définir la carte** : maillage (taille, résolution), puis placer bâtiments, surfaces d'eau et arbres via les boutons dédiés.
2. **Renseigner les matériaux** : sélectionner ou créer les revêtements et végétations avec leurs paramètres physiques.
3. **Régler la météo** : température, humidité, vent, irradiance dans l'onglet correspondant.
4. **Lancer la simulation** et visualiser les cartes de réchauffement / rafraîchissement.
5. **Interroger une maille** : la formule intégrée permet d'évaluer des grandeurs physiques en tout point, par ex. `TEMPERATURE(x,y,z)`, `EVAPOTRANSPIRATION(x,y,z)`, `IRRADIANCE_OMBRAGE(x,y,z)`, `RESULTATS_SIMU(x,y,z)`, …

## 🗂️ Structure du projet

```
Water-Impact-2025-
├── Logiciel.py            # Application principale (interface + simulation)
├── requirements.txt       # Dépendances Python
└── RessourceLogiciel/     # Ressources (logo, carte par défaut, etc.)
```

## 👥 Équipe

Projet mené en équipe de 6 élèves-ingénieurs pour le cabinet d'architectes UrbanWater, dans le cadre du PAI de Centrale Lyon.

## 📄 Licence

Projet réalisé dans un cadre pédagogique. Contactez-moi pour toute réutilisation.
