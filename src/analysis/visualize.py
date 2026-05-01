import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns

sns.set_theme(style="darkgrid")

PALETTE_CAS = {
    "Flop":           "#e74c3c",
    "Post-franchise": "#f39c12",
    "Disparu":        "#9b59b6",
    "Declin":         "#3498db",
}

PALETTE_STATUT = {
    "Avant pic":      "#2ecc71",
    "Pic":            "#f1c40f",
    "Post-pic récent":"#e67e22",
    "Déclin":         "#e74c3c",
}

COULEUR_PRINCIPALE = "#e74c3c"
COULEUR_SECONDAIRE = "#3498db"


def plot_evolution_carriere(df: pd.DataFrame, personne: str) -> plt.Figure:
    data = df[df["personne"] == personne].groupby("annee").agg(
        note_moyenne=("note_tmdb", "mean")
    ).reset_index()

    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")
    ax.plot(data["annee"], data["note_moyenne"], marker="o", linewidth=2.5,
            color=COULEUR_PRINCIPALE, markerfacecolor="#f39c12", markersize=7)
    ax.set_title(f"Évolution de la note moyenne — {personne}", color="white", fontsize=13)
    ax.set_xlabel("Année", color="white")
    ax.set_ylabel("Note TMDB", color="white")
    ax.set_ylim(0, 10)
    ax.tick_params(colors="white")
    ax.spines["bottom"].set_color("#444")
    ax.spines["left"].set_color("#444")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    return fig


def plot_note_par_statut(df: pd.DataFrame) -> plt.Figure:
    ordre = ["Avant pic", "Pic", "Post-pic récent", "Déclin"]
    agg = df.groupby("statut_carriere")["note_tmdb"].mean().reset_index()
    agg["statut_carriere"] = pd.Categorical(agg["statut_carriere"], categories=ordre, ordered=True)
    agg = agg.sort_values("statut_carriere")
    couleurs = [PALETTE_STATUT.get(s, "#aaa") for s in agg["statut_carriere"]]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")
    bars = ax.bar(agg["statut_carriere"], agg["note_tmdb"], color=couleurs, edgecolor="#222", linewidth=0.5)
    ax.set_title("Note moyenne par statut de carrière", color="white", fontsize=13)
    ax.set_xlabel("", color="white")
    ax.set_ylabel("Note TMDB moyenne", color="white")
    ax.set_ylim(0, 10)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("#444")
    plt.tight_layout()
    return fig


def plot_films_par_cas(df: pd.DataFrame) -> plt.Figure:
    agg = df.groupby("cas")["film"].count().reset_index()
    agg.columns = ["cas", "nb_films"]
    agg = agg.sort_values("nb_films", ascending=False)
    couleurs = [PALETTE_CAS.get(c, "#aaa") for c in agg["cas"]]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")
    ax.bar(agg["cas"], agg["nb_films"], color=couleurs, edgecolor="#222", linewidth=0.5)
    ax.set_title("Nombre de films par type de cas", color="white", fontsize=13)
    ax.set_xlabel("", color="white")
    ax.set_ylabel("Nombre de films", color="white")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("#444")
    plt.tight_layout()
    return fig


def plot_comparaison_personnes(df: pd.DataFrame) -> plt.Figure:
    agg = df.groupby("personne")["note_tmdb"].mean().reset_index()
    agg = agg.sort_values("note_tmdb", ascending=False)

    cmap = plt.cm.RdYlGn
    norm = mcolors.Normalize(vmin=agg["note_tmdb"].min(), vmax=agg["note_tmdb"].max())
    couleurs = [cmap(norm(v)) for v in agg["note_tmdb"]]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")
    ax.barh(agg["personne"], agg["note_tmdb"], color=couleurs, edgecolor="#222", linewidth=0.5)
    ax.set_title("Note TMDB moyenne par personne", color="white", fontsize=13)
    ax.set_xlabel("Note moyenne", color="white")
    ax.set_ylabel("", color="white")
    ax.set_xlim(0, 10)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("#444")
    plt.tight_layout()
    return fig


def plot_decennie(df: pd.DataFrame) -> plt.Figure:
    agg = df.groupby("decennie").agg(
        nb_films=("film", "count"),
        note_moyenne=("note_tmdb", "mean")
    ).reset_index().sort_values("decennie")

    fig, ax1 = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#1a1a2e")
    ax1.set_facecolor("#16213e")
    ax2 = ax1.twinx()
    ax1.bar(agg["decennie"], agg["nb_films"], color=COULEUR_SECONDAIRE, alpha=0.8, label="Nb films")
    ax2.plot(agg["decennie"], agg["note_moyenne"], marker="o", color=COULEUR_PRINCIPALE,
             linewidth=2.5, markersize=7, label="Note moyenne")
    ax1.set_title("Films et note moyenne par décennie", color="white", fontsize=13)
    ax1.set_ylabel("Nombre de films", color=COULEUR_SECONDAIRE)
    ax2.set_ylabel("Note TMDB moyenne", color=COULEUR_PRINCIPALE)
    ax1.tick_params(colors="white")
    ax2.tick_params(colors="white")
    ax1.legend(loc="upper left", facecolor="#222", labelcolor="white")
    ax2.legend(loc="upper right", facecolor="#222", labelcolor="white")
    for spine in ax1.spines.values():
        spine.set_color("#444")
    plt.tight_layout()
    return fig


def plot_scatter_note_annee(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")
    for cas, color in PALETTE_CAS.items():
        subset = df[df["cas"] == cas]
        ax.scatter(subset["annee"], subset["note_tmdb"],
                   color=color, alpha=0.7, s=50, label=cas, edgecolors="none")
    ax.set_title("Notes TMDB dans le temps par type de cas", color="white", fontsize=13)
    ax.set_xlabel("Année", color="white")
    ax.set_ylabel("Note TMDB", color="white")
    ax.tick_params(colors="white")
    ax.legend(facecolor="#222", labelcolor="white")
    for spine in ax.spines.values():
        spine.set_color("#444")
    plt.tight_layout()
    return fig