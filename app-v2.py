import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title("🧠 Simulation d'Inertie Structurelle dans la Prise de Décision")

# Intro
st.markdown("""
Ce simulateur modélise les effets combinés de facteurs internes (psychiques), externes (matériels) et structurels (systémiques) sur l'inertie décisionnelle. Il ne s'agit pas de juger mais de **rendre visible les mécanismes d'érosion de la capacité à décider et agir**.
""")

# Inputs
st.header("🔧 Paramètres de simulation")

pessimism = st.slider("Pessimisme (0 = optimiste, 1 = catastrophisme permanent)", 0.0, 1.0, 0.5)
procrastination = st.slider("Procrastination / Évitement", 0.0, 1.0, 0.5)
loss_aversion = st.slider("Aversion à la perte (perdre 5 > gagner 10)", 0.0, 1.0, 0.5)
scarcity = st.slider("Mentalité de rareté (ressources, choix, temps...)", 0.0, 1.0, 0.5)
pressure = st.slider("Pression extérieure (sociale, économique...)", 0.0, 1.0, 0.5)
invisibilisation = st.slider("Invisibilisation / Invalidation structurelle", 0.0, 1.0, 0.5)

# Compute scores par axe
psychic = (pessimism + procrastination + loss_aversion) / 3
material = (scarcity + pressure) / 2
structural = invisibilisation

# Score global d'inertie (pondéré)
inertia_score = (psychic * 0.4 + material * 0.3 + structural * 0.3) * 100

# Interprétation
st.header("🧩 Résultat de la simulation")
st.metric("Score global d'inertie structurelle", f"{inertia_score:.1f} / 100")

if inertia_score < 30:
    st.success("🌱 Inertie faible : potentiel d'action élevé. Des leviers sont mobilisables.")
elif inertia_score < 60:
    st.warning("🌀 Inertie modérée : l'élan est là, mais fragilisé par certains freins clés.")
else:
    st.error("🧊 Inertie forte : le système décourage activement l'action et la décision.")

# Outcome suggestion (based on inertia score)
st.subheader("📊 Conséquence probable dans un contexte de décision")
if inertia_score < 30:
    outcome = "✅ Décision probable : audacieuse, proactive, structurée."
elif inertia_score < 60:
    outcome = "🕗 Décision reportée, fragmentée, voire sous-optimale."
else:
    outcome = "❌ Décision évitée, ou perçue comme inutile, voire auto-sabotée."

st.info(outcome)

# Diagramme radar
st.subheader("📈 Triangulation de l'inertie")

labels = ["Psychique", "Matériel", "Structurel"]
values = [psychic, material, structural]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
values += values[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.fill(angles, values, color='skyblue', alpha=0.6)
ax.plot(angles, values, color='blue', linewidth=2)
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_title("Radar de l'inertie structurelle", fontsize=14, pad=20)

st.pyplot(fig)
