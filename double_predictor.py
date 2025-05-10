import streamlit as st
from collections import Counter
import random
import matplotlib.pyplot as plt

# Lista de cores possíveis
CORES = ["vermelho", "preto", "branco"]

# Inicializar o histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Função para prever a próxima cor com base nas últimas jogadas
def prever_proxima_cor(historico, ultimas=15):
    if len(historico) < ultimas:
        ultimos = historico
    else:
        ultimos = historico[-ultimas:]
        
    contagem = Counter(ultimos)
    total = sum(contagem.values())
    probabilidade = {cor: contagem.get(cor, 0) / total for cor in CORES}
    previsao = max(probabilidade, key=probabilidade.get)
    return previsao, probabilidade

# Função para salvar jogadas automaticamente (simulação)
def salvar_jogada_automaticamente():
    nova_cor = random.choice(CORES)  # Escolhe uma cor aleatória
    st.session_state.historico.append(nova_cor)
    return nova_cor

# Função para exibir gráficos de frequência
def plotar_frequencias(frequencias):
    fig, ax = plt.subplots()
    ax.bar(frequencias.keys(), frequencias.values(), color=["red", "black", "white"])
    ax.set_xlabel("Cor")
    ax.set_ylabel("Quantidade")
    ax.set_title("Frequência das Cores")
    st.pyplot(fig)

# Interface do App
st.title("🎯 **Previsor de Cores - Blaze Double**")
st.markdown("""
Registre as cores que saíram no jogo Double da Blaze e veja uma previsão das próximas jogadas, 
com base em análise de padrões e frequências.
""")

# Barra de seleção de cores e botão para registrar
col1, col2, col3 = st.columns(3)
with col1:
    nova_cor = st.selectbox("Selecione a cor que saiu:", CORES)

with col2:
    if st.button("Registrar Cor"):
        st.session_state.historico.append(nova_cor)
        st.success(f"Cor registrada: {nova_cor.upper()}")

with col3:
    if st.button("❌ Desfazer Última Cor"):
        if st.session_state.historico:
            removida = st.session_state.historico.pop()
            st.warning(f"Última cor removida: {removida.upper()}")
        else:
            st.info("Nenhuma cor registrada para desfazer.")

# Simulação de jogadas automáticas (pode ser ativada automaticamente, ou por botão)
if st.button("💡 Salvar Jogada Automática"):
    nova_jogada = salvar_jogada_automaticamente()
    st.success(f"Jogada automática registrada: {nova_jogada.upper()}")

# Exibição do histórico de cores registradas
st.markdown("### 🧾 Histórico das últimas jogadas:")
st.write(st.session_state.historico[-15:] or "Nenhum registro ainda.")

# Análise de padrões e previsões
if st.session_state.historico:
    previsao, probs = prever_proxima_cor(st.session_state.historico)
    st.markdown("### 🔮 Previsão da Próxima Cor:")
    st.info(f"**Probabilidade mais alta**: {previsao.upper()}")

    # Exibir gráfico de probabilidades
    st.markdown("### 📊 Probabilidades das Cores:")
    fig, ax = plt.subplots()
    ax.bar(probs.keys(), probs.values(), color=["red", "black", "white"])
    ax.set_xlabel("Cor")
    ax.set_ylabel("Probabilidade (%)")
    ax.set_title("Probabilidade de cada cor")
    st.pyplot(fig)

    # Análise de frequências
    st.markdown("### 📈 Frequência de cada cor:")
    freq = Counter(st.session_state.historico)
    for cor in CORES:
        st.write(f"**{cor.capitalize()}**: {freq.get(cor, 0)} vezes")

    # Detecção de repetições consecutivas
    rep, cor = contar_repeticoes(st.session_state.historico)
    if rep > 1:
        st.warning(f"⚠️ Atenção: a cor **{cor.upper()}** saiu {rep} vezes seguidas!")

    # Análise de sequências
    sequencias = [(st.session_state.historico[i], st.session_state.historico[i+1]) for i in range(len(st.session_state.historico)-1)]
    sequencias_freq = Counter(sequencias)
    if sequencias_freq:
        st.markdown("### 🔁 Sequências mais comuns:")
        for (a, b), qt in sequencias_freq.most_common(5):
            st.write(f"**{a} → {b}**: {qt} vezes")

else:
    st.info("Ainda não há jogadas registradas.")
