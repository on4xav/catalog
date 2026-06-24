import os
import pandas as pd
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(page_title="Mon Catalogue Produits", layout="wide")

st.title("🕯️ Catalogue de Produits en Ligne")
st.write("Bienvenue sur notre catalogue. Retrouvez toutes nos références ci-dessous.")

# --- CHARGEMENT DES DONNÉES (GOOGLE DRIVE) ---
# REMPLACEZ LE LIEN CI-DESSOUS PAR VOTRE LIEN GOOGLE DRIVE COPIÉ
LIEN_GOOGLE_DRIVE = "https://drive.google.com/file/d/1UhleUeHIKmFjsGXFRqahqpgj4Cklb4Fz/view?usp=sharing"


@st.cache_data
def obtenir_lien_direct_drive(lien_partage):
    """Transforme un lien de partage Google Drive en lien de téléchargement direct."""
    try:
        if "/file/d/" in lien_partage:
            id_fichier = lien_partage.split("/file/d/")[1].split("/")[0]
            return f"https://docs.google.com/spreadsheets/d/{id_fichier}/export?format=csv"
    except Exception as e:
        st.error(f"Erreur lors de la configuration du lien Google Drive : {e}")
    return lien_partage


@st.cache_data
def charger_donnees(url_drive):
    """Fonction pour charger le CSV directement depuis Google Drive."""
    url_direct = obtenir_lien_direct_drive(url_drive)
    try:
        # Lecture du CSV depuis l'URL Google Drive
        # Note : Google Drive exporte par défaut avec des virgules (",")
        return pd.read_csv(url_direct, sep=",")
    except Exception:
        try:
            # Sécurité au cas où le séparateur serait un point-virgule
            return pd.read_csv(url_direct, sep=";")
        except Exception as e:
            st.error(
                f"🚨 Impossible de lire le fichier depuis Google Drive. Vérifiez le partage du lien. Erreur : {e}"
            )
            return None


# Chargement du catalogue depuis Google Drive
df = charger_donnees(LIEN_GOOGLE_DRIVE)

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
