import streamlit as st
import math

# 1. Seiten-Konfiguration
st.set_page_config(page_title="Margareten Erwerbungs-Master V7", page_icon="📚", layout="wide")

st.title("📚 Margareten Erwerbungs-Master V7")
st.markdown("Das intelligente Bestandsmanagement für die Zweigstelle 05.")
st.divider()

# 2. Modus-Wahl
st.subheader("1. Vorgang auswählen")
modus = st.radio(
    "Handelt es sich um eine Übernahme aus Beständen/Spenden oder um einen Neuankauf?",
    ["Spende / Übernahme (SPE)", "Ankauf / Auswahlliste (AL)"],
    horizontal=True
)

st.divider()

# 3. Layout in Spalten aufteilen
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Stammdaten")
    isbn = st.text_input("ISBN eingeben:", "9783552075290")
    
    # Simulierter Fetch für das Beispiel
    titel = st.text_input("Titel", value="Warte im Schnee vor Deiner Tür")
    autor = st.text_input("Autor", value="Friedl Benedikt")
    verlag = st.text_input("Verlag", value="Zsolnay")
    neupreis = st.number_input("Neupreis (€)", value=26.00, step=0.5)

    st.markdown("---")
    st.subheader("📊 System-Performance (BIBLIOTHECAplus)")
    st.markdown("*(Werte aus der Katalog-Recherche übernehmen)*")
    
    gesamt = st.number_input("Ausleihen Gesamt", value=9, min_value=0)
    jahr = st.number_input("Ausleihen laufendes Jahr", value=2, min_value=0)
    vorjahr = st.number_input("Ausleihen Vorjahr", value=7, min_value=0)
    vorbestellungen = st.number_input("Aktuelle Vorbestellungen", value=0, min_value=0)

with col2:
    st.subheader("🧠 Margareten-Gehirn")
    if "SPE" in modus:
        st.success("💡 Modus: Spende. Ein hoher Neupreis bringt Pluspunkte (Budget-Ersparnis). Hohe Gesamt-Ausleihen zeigen Beliebtheit, ab 20 greift aber ein Verschleiß-Malus.")
    else:
        st.warning("⚠️ Modus: Ankauf (AL). Ein hoher Neupreis kostet Punkte (Budget-Belastung). Vorbestellungen im System zählen doppelt!")
        
    st.markdown("**Manuelle Qualitäts-Einschätzung:**")
    themen_fit = st.slider("Themen-Fit Margareten", 0, 20, 16)
    langfristig = st.slider("Langfristige Ausleih-Probabilität", 0, 20, 12)
    echo = st.slider("Literarisches Echo / Reviews", 0, 10, 8)

st.divider()

# 4. Die V7 Berechnungs-Logik
raw_score = 0
raw_score += themen_fit + langfristig + echo

# Katalog-Bonus (Wie gut lief das Buch zuletzt?)
avg_loans = (jahr + vorjahr) / 2
if avg_loans > 5:
    raw_score += 15
elif avg_loans > 2:
    raw_score += 8

# Modus-spezifische Berechnung
if "SPE" in modus:
    # Budget-Ersparnis ist positiv
    raw_score += min(15, neupreis * 0.4)
    # Bewiesene Beliebtheit vs. Verschleiß
    if gesamt > 5:
        raw_score += 5
    if gesamt > 20:
        raw_score -= 10 # Abnutzung
else:
    # Budget-Belastung ist negativ
    raw_score -= min(12, neupreis * 0.3)
    # Hype-Faktor Vorbestellungen (Extrem wichtig bei Neukauf)
    raw_score += (vorbestellungen * 6)

# Finaler Optimismus-Faktor (15%) und Deckelung
final_score = int(round(raw_score * 1.15))
final_score = max(0, min(100, final_score))

# 5. Ergebnis-Anzeige
st.subheader("Ergebnis: Margareten-Score")

if final_score >= 80:
    st.success(f"🏆 TOP-PRIORITÄT | Score: {final_score} / 100")
elif final_score >= 65:
    st.info(f"✅ EMPFEHLUNG | Score: {final_score} / 100")
else:
    st.error(f"🛑 ZURÜCKSTELLEN | Score: {final_score} / 100")

# Visueller Balken
st.progress(final_score / 100.0)
