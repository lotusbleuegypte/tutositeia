
import streamlit as st
import speech_recognition as sr
import os
import tempfile
import requests
import base64
from gtts import gTTS
from PIL import Image
import io
from bs4 import BeautifulSoup
import docx
import PyPDF2
import json
import time

# Configuration de la page
st.set_page_config(
    page_title="🤖 Ma Plateforme IA Gratuite",
    page_icon="🚀",
    layout="wide"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .tool-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stApp {
        background: #f8f9fa;
    }
    .info-box {
        background: #e7f3ff;
        color: #0066cc;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# En-tête principal
st.markdown("""
<div class="main-header">
    <h1>🤖 Ma Plateforme IA Gratuite à Vie</h1>
    <p>Tous les outils IA dont tu as besoin, 100% gratuit, sans limite !</p>
</div>
""", unsafe_allow_html=True)

# Message d'information pour partager l'URL
st.markdown("""
<div class="info-box">
    <h3>📋 Partage cette application avec tes clients !</h3>
    <p>Cette URL est publique et gratuite à vie. Tes clients peuvent l'utiliser directement sans installation !</p>
</div>
""", unsafe_allow_html=True)

# Menu de navigation
tool_choice = st.sidebar.selectbox(
    "🛠️ Choisis ton outil IA :",
    ["🏠 Accueil", "🎤 Transcription Audio", "🔊 Synthèse Vocale", "📝 Extraction de Texte", "🖼️ Analyse d'Image", "🌐 Extracteur Web", "📊 Générateur de Contenu"]
)

# Fonctions pour chaque outil
def transcribe_audio(audio_file):
    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        text = r.recognize_google(audio, language='fr-FR')
        return text
    except Exception as e:
        return f"❌ Erreur lors de la transcription : {str(e)}"

def text_to_speech(text, lang='fr'):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.error(f"Erreur : {str(e)}")
        return None

def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"❌ Erreur lors de l'extraction : {str(e)}"

def extract_text_from_docx(docx_file):
    try:
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"❌ Erreur lors de l'extraction : {str(e)}"

def analyze_image(image):
    try:
        width, height = image.size
        format_img = image.format
        mode = image.mode
        
        analysis = f"""
📐 Dimensions : {width} x {height} pixels
📄 Format : {format_img}
🎨 Mode couleur : {mode}
📊 Ratio : {round(width/height, 2)}:1
💾 Taille estimée : {width * height} pixels totaux
        """
        return analysis
    except Exception as e:
        return f"❌ Erreur lors de l'analyse : {str(e)}"

def extract_web_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('title')
        title = title.get_text() if title else "Titre non trouvé"
        
        paragraphs = soup.find_all('p')
        content = "\n".join([p.get_text() for p in paragraphs[:5]])
        
        return f"📰 Titre : {title}\n\n📝 Contenu :\n{content}"
    except Exception as e:
        return f"❌ Erreur lors de l'extraction web : {str(e)}"

# Interface pour chaque outil
if tool_choice == "🏠 Accueil":
    st.markdown("""
    <div class="tool-card">
        <h2>Bienvenue sur ta plateforme IA gratuite ! 🎉</h2>
        <p>Utilise le menu à gauche pour choisir ton outil :</p>
        <ul>
            <li>🎤 <strong>Transcription Audio</strong> : Convertis tes fichiers audio en texte</li>
            <li>🔊 <strong>Synthèse Vocale</strong> : Transforme du texte en audio</li>
            <li>📝 <strong>Extraction de Texte</strong> : Récupère le texte de tes PDF/Word</li>
            <li>🖼️ <strong>Analyse d'Image</strong> : Analyse tes images</li>
            <li>🌐 <strong>Extracteur Web</strong> : Récupère le contenu d'un site web</li>
            <li>📊 <strong>Générateur de Contenu</strong> : Crée du contenu automatiquement</li>
        </ul>
        <h3>🚀 Comment partager avec tes clients :</h3>
        <p>1. Copie l'URL de cette page dans ton navigateur</p>
        <p>2. Partage cette URL avec tes clients</p>
        <p>3. Ils peuvent utiliser tous les outils gratuitement !</p>
    </div>
    """, unsafe_allow_html=True)

elif tool_choice == "🎤 Transcription Audio":
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.header("🎤 Transcription Audio Gratuite")
    st.write("Télécharge ton fichier audio et je le convertis en texte !")
    
    audio_file = st.file_uploader("Choisis ton fichier audio", type=['wav', 'mp3', 'flac', 'm4a'])
    
    if audio_file:
        st.info(f"📁 Fichier : {audio_file.name} ({audio_file.size} bytes)")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_file_path = tmp_file.name
        
        if st.button("🚀 Transcrire l'audio"):
            with st.spinner("Transcription en cours..."):
                result = transcribe_audio(tmp_file_path)
                st.markdown(f'<div class="success-message">✅ Transcription terminée !</div>', unsafe_allow_html=True)
                st.text_area("📝 Voici ton texte :", result, height=200)
        
        try:
            os.unlink(tmp_file_path)
        except:
            pass
    st.markdown('</div>', unsafe_allow_html=True)

elif tool_choice == "🔊 Synthèse Vocale":
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.header("🔊 Synthèse Vocale Gratuite")
    st.write("Écris ton texte et je le convertis en audio !")
    
    text_input = st.text_area("✍️ Écris ton texte ici :", height=100, max_chars=500)
    lang_choice = st.selectbox("🌍 Choisis la langue :", 
                              options=['fr', 'en', 'es', 'de', 'it'],
                              format_func=lambda x: {'fr': 'Français', 'en': 'Anglais', 'es': 'Espagnol', 'de': 'Allemand', 'it': 'Italien'}[x])
    
    if st.button("🎵 Générer l'audio") and text_input:
        with st.spinner("Génération audio en cours..."):
            audio_buffer = text_to_speech(text_input, lang_choice)
            if audio_buffer:
                st.markdown(f'<div class="success-message">✅ Audio généré !</div>', unsafe_allow_html=True)
                st.audio(audio_buffer.getvalue(), format='audio/mp3')
    st.markdown('</div>', unsafe_allow_html=True)

elif tool_choice == "📝 Extraction de Texte":
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.header("📝 Extraction de Texte Gratuite")
    st.write("Télécharge ton PDF ou document Word et je récupère le texte !")
    
    doc_file = st.file_uploader("Choisis ton document", type=['pdf', 'docx'])
    
    if doc_file:
        st.info(f"📁 Fichier : {doc_file.name} ({doc_file.size} bytes)")
        
        if st.button("📄 Extraire le texte"):
            with st.spinner("Extraction en cours..."):
                if doc_file.type == "application/pdf":
                    result = extract_text_from_pdf(doc_file)
                elif doc_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    result = extract_text_from_docx(doc_file)
                else:
                    result = "❌ Format de fichier non supporté"
                
                st.markdown(f'<div class="success-message">✅ Texte extrait !</div>', unsafe_allow_html=True)
                st.text_area("📝 Voici ton texte :", result, height=300)
    st.markdown('</div>', unsafe_allow_html=True)

elif tool_choice == "🖼️ Analyse d'Image":
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.header("🖼️ Analyse d'Image Gratuite")
    st.write("Télécharge ton image et je l'analyse pour toi !")
    
    image_file = st.file_uploader("Choisis ton image", type=['jpg', 'jpeg', 'png', 'gif', 'bmp'])
    
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Ton image", use_column_width=True)
        
        if st.button("🔍 Analyser l'image"):
            with st.spinner("Analyse en cours..."):
                result = analyze_image(image)
                st.markdown(f'<div class="success-message">✅ Analyse terminée !</div>', unsafe_allow_html=True)
                st.text_area("📊 Voici l'analyse :", result, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

elif tool_choice == "🌐 Extracteur Web":
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.header("🌐 Extracteur Web Gratuit")
    st.write("Donne-moi une URL et je récupère le contenu de la page !")
    
    url_input = st.text_input("🔗 Colle ton URL ici :", placeholder="https://exemple.com")
    
    if st.button("🌐 Extraire le contenu") and url_input:
        if not url_input.startswith(('http://', 'https://')):
            url_input = 'https://' + url_input
            
        with st.spinner("Extraction en cours..."):
            result = extract_web_content(url_input)
            st.markdown(f'<div class="success-message">✅ Contenu extrait !</div>', unsafe_allow_html=True)
            st.text_area("📝 Voici le contenu :", result, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

elif tool_choice == "📊 Générateur de Contenu":
    st.markdown('<div class="tool-card">', unsafe_allow_html=True)
    st.header("📊 Générateur de Contenu Gratuit")
    st.write("Génère du contenu automatiquement selon tes besoins !")
    
    content_type = st.selectbox("📝 Type de contenu :", 
                               ["Email professionnel", "Post LinkedIn", "Article de blog", "Description produit", "Communiqué de presse"])
    
    topic = st.text_input("💡 Sujet/Mots-clés :", placeholder="Ex: intelligence artificielle, marketing digital...")
    
    if st.button("✨ Générer le contenu") and topic:
        with st.spinner("Génération en cours..."):
            templates = {
                "Email professionnel": f"""
Objet : {topic.title()}

Bonjour,

J'espère que ce message vous trouve en bonne santé. Je vous contacte concernant {topic}.

Après réflexion sur ce sujet, je pense qu'il serait intéressant de discuter de cette opportunité plus en détail.

Les avantages que je vois :
• Impact positif sur votre activité
• Solution adaptée à vos besoins
• Résultats mesurables

Seriez-vous disponible pour un bref échange téléphonique cette semaine ?

Cordialement,
[Votre nom]
                """,
                "Post LinkedIn": f"""
🚀 {topic.title()} : Une opportunité à saisir !

Récemment, j'ai découvert l'importance croissante de {topic} dans notre secteur.

💡 Voici 3 points clés à retenir :
• Innovation et adaptation constante
• Collaboration entre équipes
• Focus sur les résultats concrets

🎯 Mon conseil : Commencez petit, testez rapidement, et adaptez-vous en continu.

Qu'en pensez-vous ? Partagez vos expériences en commentaire !

#business #innovation #croissance #{topic.replace(' ', '')}
                """,
                "Article de blog": f"""
# {topic.title()} : Guide Complet 2025

## Introduction

{topic.title()} est devenu un élément essentiel dans notre monde moderne. Dans cet article, nous explorerons les aspects fondamentaux de ce sujet passionnant.

## Les Points Essentiels

### 1. Comprendre les bases
La première étape consiste à maîtriser les concepts fondamentaux de {topic}. Cette compréhension vous donnera les clés pour réussir.

### 2. Mise en pratique
L'application concrète permet de consolider les connaissances théoriques. Commencez par de petits projets pour gagner en expérience.

### 3. Optimisation continue
L'amélioration constante est la clé du succès à long terme. Analysez vos résultats et adaptez votre approche.

## Conseils Pratiques

• Restez informé des dernières tendances
• Échangez avec d'autres professionnels
• Testez régulièrement de nouvelles approches
• Mesurez vos résultats

## Conclusion

{topic.title()} offre de nombreuses opportunités pour ceux qui s'y intéressent sérieusement. L'avenir appartient à ceux qui osent innover.
                """,
                "Description produit": f"""
🌟 {topic.title()} - La Solution Parfaite

✅ Caractéristiques principales :
• Qualité supérieure garantie
• Facilité d'utilisation remarquable
• Résultats rapides et durables
• Support technique inclus

🎯 Parfait pour :
• Professionnels exigeants
• Usage quotidien intensif
• Projets spéciaux et créatifs
• Équipes de toute taille

💡 Pourquoi choisir notre solution ?
Parce qu'elle combine performance exceptionnelle et fiabilité éprouvée pour répondre à tous vos besoins en matière de {topic}.

🚀 Commandez maintenant et découvrez la différence !

📞 Contact : [Votre contact]
                """,
                "Communiqué de presse": f"""
COMMUNIQUÉ DE PRESSE

[Date] - [Ville]

Nouvelle Avancée dans le Domaine de {topic.title()}

[Votre Entreprise] annonce aujourd'hui une innovation majeure concernant {topic}, marquant une étape importante dans ce secteur en pleine évolution.

Cette nouvelle approche permettra de :
• Améliorer l'efficacité des processus
• Réduire les coûts opérationnels
• Optimiser l'expérience utilisateur

"Cette innovation représente l'avenir de {topic}", déclare [Nom], [Titre] de [Votre Entreprise]. "Nous sommes fiers de contribuer à faire avancer ce domaine."

À propos de [Votre Entreprise] :
[Description de votre entreprise]

Contact Presse :
[Vos coordonnées]
                """
            }
            
            result = templates[content_type]
            st.markdown(f'<div class="success-message">✅ Contenu généré !</div>', unsafe_allow_html=True)
            st.text_area("📝 Voici ton contenu :", result, height=400)
            
            # Bouton de téléchargement
            st.download_button(
                label="💾 Télécharger le contenu",
                data=result,
                file_name=f"{content_type.replace(' ', '_')}_{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style="text-align: center; padding: 2rem; color: #666;">
    🚀 Plateforme IA Gratuite à Vie - Créée avec ❤️ par ton ingénieur IA personnel<br>
    📋 Partage cette URL avec tes clients pour qu'ils profitent aussi de ces outils gratuits !
</div>
""", unsafe_allow_html=True)
