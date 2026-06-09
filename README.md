# 📊 PAPETIS DISTRIBUTION — Système de Prévisions des Ventes 2026

Application web interactive développée avec **Streamlit** pour calculer et visualiser les prévisions de ventes 2026 selon un modèle multiplicatif (MCO).

---

## ⚙️ Prérequis

- Python 3.10 ou supérieur
- Anaconda (recommandé)

---

## 📦 Installation des dépendances

Ouvre **Anaconda Prompt** et tape :

```
pip install streamlit pandas numpy matplotlib openpyxl
```

---

## 🚀 Lancement de l'application

Dans **Anaconda Prompt**, tape :

```
streamlit run C:\chemin\vers\site_projet.py
```

Le site s'ouvre automatiquement dans ton navigateur à l'adresse :
```
http://localhost:8501
```

---

## 📁 Fichier Excel requis

Le fichier Excel source doit contenir exactement **deux feuilles** :

| Feuille | Colonnes attendues |
|---|---|
| `Ventes globales` | Annee, Mois, Nom_Mois, t, Ventes |
| `Ventes par famille` | Annee, Mois, Nom_Mois, t, Cahiers, Classeurs, Ecriture, Technique, Manuels, Bureau, Total |

- 60 lignes de données (janvier 2021 à décembre 2025)
- Unité : kMAD (milliers de dirhams marocains)

---

## 🖥️ Utilisation

1. Lancer l'application (voir ci-dessus)
2. Cliquer sur **📂 Charger le fichier Excel**
3. Sélectionner le fichier `papetis_ventes_historiques.xlsx`
4. Les résultats s'affichent automatiquement :
   - KPIs (CA 2025, prévision 2026, pente, R²)
   - Graphique historique + prévisions
   - Graphique des coefficients saisonniers
   - Graphique des prévisions mensuelles 2026
   - Tableau détaillé des prévisions
5. Cliquer sur **📥 Télécharger Excel** pour exporter les résultats

---

## 📊 Ce que l'application calcule

| Étape | Description |
|---|---|
| **MCO** | Calcul de la tendance linéaire Tt = a·t + b |
| **R²** | Coefficient de détermination de l'ajustement |
| **Coefficients saisonniers** | 12 coefficients normalisés (somme = 12) |
| **Prévisions 2026** | Prevision_t = Tt × Cs pour t = 61 à 72 |

---

## 📂 Structure des fichiers

```
projet/
│
├── site_projet.py          ← Application Streamlit (fichier principal)
├── README.md               ← Ce fichier
└── papetis_ventes_historiques.xlsx  ← Données source (à fournir)
```

---

## ❗ Problèmes fréquents

| Problème | Solution |
|---|---|
| `streamlit : commande introuvable` | Ouvrir **Anaconda Prompt** (pas PowerShell) |
| `File does not exist` | Vérifier le chemin du fichier `.py` |
| `KeyError` sur une colonne | Vérifier que les feuilles Excel sont bien nommées |
| Page blanche dans le navigateur | Attendre quelques secondes et rafraîchir |

---

## 👤 Projet

**PAPETIS DISTRIBUTION** — Contrôle de Gestion · Prototype MVP · 2025-2026
