import streamlit as st
from collections import Counter

CORES = ["vermelho", "preto", "branco"]

if "historico" not in st.session_state:
    st.session_state.historico = []

def prever_proxima_cor(historico, ultimas=15):
    if not historico:
        return "Sem dados", {cor: 1/3 for cor in CORES}

    ultimos = historico[-ultimas:]
    contagem = Counter(ultimos)
    total = sum(contagem.values())
    probabilidade = {cor: contagem.get(cor, 0) / total for cor in CORES}
    previsao = max(probabilidade, key=probabilidade.get)
    return previsao, probabilidade

def analisar_sequencias(historico):
    if len(historico) < 2:
        return [], {}
    
    # Ex: ['vermelho', 'preto', 'vermelho'] => [('vermelho','preto'), ('preto','vermelho')]
    sequencias = [(historico[i], historico[i+1]) for i in range(len(historico)-1)]
    contagem_sequencias = Counter(sequencias)
    return sequencias, contagem_sequencias

def contar_repeticoes(historico):
    if not historico:
        return 0, ""
    
    ultima = historico[-1]
    cont = 1
    for i in range(len(historico)-2, -1, -1):
        if historico[i] == ultima:
            cont += 1
        else:
            break
    return cont, ultima

# Interface principal
st.title("🎯 Blaze Double - Analisador de Cores")
st.markdown("Registre as cores e veja previsões, padrões e estatísticas.")

# Interface de registro
col1, col2, col3 = st.columns(3)
with col1:
    nova_cor = st.selectbox("Selecione a cor que saiu:", CORES)

with col2:
    if st.button("Registrar"):
        st.session_state.historico.append(nova_cor)
        st.success(f"Cor registrada: {nova_cor.upper()}")

with col3:
    if st.button("❌ Desfazer última cor"):
        if st.session_state.historico:
            removida = st.session_state.historico.pop()
            st.warning(f"Removida: {removida.upper()}")
        else:
            st.info("Nada para desfazer.")

# Resetar histórico
if st.button("🔁 Resetar histórico"):
    st.session_state.historico.clear()
    st.info("Histórico apagado!")

# Mostrar histórico
st.markdown("### 🧾 Histórico:")
st.write(st.session_state.historico[-15:] or "Sem registros ainda.")

# Análise de padrões
if st.session_state.historico:
    # Previsão
    previsao, probs = prever_proxima_cor(st.session_state.historico)
    st.markdown("### 🔮 Previsão da próxima cor:")
    st.info(f"Mais provável: **{previsao.upper()}**")

    st.markdown("### 📊 Probabilidades baseadas nas últimas jogadas:")
    for cor, prob in probs.items():
        st.write(f"**{cor.capitalize()}**: {prob*100:.2f}%")

    # Frequência total
    st.markdown("### 📈 Frequência de cada cor:")
    freq = Counter(st.session_state.historico)
    for cor in CORES:
        st.write(f"**{cor.capitalize()}**: {freq.get(cor, 0)} vezes")

    # Repetições seguidas
    rep, cor = contar_repeticoes(st.session_state.historico)
    if rep > 1:
        st.warning(f"⚠️ Atenção: a cor **{cor.upper()}** saiu {rep} vezes seguidas!")

    # Análise de sequências
    _, seq_freq = analisar_sequencias(st.session_state.historico)
    if seq_freq:
        st.markdown("### 🔁 Sequências mais comuns:")
        mais_comuns = seq_freq.most_common(5)
        for (a, b), qt in mais_comuns:
            st.write(f"{a} → {b}: {qt} vezes")
