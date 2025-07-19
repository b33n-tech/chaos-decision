import streamlit as st
import random

st.set_page_config(page_title="Simulateur de décision biaisée + invisibilisation", layout="wide")

# ----------- CLASSE SIMULATEUR ----------------
class DecisionAgent:
    def __init__(self, procrastination, pessimism, loss_aversion, scarcity, avoidance, pressure, invisibilisation):
        self.procrastination = procrastination
        self.pessimism = pessimism
        self.loss_aversion = loss_aversion
        self.scarcity = scarcity
        self.avoidance = avoidance
        self.pressure = pressure
        self.invisibilisation = invisibilisation

    def simulate(self):
        outcome = "indécision"
        decision_progress = 0
        time_elapsed = 0
        steps = []

        while outcome == "indécision" and time_elapsed < 12:
            time_elapsed += 1
            base_step = f"**Mois {time_elapsed}** : "

            # 1. Pessimisme bloque la projection
            if random.random() < self.pessimism / 15:
                steps.append(base_step + "vision négative → inertie.")
                continue

            # 2. Procrastination : report
            if random.random() < self.procrastination / 12:
                steps.append(base_step + "report de la décision.")
                continue

            # 3. Scarcity mindset : réduction du champ décisionnel
            if random.random() < self.scarcity / 12:
                steps.append(base_step + "réduction des options → statu quo.")
                continue

            # 4. Invisibilisation : actions ignorées ou sabotées
            if random.random() < self.invisibilisation / 15:
                decision_progress -= 1
                steps.append(base_step + "action invisible → sentiment d’inutilité.")
                continue

            if self.invisibilisation > 8 and random.random() < 0.5:
                steps.append(base_step + "auto-effacement → renoncement silencieux.")
                continue

            # 5. Pression extérieure déclenche parfois l’action
            if random.random() < self.pressure / 10:
                decision_progress += 3
                steps.append(base_step + "pression extérieure → tentative d’action.")
            else:
                decision_progress += 1
                steps.append(base_step + "réflexion / micro-action.")

            # 6. Aversion à la perte → doute après action
            if random.random() < self.loss_aversion / 15:
                decision_progress -= 1
                steps[-1] += " → doute post-action."

            # Check result
            if decision_progress >= 8:
                outcome = "succès"
            elif decision_progress <= -5:
                outcome = "échec"

        if time_elapsed >= 12 and outcome == "indécision":
            outcome = "report indéfini"

        return steps, outcome

# ----------- INTERFACE STREAMLIT --------------
st.title("🧠 Simulateur de prise de décision biaisée & invisibilisation")
st.markdown(
    "Ce simulateur génère des scénarios où la prise de décision est affectée par des biais cognitifs, émotionnels, "
    "et par la dynamique structurelle d’invisibilisation/invalidation."
)

with st.sidebar:
    st.header("🧩 Paramètres du profil")
    procrastination = st.slider("⏳ Procrastination", 0, 10, 5)
    pessimism = st.slider("🌧️ Vision pessimiste", 0, 10, 5)
    loss_aversion = st.slider("⚖️ Aversion à la perte", 0, 10, 5)
    scarcity = st.slider("🚪 Mentalité de rareté", 0, 10, 5)
    avoidance = st.slider("🙈 Évitement décisionnel", 0, 10, 5)
    pressure = st.slider("🔥 Pression extérieure", 0, 10, 5)
    invisibilisation = st.slider("👻 Invisibilisation structurelle", 0, 10, 5)

    if st.button("🎲 Lancer la simulation"):
        agent = DecisionAgent(
            procrastination=procrastination,
            pessimism=pessimism,
            loss_aversion=loss_aversion,
            scarcity=scarcity,
            avoidance=avoidance,
            pressure=pressure,
            invisibilisation=invisibilisation,
        )
        story, outcome = agent.simulate()

        st.session_state["story"] = story
        st.session_state["outcome"] = outcome

# ----------- AFFICHAGE DU RÉSULTAT --------------
if "story" in st.session_state:
    st.subheader("📜 Scénario simulé")
    for line in st.session_state["story"]:
        st.markdown(f"- {line}")

    st.subheader("🎯 Résultat final")
    emoji = {
        "succès": "✅",
        "échec": "❌",
        "report indéfini": "⏸️",
        "indécision": "🤷‍♂️"
    }
    result = st.session_state["outcome"]
    st.markdown(f"### {emoji.get(result, '')} **{result.upper()}**")
