import os
import pandas as pd
import streamlit as st

# Configuration de la page Streamlit (Largeur max pour un effet catalogue)
st.set_page_config(page_title="Mon Catalogue Produits", layout="wide")

st.title("🕯️ Catalogue de Produits en Ligne")
st.write("Bienvenue sur notre catalogue. Retrouvez toutes nos références ci-dessous.")

# --- CHARGEMENT DES DONNÉES ---
# Cette ligne trouve automatiquement le dossier actuel du script, sur Windows ou sur GitHub
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "catalogue.xlsx")


@st.cache_data
def charger_donnees(chemin):
    """Fonction pour charger le fichier Excel de manière optimisée."""
    if not os.path.exists(chemin):
        st.error(f"⚠️ Erreur : Le fichier spécifié est introuvable au chemin : {chemin}")
        return None
    try:
        # Charge le fichier Excel
        return pd.read_excel(chemin)
    except Exception as e:
        st.error(f"🚨 Erreur lors de la lecture du fichier Excel : {e}")
        return None


# Chargement effectif du catalogue
df = charger_donnees(EXCEL_PATH)

if df is not None:
    # --- BARRE LATÉRALE (FILTRES) ---
    st.sidebar.header("Navigation")

    # Récupération unique des catégories (et tri par ordre alphabétique)
    categories = sorted(df["Catégorie"].dropna().unique())

    # Menu déroulant pour choisir la catégorie
    choix_categorie = st.sidebar.selectbox("Choisir une catégorie", categories)

    # Filtrer le DataFrame selon la catégorie choisie
    produits_filtres = df[df["Catégorie"] == choix_categorie]

    # Affichage du titre de la catégorie actuelle
    st.header(f"Catégorie : {choix_categorie}")

    # --- AFFICHAGE DES ARTICLES ---
    if produits_filtres.empty:
        st.info("Aucun article disponible dans cette catégorie pour le moment.")
    else:
        for index, produit in produits_filtres.iterrows():
            # Création d'une ligne de séparation visuelle entre chaque article
            st.markdown("---")

            # Séparation de la fiche en deux colonnes (1/3 pour la photo, 2/3 pour le texte)
            col1, col2 = st.columns([1, 2])

            with col1:
                # Gestion de la photo (URL ou fichier local)
                lien_photo = produit["Photo"]
                # Si la case est vide dans Excel, on met une image par défaut
                if pd.isna(lien_photo) or str(lien_photo).strip() == "":
                    lien_photo = "https://placehold.co/300x300?text=Pas+d'image"

                try:
                    st.image(lien_photo, use_container_width=True)
                except Exception:
                    # Sécurité si le lien de la photo est mort ou introuvable
                    st.image(
                        "https://placehold.co/300x300?text=Erreur+Image",
                        use_container_width=True,
                    )

            with col2:
                # Informations textuelles du produit
                st.subheader(produit["Nom"])
                st.markdown(
                    f"**Référence de commande :** `{produit['Référence']}`"
                )
                st.write(produit["Description"])
