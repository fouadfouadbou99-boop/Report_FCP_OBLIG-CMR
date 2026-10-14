def generate_commentary(kpis):

    perf = kpis["Performance Annualisée"]
    vol = kpis["Volatilité"]
    sharpe = kpis["Sharpe"]

    txt = f"""
Le fonds affiche une performance annualisée
de {perf:.2%}.

La volatilité ressort à {vol:.2%},
confirmant un profil de risque maîtrisé.

Le ratio de Sharpe s'établit à
{sharpe:.2f}.

Les indicateurs de risque demeurent
globalement conformes aux limites de gestion.

Une vigilance particulière devra être
maintenue sur l'évolution des taux afin
de limiter l'impact négatif lié à la
duration du portefeuille.
"""

    return txt
