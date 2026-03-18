# 📘 Guide Détaillé des Visualisations

Ce document explique en détail le fonctionnement, l'utilité scientifique et la logique technique de chaque graphique présent dans l'application **Sleep Analytics**.

---

## 📊 1. Qualité & Récupération

### 🟥 Structure des Nuits (Stacked Bar)
*   **Ce que c'est :** Un graphique en barres empilées montrant la composition de chaque nuit. Chaque couleur représente une phase : **Profond** (Bleu), **Léger** (Violet), **paradoxal/REM** (Rouge) et **Éveillé** (Jaune).
*   **L'intérêt Scientifique :** La durée totale ne suffit pas. Une nuit de 8h sans sommeil profond (récupération physique) ou sans REM (récupération mentale) est peu réparatrice.
*   **Fonctionnement Technique :** 
    *   On utilise `plotly.express.bar`.
    *   La ligne blanche pointillée représente votre **Moyenne** sur la période.
    *   La ligne verte tiretée représente votre **Objectif Durée** défini dans les réglages.

### 📈 Qualité : Sommeil Profond (%)
*   **Ce que c'est :** Une courbe montrant le pourcentage de temps passé en sommeil profond par rapport au temps total.
*   **L'intérêt Scientifique :** Le sommeil profond est crucial pour la régénération cellulaire, le système immunitaire et la production d'hormone de croissance. Un taux sain se situe généralement entre **15% et 20%**.
*   **Fonctionnement Technique :**
    *   Formule : `(Heures Profond / Heures Totales) * 100`.
    *   Une ligne verte indique votre cible (par défaut 20%).

### 📉 Ratio Profond vs REM
*   **Ce que c'est :** Une comparaison directe (deux courbes) entre la quantité de sommeil **Physique** (Profond) et **Mental** (REM).
*   **L'intérêt Scientifique :** Au début de la nuit, on fait plus de sommeil profond. En fin de nuit, plus de REM. Un déséquilibre peut indiquer du stress (moins de Profond) ou une dépression/privation (impact sur le REM).
*   **Fonctionnement Technique :**
    *   Les données sont restructurées (Melt) pour afficher deux séries temporelles sur le même axe Y.

### ⚡ Efficacité du Sommeil (%)
*   **Ce que c'est :** Le ratio entre le temps réellement dormi et le temps passé au lit.
*   **L'intérêt Scientifique :** Dormir 8h en restant 10h au lit signifie une efficacité de 80% (ce qui est moyen). Une bonne efficacité est supérieure à **85%**. Si elle est basse, cela indique des insomnies ou des réveils fréquents.
*   **Fonctionnement Technique :**
    *   Formule : `Temps Dormi / (Temps Dormi + Temps Éveillé)`.

### 🚧 Temps Éveillé (Agitation)
*   **Ce que c'est :** Un graphique en barres montrant le temps total passé éveillé *pendant* la nuit (micro-réveils ou insomnies).
*   **L'intérêt Scientifique :** Indique la fragmentation du sommeil. Un temps d'éveil élevé (> 1h) est un signe de sommeil de mauvaise qualité.

---

## 📆 Habitudes & Rythme

### ⏳ Régularité des Horaires (Timeline)
*   **Ce que c'est :** Un graphique de type "Gantt" ou "Timeline". Chaque barre horizontale représente une nuit, du début (coucher) à la fin (lever).
*   **L'intérêt Scientifique :** La régularité est aussi importante que la durée. Se coucher et se lever à des heures fixes ancre le rythme circadien (horloge biologique). Des barres décalées indiquent un "Jetlag social".
*   **Fonctionnement Technique :**
    *   Utilise `start_time` et `end_time`.
    *   La couleur de la barre change selon la durée totale de la nuit.

