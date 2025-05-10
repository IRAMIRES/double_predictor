import streamlit as st
import random

class DoublePredictor:
    def __init__(self):
        self.cores = ['preto', 'vermelho', 'branco']
        self.history = []  # Histórico das cores que saíram

    def registrar_cor(self, cor):
        """Registra a cor que saiu para análise futura."""
        if cor in self.cores:
            self.history.append(cor)

    def prever_cor(self):
        """Faz uma previsão simples da próxima cor com base no histórico."""
        if len(self.history) == 0:
            return random.choice(self.cores)
        
        # Contagem das cores no histórico
        contagem = {cor: self.history.count(cor) for cor in self.cores}
        
        # Probabilidades simples com base na frequência das cores
        probabilidade = {cor: contagem[cor] / len(self.history) for cor in self.cores}
        
        # Escolha a cor que menos apareceu ou a que tem a maior probabilidade
        cor_prevista = min(probabilidade, key=probabilidade.get)
        
        return cor_prevista

# Inicializa o preditor
preditor = DoublePredictor()

st.title('Double Predictor')
st.write("Bem-vindo ao preditor do Double. Escolha as cores jogadas para ver a previsão da próxima cor.")

# Formulário para registrar a cor
cor_jogada = st.selectbox("Escolha a cor jogada:", ['preto', 'vermelho', 'branco'])

if st.button('Registrar cor'):
    preditor.registrar_cor(cor_jogada)
    st.write(f"A cor {cor_jogada} foi registrada no histórico!")

# Exibir histórico
st.write("Histórico de cores jogadas:", preditor.history)

# Prever a próxima cor
if len(preditor.history) > 0:
    cor_prevista = preditor.prever_cor()
    st.write(f"A próxima cor prevista é: {cor_prevista}")
else:
    st.write("Ainda não há histórico suficiente para previsão.")
