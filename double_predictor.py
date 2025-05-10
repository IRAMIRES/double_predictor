import streamlit as st
from collections import Counter

# Lista de cores possíveis
CORES = ["vermelho", "preto", "branco"]

# Inicializar o histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Função para calcular a próxima cor provável
def prever_proxima_cor(historico, ultimas=15):
    if not historico:
        return "Sem dados", {cor: 1/3 for cor in CORES}

    ultimos = historico[-ultimas:]
    contagem = Counter(ultimos)
    total = sum(contagem.values())
    probabilidade = {cor: contagem.get(cor, 0) / total for cor in CORES}
    previsao = max(probabilidade, key=probabilidade.get)
    return previsao, probabilidade

# Interface do App
st.title("🎲 Previsor Simulado - Blaze Double")
st.markdown("Registre manualmente as cores que saíram e veja uma previsão com base no histórico.")

# Input do usuário
nova_cor = st.selectbox("Selecione a cor que saiu:", CORES)
if st.button("Registrar"):
    st.session_state.historico.append(nova_cor)
    st.success(f"Cor registrada: {nova_cor.upper()}")

# Exibir histórico
st.markdown("### 🧾 Últimos resultados:")
st.write(st.session_state.historico[-15:] or "Nenhum resultado registrado ainda.")

# Prever próxima cor
if st.session_state.historico:
    previsao, probs = prever_proxima_cor(st.session_state.historico)
    st.markdown("### 🔮 Previsão da próxima cor:")
    st.info(f"Provável próxima cor: **{previsao.upper()}**")

    st.markdown("### 📊 Probabilidades com base nas últimas jogadas:")
    for cor, prob in probs.items():
        st.write(f"**{cor.capitalize()}**: {prob*100:.2f}%")
