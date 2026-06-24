import os
import pandas as pd
import streamlit as st

# Configuration de la page Streamlit (Largeur maximale)
st.set_page_config(page_title="Mon Catalogue Produits", layout="wide")

st.title("Mon Catalogue de Produits en Ligne 🕯️")
st.write(
    "Bienvenue sur le catalogue. Utilisez le menu de gauche pour naviguer entre les catégories."
)

# --- CONFIGURATION GOOGLE DRIVE ---
# Collez votre lien de partage Google Drive ou Google Sheets ci-dessous
# ASSUREZ-VOUS QUE LE PARTAGE EST SUR "Tous les utilisateurs disposant du lien"
LIEN_GOOGLE_DRIVE = "https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J/edit?usp=sharing"


@st.cache_data
def obtenir_lien_direct_drive(lien_partage):
    """Transforme un lien Google Drive (Fichier ou Sheets) en lien de téléchargement direct CSV."""
    try:
        # Cas 1 : C'est un vrai Google Sheets (icône verte)
        if "/spreadsheets/d/" in lien_partage:
            id_fichier = lien_partage.split("/spreadsheets/d/")[1].split("/")[0]
            return f"https://docs.google.com/spreadsheets/d/{id_fichier}/export?format=csv"

        # Cas 2 : C'est un fichier CSV brut stocké sur le Drive (icône grise)
        elif "/file/d/" in lien_partage:
            id_fichier = lien_partage.split("/file/d/")[1].split("/")[0]
            return f"https://docs.google.com/uc?export=download&id={id_fichier}"

    except Exception as e:
        st.error(f"Erreur lors de la configuration du lien Google Drive : {e}")
    return lien_partage


@st.cache_data
def charger_donnees(url_drive):
    """Fonction pour charger le CSV directement depuis Google Drive."""
    url_direct = obtenir_lien_direct_drive(url_drive)
    try:
        # Lecture du CSV depuis l'URL Google Drive
        # Par défaut, Google Drive exporte avec des virgules (",")
        return pd.read_csv(url_direct, sep=",")
    except Exception:
        try:
            # Sécurité au cas où le séparateur exporté serait un point-virgule (";")
            return pd.read_csv(url_direct, sep=";")
        except Exception as e:
            st.error(
                f"🚨 Impossible de lire le fichier depuis Google Drive."
                f"Vérifiez que le fichier est bien partagé en mode 'Lecteur public'. Erreur : {e}"
            )
            return None


# Chargement du catalogue depuis Google Drive
df = charger_donnees(LIEN_GOOGLE_DRIVE)

if df is not None:
    # --- BARRE LATÉRALE (FILTRES) ---
    st.sidebar.header("Navigation")

    # Récupération unique des catégories (on nettoie les lignes vides)
    categories = sorted(df["Catégorie"].dropna().unique())

    if not categories:
        st.warning(
            "Aucune catégorie trouvée. Vérifiez l'en-tête de votre fichier (Nom, Catégorie, etc.)."
        )
    else:
        # Menu déroulant pour choisir la catégorie
        choix_categorie = st.sidebar.selectbox(
            "Choisir une catégorie", categories
        )

        # Filtrer les produits selon la catégorie
        produits_filtres = df[df["Catégorie"] == choix_categorie]

        st.header(f"Catégorie : {choix_categorie}")

        # --- AFFICHAGE DES ARTICLES ---
        if produits_filtres.empty:
            st.info(
                "Aucun article disponible dans cette catégorie pour le moment."
            )
        else:
            for index, produit in produits_filtres.iterrows():
                st.markdown("---")

                # Structure en 2 colonnes (1/3 image, 2/3 texte)
                col1, col2 = st.columns([1, 2])

                with col1:
                    # Gestion de la photo
                    lien_photo = produit["Photo"]
                    if pd.isna(lien_photo) or str(lien_photo).strip() == "":
                        lien_photo = (
                            "https://placehold.co/300x300?text=Pas+d'image"
                        )

                    try:
                        st.image(lien_photo, use_container_width=True)
                    except Exception:
                        st.image(
                            "https://placehold.co/300x300?text=Erreur+Image",
                            use_container_width=True,
                        )

                with col2:
                    # Informations de l'article
                    st.subheader(produit["Nom"])
                    st.markdown(
                        f"**Référence de commande :** `{produit['Référence']}`"
                    )
                    st.write(produit["Description"])
