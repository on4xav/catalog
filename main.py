import os
import pandas as pd
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(page_title="Mon Catalogue Produits", layout="wide")

st.title("🕯️ Catalogue de Produits en Ligne")
st.write("Bienvenue sur notre catalogue. Retrouvez toutes nos références ci-dessous.")

# --- CHARGEMENT DES DONNÉES (CSV) ---
# Cette ligne est la plus robuste : elle cherche le fichier juste à côté du script main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "catalogue.csv")


@st.cache_data
def charger_donnees(chemin):
    """Fonction pour charger le fichier CSV de manière robuste."""
    if not os.path.exists(chemin):
        st.error(f"⚠️ Erreur : Le fichier CSV est introuvable ici : {chemin}")
        return None
    try:
        # On essaie d'abord de lire avec un point-virgule (standard Excel français)
        return pd.read_csv(chemin, sep=";")
    except Exception:
        try:
            # Si ça échoue, on essaie avec une virgule (standard international)
            return pd.read_csv(chemin, sep=",")
        except Exception as e:
            st.error(f"🚨 Erreur lors de la lecture du fichier CSV : {e}")
            return None


# Chargement du catalogue
df = charger_donnees(CSV_PATH)

if df is not None:
    # --- BARRE LATÉRALE (FILTRES) ---
    st.sidebar.header("Navigation")

    # Récupération unique des catégories
    categories = sorted(df["Catégorie"].dropna().unique())

    # Menu déroulant
    choix_categorie = st.sidebar.selectbox("Choisir une catégorie", categories)

    # Filtrer les produits
    produits_filtres = df[df["Catégorie"] == choix_categorie]

    st.header(f"Catégorie : {choix_categorie}")

    # --- AFFICHAGE DES ARTICLES ---
    if produits_filtres.empty:
        st.info("Aucun article disponible dans cette catégorie pour le moment.")
    else:
        for index, produit in produits_filtres.iterrows():
            st.markdown("---")
            col1, col2 = st.columns([1, 2])

            with col1:
                # Gestion de la photo
                lien_photo = produit["Photo"]
                if pd.isna(lien_photo) or str(lien_photo).strip() == "":
                    lien_photo = "https://placehold.co/300x300?text=Pas+d'image"

                try:
                    st.image(lien_photo, use_container_width=True)
                except Exception:
                    st.image(
                        "https://placehold.co/300x300?text=Erreur+Image",
                        use_container_width=True,
                    )

            with col2:
                st.subheader(produit["Nom"])
                st.markdown(
                    f"**Référence de commande :** `{produit['Référence']}`"
                )
                st.write(produit["Description"])
