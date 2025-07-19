import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Simulateur avancé d'inertie structurelle", layout="wide")

class DecisionAgent:
    def __init__(self, procrastination, pessimism, loss_aversion, scarcity, avoidance, pressure, invisibilisation, visibilite_coulisses):
        self.procrastination = procrastination
        self.pessimism = pessimism
        self.loss_aversion = loss_aversion
        self.scarcity = scarcity
        self.avoidance = avoidance
        self.pressure = pressure
        self.invisibilisation = invisibilisation
        self.visibilite_coulisses = visibilite_coulisses

    def simulate(self):
        outcome = "indécision"
        decision_progress = 0
        time_elapsed = 0
        steps = []
        progress_history = []

        while outcome == "indécision" and time_elapsed < 12:
            time_elapsed += 1
            base_step = f"Mois {time_elapsed} : "

            # Pessimisme bloque la projection
            if random.random() < self.pessimism / 15:
                steps.append(base_step + "vision négative → inertie.")
                progress_history.append(decision_progress)
                continue

            # Procrastination : report
            if random.random() < self.procrastination / 12:
                steps.append(base_step + "report de la décision.")
                progress_history.append(decision_progress)
                continue

            # Scarcity mindset : réduction du champ décisionnel
            if random.random() < self.scarcity / 12:
                steps.append(base_step + "réduction des options → statu quo.")
                progress_history.append(decision_progress)
                continue

            # Invisibilisation : actions ignorées ou sabotées
            if random.random() < self.invisibilisation / 15:
                decision_progress -= 1
                steps.append(base_step + "action invisible → sentiment d’inutilité.")
                progress_history.append(decision_progress)
                continue

            # Auto-effacement si invisibilisation forte
            if self.invisibilisation > 8 and random.random() < 0.5:
                steps.append(base_step + "auto-effacement → renoncement silencieux.")
                progress_history.append(decision_progress)
                continue

            # Pression extérieure déclenche parfois l’action
            if random.random() < self.pressure / 10:
                decision_progress += 3
                steps.append(base_step + "pression extérieure → tentative d’action.")
            else:
                decision_progress += 1
                steps.append(base_step + "réflexion / micro-action.")

            # Aversion à la perte → doute après action
            if random.random() < self.loss_aversion / 15:
                decision_progress -= 1
                steps[-1] += " → doute post-action."

            progress_history.append(decision_progress)

            # Check résultat
            if decision_progress >= 8:
                outcome = "succès"
            elif decision_progress <= -5:
                outcome = "échec"

        if time_elapsed >= 12 and outcome == "indécision":
            outcome = "report indéfini"

        return steps, outcome, progress_history

    def calculate_inertia_score(self):
        # Score cognitif
        score_cognitif = (self.procrastination + self.pessimism + self.loss_aversion + self.avoidance) * 2.5
        # Score conjoncturel (pressure inverse)
        score_conjoncturel = (self.scarcity + (10 - self.pressure)) * 5
        # Score structurel
        score_structurel = self.invisibilisation * 10

        # Effet amplificateur de la visibilité : moins on voit, plus l'inertie structurelle augmente
        # On définit un facteur multiplicateur de 1 (transparence totale) à 1.5 (opaque)
        amplificateur_visibilite = 1 + (10 - self.visibilite_coulisses) * 0.05

        # Application du multiplicateur sur la somme des scores
        total_brut = score_cognitif + score_conjoncturel + score_structurel
        total = total_brut * amplificateur_visibilite

        return {
            "cognitif": score_cognitif,
            "conjoncturel": score_conjoncturel,
            "structurel": score_structurel,
            "total_brut": total_brut,
            "total": total,
            "amplificateur_visibilite": amplificateur_visibilite
        }


st.title("🧠 Simulateur avancé d'inertie structurelle avec visibilité interne")

st.markdown("""
Ce simulateur modélise l’impact combiné de biais cognitifs, contextuels, invisibilisation structurelle et visibilité des coulisses sur la prise de décision.
""")

