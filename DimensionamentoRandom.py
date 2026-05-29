# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:17:56 2026

@author: Vicenzo
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson, norm
import base64
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Dimensionamento de Sobressalentes", layout="wide")

def image_to_base64(path):
    try:
        image_path = Path(path)
        if not image_path.exists():
            return ""
        return base64.b64encode(image_path.read_bytes()).decode("utf-8")
    except Exception:
        return ""

# Tenta carregar uma imagem de fundo (opcional, pode ser a mesma capa.png usada no outro app)
LOGIN_BG_BASE64 = image_to_base64("capa.png")
LOGIN_BG_URL = f"data:image/png;base64,{LOGIN_BG_BASE64}" if LOGIN_BG_BASE64 else ""

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            height: 100%;
            overflow: hidden !important;
            background: #03152b !important;
        }}

        [data-testid="stSidebar"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{
            display: none !important;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
            height: 0 !important;
        }}

        .main, .stApp {{
            background: transparent !important;
        }}

        .block-container {{
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }}

        .login-bg-full {{
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(90deg, rgba(3,21,43,0.04) 0%, rgba(3,21,43,0.02) 58%, rgba(3,21,43,0.10) 100%),
                url("{LOGIN_BG_URL}");
            background-size: 100% 100%;
            background-position: center center;
            background-repeat: no-repeat;
            background-color: #03152b;
            z-index: 0;
        }}

        .login-page-content {{
            position: relative;
            z-index: 5;
            padding: 28px 38px 18px 38px;
        }}

        .login-page-content > div[data-testid="stHorizontalBlock"] {{
            align-items: flex-start !important;
        }}

        .login-title-box {{
            margin-top: 16px;
            margin-bottom: 10px;
            text-align: center;
        }}

        .login-title-box h2 {{
            margin: 0;
            font-size: 2.15rem;
            font-weight: 900;
            letter-spacing: -0.04em;
            color: #ffffff;
            text-shadow: 0 3px 14px rgba(0,0,0,0.42);
        }}

        div[data-testid="stForm"] {{
            background: rgba(255,255,255,0.97) !important;
            border-radius: 28px !important;
            border: 1px solid rgba(255,255,255,0.78) !important;
            box-shadow: 0 24px 56px rgba(0,19,42,0.24) !important;
            padding: 1.25rem 1.25rem 1.05rem 1.25rem !important;
            backdrop-filter: blur(8px);
        }}

        div[data-testid="stForm"] > div {{
            background: transparent !important;
            border: 0 !important;
            box-shadow: none !important;
        }}

        div[data-testid="stForm"] label {{
            color: #2b3443 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }}

        div[data-testid="stForm"] input {{
            background: #ffffff !important;
            color: #111827 !important;
            border: 1px solid rgba(17,24,39,0.14) !important;
            border-radius: 13px !important;
            min-height: 2.95rem !important;
            font-size: 0.96rem !important;
        }}

        .stFormSubmitButton > button {{
            width: 100% !important;
            min-height: 2.95rem !important;
            border-radius: 13px !important;
            background: #0b76bd !important;
            color: #ffffff !important;
            border: 0 !important;
            font-size: 1rem !important;
            font-weight: 780 !important;
            box-shadow: 0 14px 28px rgba(11,118,189,0.28) !important;
        }}

        .stFormSubmitButton > button:hover {{
            background: #095f98 !important;
            color: #ffffff !important;
        }}

        div[data-testid="stAlert"] {{
            border-radius: 12px !important;
            margin-top: 0.75rem !important;
        }}

        @media (max-width: 980px) {{
            .login-bg-full {{
                background-size: cover;
                background-position: center center;
            }}
            .login-page-content {{
                padding: 18px;
            }}
            .login-title-box h2 {{
                font-size: 1.85rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-bg-full"></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-page-content">', unsafe_allow_html=True)

    left_space, right_login = st.columns([1.72, 0.52], gap="medium")

    with left_space:
        st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)

    with right_login:
        st.markdown(
            """
            <div class="login-title-box">
                <h2>Acesso</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Usuário", placeholder="Digite seu usuário")
            password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submitted = st.form_submit_button("Entrar", use_container_width=True)

        if submitted:
            if username.strip().lower() == "vicenzo" and password == "12345":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()  

# ==========================================
# LÓGICA DE CÁLCULO
# ==========================================
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

# ==========================================
# TELA PRINCIPAL (Template adaptado do main.py)
# ==========================================

# Criando 3 colunas para colocar a imagem no centro
col_img1, col_img2, col_img3 = st.columns(3)
try:
    foto = Image.open('randomen.png')
    col_img2.image(foto, use_container_width=True)
except FileNotFoundError:
    col_img2.warning("Imagem 'randomen.png' não encontrada.")

# Título centralizado
st.markdown("<h2 style='text-align: center; color: #0b76bd;'>Sistema de Dimensionamento de Sobressalentes</h2>", unsafe_allow_html=True)

# Menu na barra lateral
menu = ["Dimensionamento", "Sobre"]
choice = st.sidebar.selectbox("Selecione o modo", menu)

if choice == menu[0]:
    st.header(menu[0])
    
    st.subheader("Insira os parâmetros abaixo:")
    
    # Inputs movidos para o meio da tela (main area)
    L = st.number_input("Lambda (taxa de falha):", min_value=0.0000, value=0.05, step=0.01, format="%.6f")
    N = st.number_input("Número de máquinas ativas (n):", min_value=1, value=10, step=1)
    T = st.number_input("Tempo de reposição (t):", min_value=1, value=1, step=1)
    R_PCT = st.number_input("Risco Alvo (%):", min_value=0.01, max_value=99.99, value=5.00, step=1.0, format="%.2f")

    st.subheader("Clique no botão abaixo para calcular as recomendações:")    
    botao = st.button("Calcular Dimensionamento")        
    
    if botao:
        risco = R_PCT / 100.0
        LG = L * N
        
        df_p, x_p, m_val = calcular_poisson(L, N, T, risco)
        df_n, x_n, sigma_val = calcular_normal(L, N, T, risco)
        
        n_10PCT = max(1, int(np.ceil(0.10 * N)))

        st.subheader("Parâmetros Utilizados")
        col1, col2, col3 = st.columns(3)
        col1.metric("Valor Esperado de Falhas (m)", f"{m_val:.2f}")
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

        col_tabela1, col_tabela2 = st.columns(2)
        
        with col_tabela1:
            exibir_resumo_streamlit(df_p, x_p, "Distribuição de Poisson")
            
        with col_tabela2:
            if LG >= 20:
                exibir_resumo_streamlit(df_n, x_n, "Aproximação Normal")
            else:
                st.info("Aproximação pela Normal não recomendada.")

elif choice == menu[1]:
    st.header(menu[1])
    st.write("Este sistema realiza o dimensionamento de peças sobressalentes usando as distribuições de Poisson e Normal.")
    st.write("Desenvolvido por Vicenzo para o grupo de pesquisa RANDOM.")
