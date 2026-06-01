# Moteur d'Audit Quantitatif & Gestion des Risques Financiers

Ce projet présente un moteur d'analyse quantitative et de gestion des risques codé en Python. Il regroupe des concepts fondamentaux de la gestion des risques de marché, de la réglementation bancaire, de la sécurité des marchés automatisés et de l'analyse financière d'entreprise.

L'algorithme combine des simulations théoriques et une infrastructure robuste connectée aux données réelles du marché via l'API Yahoo Finance (`yfinance`).

---

## 🚀 Fonctionnalités et Architecture

Le script est conçu selon une approche modulaire et défensive (validation stricte des types et gestion des erreurs), articulé autour de trois piliers majeurs :

### Module 1 : Risque de Marché & Robustesse Bancaire

* **Calcul de la Value at Risk (VaR) & de l'Expected Shortfall (ES) :** Évaluation des pertes extrêmes (risques de queue ou *Fat Tails*) sur des rendements historiques réels.
* **Stress Test Bâle III :** Simulation de la dégradation des fonds propres réglementaires d'une institution financière face à un choc systémique calibré sur l'Expected Shortfall du marché.

### Module 2 : Sécurité des Marchés Algorithmiques (HFT)

* **Coupe-circuit Limit Up-Limit Down (LULD) :** Simulation des mécanismes de protection des bourses (ex: Flash Crash de 2010). Le système gèle automatiquement les transactions si les prix dévient au-delà d'un tunnel de tolérance dynamique.

### Module 3 : Valorisation Fondamentale & Viabilité

* **Modèle d'Actualisation (DCF) :** Évaluation de la valeur temps de l'argent.
$$PV = \frac{FV}{(1 + r)^n}$$


* **Trajectoire de Cash Burn :** Modélisation mathématique de l'épuisement de la trésorerie (*Runway*) lors de la phase d'échelle (*scaling*) d'une entreprise présentant une marge unitaire négative.

---

## 📊 Visualisations Graphiques

Le projet intègre un module de datavisualisation utilisant `matplotlib` pour analyser visuellement les résultats de l'audit quantitatif.

Voici le rendu obtenu lors d'un crash-test sur l'action **Tesla (TSLA)** :

* **À gauche :** La courbe de Cash Burn met en évidence l'effondrement de la trésorerie et le point de faillite précis (intersection avec la ligne $0\$$).
* **À droite :** L'histogramme des rendements quotidiens réels montre la distribution des variations de marché, matérialisée par la "ligne rouge" de la VaR (95%).

---

## 🛠️ Installation et Prérequis

Ce projet est entièrement autonome et tient dans un fichier unique pour faciliter son exécution.

### Prérequis

Assure-toi d'avoir installé les bibliothèques nécessaires :

```bash
pip install numpy yfinance matplotlib

```

### Structure du dépôt

```text
├── audit_quantitatif.py  # Fichier principal contenant les classes et le crash-test
└── README.md             # Documentation du projet

```

---

## 💻 Utilisation

Pour lancer l'audit quantitatif et générer les graphiques, exécutez simplement le script principal :

```bash
python audit_quantitatif.py

```

### Exemple de sortie du terminal (Logs)

Le projet intègre le module standard `logging` de Python pour assurer une traçabilité industrielle des alertes :

```text
INFO - === DÉMARRAGE DE L'AUDIT QUANTITATIF (LIVE DATA) ===
INFO - [MODULE 1A] Téléchargement des données pour TSLA (1 dernière année)...
INFO -  -> 252 jours de trading analysés. Prix actuel : 178.42$
INFO -  -> Value at Risk (VaR 95%) : -4.42% (Pire perte quotidienne 'normale')
INFO -  -> Expected Shortfall (ES 95%) : -6.15% (Moyenne du gouffre)
INFO - [MODULE 1B] Stress Test Bâle III (Basé sur le choc réel)
WARNING - Banque insolvable. Pertes (615,231$) > Fonds propres (500,000$)
INFO - [MODULE 2] Sécurité Haute Fréquence (Flash Crash simulé)
ERROR - COUPE-CIRCUIT ACTIVÉ. Le prix (151.66$) est hors tolérance.
INFO - [MODULE 3] Valorisation DCF & Cash Burn
INFO -  -> DCF : Valeur actuelle de 10M€ dans 5 ans : 6,209,213.23 €
CRITICAL - FAILLITE MATHÉMATIQUE ATTEINTE à l'étape 4 (Trésorerie: -39000.0$).
INFO - === FIN DE L'AUDIT ===

```

---

## 📈 Perspectives d'Évolution

* **VaR Paramétrique & GARCH :** Intégrer un calcul de VaR basé sur une distribution normale et modéliser la volatilité conditionnelle.
* **Modèle CAPM (MEDAF) :** Calculer dynamiquement le taux d'actualisation ($r$) du module DCF en fonction du coefficient Bêta de l'actif par rapport à son indice de référence.
* **Optimisation de Portefeuille :** Étendre le module de risque à un portefeuille multi-actifs en utilisant la frontière efficiente de Markowitz.

---

## 📇 Contact

* **Auteur :** Alexandre RETENO NZOGHE
* **Formation :** Étudiant en Licence Mathématiques & Informatique 
* **Ville :** Lyon, France