with st.sidebar:
    st.header("🔧 Paramètres du profil")
    procrastination = st.slider("⏳ Procrastination", 0, 10, 5)
    pessimism = st.slider("🌧️ Vision pessimiste", 0, 10, 5)
    loss_aversion = st.slider("⚖️ Aversion à la perte", 0, 10, 5)
    scarcity = st.slider("🚪 Mentalité de rareté", 0, 10, 5)
    avoidance = st.slider("🙈 Évitement décisionnel", 0, 10, 5)
    pressure = st.slider("🔥 Pression extérieure", 0, 10, 5)
    invisibilisation = st.slider("👻 Invisibilisation structurelle", 0, 10, 5)
    visibilite_coulisses = st.slider("🔍 Visibilité sur les coulisses (transparence interne)", 0, 10, 5)

    if st.button("🎲 Lancer la simulation"):
        agent = DecisionAgent(
            procrastination,
            pessimism,
            loss_aversion,
            scarcity,
            avoidance,
            pressure,
            invisibilisation,
            visibilite_coulisses
        )
        story, outcome, progress_history = agent.simulate()
        inertia_scores = agent.calculate_inertia_score()

        st.session_state["story"] = story
        st.session_state["outcome"] = outcome
        st.session_state["progress_history"] = progress_history
        st.session_state["inertia_scores"] = inertia_scores
        st.session_state["visibilite_coulisses"] = visibilite_coulisses

if "story" in st.session_state:
    st.subheader("📜 Scénario simulé mois par mois")
    for line in st.session_state["story"]:
        st.markdown(f"- {line}")

    st.subheader("🎯 Résultat final")
    emoji = {
        "succès": "✅",
        "échec": "❌",
        "report indéfini": "⏸️",
        "indécision": "🤷‍♂️"
    }
    st.markdown(f"### {emoji.get(st.session_state['outcome'], '')} **{st.session_state['outcome'].upper()}**")

    st.subheader("🧭 Score d'inertie structurelle")
    s = st.session_state["inertia_scores"]
    ampl = s["amplificateur_visibilite"]
    st.markdown(f"""
    - Cognitif : **{s['cognitif']:.1f} / 100**  
    - Conjoncturel : **{s['conjoncturel']:.1f} / 100**  
    - Structurel : **{s['structurel']:.1f} / 100**  
    - Score brut : **{s['total_brut']:.1f}**  
    - Amplificateur visibilité : **{ampl:.2f}** (1 = transparence totale, 1.5 = opaque)  
    - **Score total corrigé : {s['total']:.1f}** (prise en compte visibilité)  
    """)

    # Interprétation du score total corrigé
    total_corrige = s["total"]
    st.subheader("💡 Interprétation du score total corrigé")
    if total_corrige < 120:
        st.success("🌱 Faible inertie : dynamique activable, leviers d’action possibles.")
    elif total_corrige < 180:
        st.warning("🌀 Inertie modérée : effort coûteux, vigilance nécessaire.")
    elif total_corrige < 240:
        st.error("🧊 Inertie significative : blocages structurels notables.")
    else:
        st.error("🛑 Blocage structurel majeur : le système décourage fortement l’action.")

    # Diagramme radar
    st.subheader("📈 Triangulation de l'inertie (psychique, matériel, structurel)")
    labels = ['Cognitif', 'Conjoncturel', 'Structurel']
    values = [s['cognitif'], s['conjoncturel'], s['structurel']]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='skyblue', alpha=0.7)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Radar de l'inertie structurelle", fontsize=14, pad=20)
    st.pyplot(fig)

    # Frise chronologique de la progression décisionnelle
    st.subheader("📅 Frise chronologique de la progression décisionnelle")

    progress = st.session_state["progress_history"]
    months = list(range(1, len(progress)+1))

    fig2, ax2 = plt.subplots(figsize=(10,3))
    ax2.plot(months, progress, marker='o', color='tab:green')
    ax2.axhline(y=8, color='tab:blue', linestyle='--', label="Seuil succès")
    ax2.axhline(y=-5, color='tab:red', linestyle='--', label="Seuil échec")
    ax2.set_xlabel("Mois")
    ax2.set_ylabel("Progression décisionnelle")
    ax2.set_xticks(months)
    ax2.set_ylim(min(progress)-1, max(progress)+1)
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
