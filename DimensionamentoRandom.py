# -*- coding: utf-8 -*-
"""
Created on Thu May 28 17:04:19 2026

@author: Vicenzo
"""


import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson, norm

st.set_page_config(page_title="Dimensionamento de Sobressalentes", layout="wide")

def calcular_poisson(lmbda, n, t, risco_alvo):
    m = lmbda * n * t
    x = 0
    prob_acumulada = 0
    x_ideal = -1
    
    lista_x, lista_p, lista_margem, lista_risco = [], [], [], []
    
    while True:
        p_x = poisson.pmf(x, m)
        prob_acumulada += p_x
        risco_atual = max(1 - prob_acumulada, 0.0)
        
        lista_x.append(x)
        lista_p.append(p_x)
        lista_margem.append(prob_acumulada)
        lista_risco.append(risco_atual)
        
        if risco_atual < risco_alvo and x_ideal == -1:
            x_ideal = x
            
        if x_ideal != -1 and x >= x_ideal + 1:
            break
        x += 1
        
    df = pd.DataFrame({
        'x': lista_x,
        'P(X=x)': lista_p,
        'Margem Seg.': lista_margem,
        'Risco': lista_risco })
    
    return df, x_ideal, m

def calcular_normal(lmbda, n, t, risco_alvo):
    m = lmbda * n * t
    sigma = np.sqrt(m)
    x = 0
    x_ideal = -1
    
    lista_x, lista_p, lista_margem, lista_risco = [], [], [], []
    
    while True:
        prob_acum = norm.cdf(x, loc=m, scale=sigma)
       
        if x == 0:
            p_x = prob_acum
        else:
            p_x = prob_acum - norm.cdf(x - 1, loc=m, scale=sigma)
            
        risco_atual = max(1 - prob_acum, 0.0)
        
        lista_x.append(x)
        lista_p.append(p_x)
        lista_margem.append(prob_acum)
        lista_risco.append(risco_atual)
        
        if risco_atual < risco_alvo and x_ideal == -1:
            x_ideal = x
            
        if x_ideal != -1 and x >= x_ideal + 1:
            break
        x += 1
        
    df = pd.DataFrame({
        'x': lista_x,
        'P(X=x)': lista_p,
        'Margem Seg.': lista_margem,
        'Risco': lista_risco })
    
    return df, x_ideal, sigma

def main():
    # Título centralizado e estilizado igual ao main.py
    st.markdown("<h2 style='text-align: center; color: #306754;'>Sistema de Dimensionamento de Sobressalentes</h2>", unsafe_allow_html=True)
    
    # Criação do menu lateral para mudança de modo
    menu = ["Calculadora", "Instruções"]
    choice = st.sidebar.selectbox("Selecione o modo aqui", menu)
    
    if choice == menu[0]:
        st.header("Calculadora")
        
        # Parâmetros trazidos da barra lateral para o meio da tela
        st.subheader("Insira os valores dos parâmetros abaixo:")
        
        L = st.number_input("Lambda (taxa de falha):", min_value=0.0000, value=0.05, step=0.01, format="%.6f")
        N = st.number_input("Número de máquinas ativas (n):", min_value=1, value=10, step=1)
        T = st.number_input("Tempo (t):", min_value=0.1, value=1.0, step=0.1)
        R_PCT = st.number_input("Risco máximo aceitável em %:", min_value=0.01, max_value=100.0, value=5.0, step=1.0)
        
        st.subheader("Clique no botão abaixo para rodar a aplicação:")    
        botao = st.button("Calcular Dimensionamento")
        
        if botao:
            R_ALVO = R_PCT / 100.0
            n_10PCT = round(N * 0.1)
            
            # Cálculo do lambda geral
            lambda_geral = L * N
        
            df_p, x_p, m_val = calcular_poisson(L, N, T, R_ALVO)
        
            st.divider() 
            col1, col2, col3 = st.columns(3)
            col1.metric("Média (m)", f"{m_val:.2f}")
            col2.metric("Risco Alvo", f"{R_PCT}%")
            col3.metric("Regra dos 10%", f"{n_10PCT} peças")
        
            st.divider()
        
            def exibir_resumo_streamlit(df, x_alvo, titulo):
                st.subheader(titulo)
                
                idx_inicio = max(0, x_alvo - 1)
                resumo = df.iloc[idx_inicio : x_alvo + 2].copy()
                
                resumo['P(X=x)'] = resumo['P(X=x)'].apply(lambda v: f"{v:.4%}")
                resumo['Margem Seg.'] = resumo['Margem Seg.'].apply(lambda v: f"{v:.4%}")
                resumo['Risco'] = resumo['Risco'].apply(lambda v: f"{v:.4%}")
                
                st.success(f"**Quantidade Recomendada:** {x_alvo} peças")
                st.dataframe(resumo, use_container_width=True, hide_index=True)
        
            # Mantendo a mesma forma de output das tabelas
            col_tabela1, col_tabela2 = st.columns(2)
            
            with col_tabela1:
                exibir_resumo_streamlit(df_p, x_p, "Distribuição de Poisson")
                
            with col_tabela2:
                # Condicional para exibir a Aproximação pela Normal
                if lambda_geral >= 20:
                    df_n, x_n, sigma_val = calcular_normal(L, N, T, R_ALVO)
                    exibir_resumo_streamlit(df_n, x_n, "Aproximação pela Normal")
                else:
                    st.subheader("Aproximação pela Normal")
                    st.warning(f"**Cálculo não recomendado:** O λ geral é **{lambda_geral:.2f}**. O método de Aproximação pela Normal é válido apenas para λ ≥ 20.")

    elif choice == menu[1]:
        # Espaço reservado para documentação futura do projeto no estilo de um segundo modo
        st.header("Instruções")
        st.write("Esta página é dedicada à visualização das lógicas e premissas por trás do dimensionamento.")
        st.info("Utilize a barra lateral para voltar ao modo **Calculadora**.")

if __name__ == "__main__":
    # Caso possua lógica de login, envolva a chamada do main() nessa condicional.
    main()