### 🆚 Semaine vs Week-end (Box Plot)
*   **Ce que c'est :** Une "boîte à moustaches" comparant la distribution de vos nuits en semaine (Lun-Ven) vs le Week-end (Sam-Dim).
*   **L'intérêt Scientifique :** Permet de voir si vous "rattrapez" le sommeil le week-end (dette accumulée) ou si vous décalez drastiquement vos horaires.
*   **Fonctionnement Technique :**
    *   Trie les données selon `dayofweek`.
    *   La boîte montre la médiane et les quartiles (où se situent 50% de vos nuits).

### 🕸️ Cycle Hebdomadaire (Radar)
*   **Ce que c'est :** Un graphique radar (l'araignée) montrant la durée moyenne pour chaque jour de la semaine (Lundi, Mardi...).
*   **L'intérêt Scientifique :** Identifie les jours "faibles". Par exemple, on dort souvent moins bien le Dimanche soir (stress de la reprise) ou le Vendredi (fatigue).

### 📍 Impact de l'Heure de Coucher (Corrélation)
*   **Ce que c'est :** Un nuage de points mettant en relation l'heure de coucher (Axe X) et la durée du sommeil (Axe Y).
*   **L'intérêt Scientifique :** Répond à la question : *"Est-ce que quand je me couche plus tôt, je dors vraiment plus ?"*. La ligne de tendance indique la relation.
*   **Fonctionnement Technique :**
    *   Les heures (ex: 23h30) sont converties en décimales (23.5) pour être placées sur le graphique.
    *   Les heures du petit matin (01h00) sont converties en "25h00" pour garder la continuité temporelle à droite du graphique.

### 📊 Distribution des Heures de Coucher
*   **Ce que c'est :** Un histogramme comptant combien de fois vous vous êtes couché à 22h, 23h, 00h, etc.
*   **L'intérêt Scientifique :** Montre votre "heure préférée" ou votre dispersion.

---

## 🔍 Vue d'Ensemble

### 📉 Dette de Sommeil Cumulée
*   **Ce que c'est :** Une courbe d'aire qui monte ou descend. C'est le compte bancaire de votre sommeil.
*   **L'intérêt Scientifique :** Si votre objectif est 8h et que vous dormez 7h, vous avez -1h de dette. Le lendemain, si vous dormez 7h, vous avez -2h cumulées. Une grande dette est liée à la baisse de performance cognitive.
*   **Fonctionnement Technique :**
    *   Calcul journalier : `Réel - Objectif`.
    *   Calcul cumulé : On somme ces écarts jour après jour (`cumsum()`).
    *   Si la courbe descend, vous accumulez de la fatigue. Si elle monte, vous récupérez.

### 🌊 Tendance Lissée (Moyenne Mobile)
*   **Ce que c'est :** Superpose votre durée réelle (points gris) et une courbe lissée sur 7 jours (ligne bleue épaisse).
*   **L'intérêt Scientifique :** Les données de sommeil sont très volatiles (une mauvaise nuit arrive). La moyenne mobile efface ce "bruit" pour montrer la vraie tendance (est-ce que je dors mieux globalement depuis 2 semaines ?).
*   **Fonctionnement Technique :**
    *   Chaque point de la ligne bleue est la moyenne de la nuit actuelle + des 3 nuits avant + des 3 nuits après.

### 🔥 Calendrier Heatmap
*   **Ce que c'est :** Une matrice colorée. Axe X = Semaines, Axe Y = Jours (Lundi...Dimanche). La couleur = Durée.
*   **L'intérêt Scientifique :** Permet de repérer des motifs visuels immédiats (ex: "Mes mardis sont toujours bleu clair, donc courts").
*   **Fonctionnement Technique :**
    *   Utilise un `pivot_table` Pandas pour transformer la liste de dates en grille [Semaine x Jour].

### 🥧 Répartition Globale
*   **Ce que c'est :** Un camembert (Pie Chart) sommant toutes les heures de toute la période.
*   **L'intérêt Scientifique :** Donne une vue macroscopique de votre architecture de sommeil sur le long terme.
