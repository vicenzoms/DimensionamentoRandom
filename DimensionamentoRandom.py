# -*- coding: utf-8 -*-
"""
Spare Parts Inventory Sizing System - Grupo RANDOM
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson, norm
import base64
from pathlib import Path
from PIL import Image

# Configuração inicial da página
st.set_page_config(page_title="Dimensionamento de Sobressalentes - RANDOM", layout="wide")

def image_to_base64(path):
    """Função para converter imagens em Base64 e renderizá-las no HTML/CSS"""
    try:
        image_path = Path(path)
        if not image_path.exists():
            return ""
        return base64.b64encode(image_path.read_bytes()).decode("utf-8")
    except Exception:
        return ""

# Carrega as imagens para a tela de login (capa de fundo e logo)
LOGIN_BG_BASE64 = image_to_base64("capa.png")
LOGIN_BG_URL = f"data:image/png;base64,{LOGIN_BG_BASE64}" if LOGIN_BG_BASE64 else ""

LOGO_BASE64 = image_to_base64("logo.png")
LOGO_HTML = f'<img src="data:image/png;base64,{LOGO_BASE64}" class="login-logo">' if LOGO_BASE64 else ''

# Inicializa o estado de autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# TELA DE LOGIN 

if not st.session_state.authenticated:
    st.markdown(
        f"""
        <style>
        /* Oculta menus padrão do Streamlit no ecrã de login */
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            height: 100%;
            overflow: hidden !important;
            background: #f4f5f7 !important;
        }}
        [data-testid="stSidebar"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stHeader"] {{
            display: none !important;
        }}
        .main, .stApp {{ background: transparent !important; }}
        .block-container {{ max-width: 100% !important; padding: 0 !important; margin: 0 !important; }}

        /* Fundo claro com gradiente sobre a imagem */
        .login-bg-full {{
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(135deg, rgba(255,255,255,0.92) 0%, rgba(240,242,245,0.98) 100%),
                url("{LOGIN_BG_URL}");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-color: #f4f5f7;
            z-index: 0;
        }}

        .login-page-content {{
            position: relative;
            z-index: 5;
            padding: 8vh 38px 18px 38px;
            display: flex;
            justify-content: center;
        }}

        .login-title-box {{
            margin-top: 5px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .login-logo {{
            max-height: 150px;
            width: auto;
            margin-bottom: 15px;
        }}

        .login-title-box h2 {{
            margin: 0;
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: #388E3C; /* Verde Material */
            font-family: 'Roboto', sans-serif;
        }}
        
        .login-title-box p {{
            color: #666666;
            font-size: 0.95rem;
            margin-top: 5px;
        }}

        /* Estilo do Cartão (Material Design Branco) */
        div[data-testid="stForm"] {{
            background: #ffffff !important;
            border-radius: 8px !important;
            border: 1px solid #e0e0e0 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
            padding: 2.5rem 2rem 2rem 2rem !important;
        }}
        div[data-testid="stForm"] > div {{ background: transparent !important; border: 0 !important; box-shadow: none !important; }}
        div[data-testid="stForm"] label {{ color: #333333 !important; font-weight: 600 !important; font-size: 0.90rem !important; }}
        div[data-testid="stForm"] input {{
            background: #fafafa !important;
            color: #333333 !important;
            border: 1px solid #cccccc !important;
            border-radius: 4px !important;
            min-height: 2.8rem !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease-in-out;
        }}
        div[data-testid="stForm"] input:focus {{ border-color: #388E3C !important; box-shadow: 0 0 0 1px #388E3C !important; }}

        /* Botão Material Green */
        .stFormSubmitButton > button {{
            width: 100% !important;
            min-height: 2.8rem !important;
            border-radius: 4px !important;
            background: #388E3C !important;
            color: #ffffff !important;
            border: 0 !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: 0 2px 5px rgba(56, 142, 60, 0.3) !important;
            transition: background 0.2s;
        }}
        .stFormSubmitButton > button:hover {{
            background: #2E7D32 !important;
            color: #ffffff !important;
            box-shadow: 0 4px 8px rgba(56, 142, 60, 0.4) !important;
        }}

        div[data-testid="stAlert"] {{ border-radius: 4px !important; margin-top: 0.75rem !important; }}
        @media (max-width: 980px) {{ .login-page-content {{ padding: 4vh 18px; }} }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-bg-full"></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-page-content">', unsafe_allow_html=True)

    # Colunas para centralizar o formulário na tela
    col_vazia1, col_login, col_vazia2 = st.columns([1, 1.2, 1])

    with col_login:
        st.markdown(
            f"""
            <div class="login-title-box">
                {LOGO_HTML}
                <h2>Acesso ao Sistema</h2>
                <p>RANDOM - Grupo de Pesquisa</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Utilizador", placeholder="Digite o seu utilizador")
            password = st.text_input("Palavra-passe", type="password", placeholder="Digite a sua palavra-passe")
            submitted = st.form_submit_button("Entrar", use_container_width=True)

        if submitted:
            if username.strip().lower() == "vicenzo" and password == "12345":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Utilizador ou palavra-passe incorretos.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()  


# CSS DA TELA PRINCIPAL (Pós-Login - Estilo Verde)
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    h1, h2, h3 { color: #388E3C !important; font-family: 'Roboto', sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e0e0e0; }
    
    .stButton > button {
        background-color: #388E3C !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        font-weight: 600 !important;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #2E7D32 !important;
        color: white !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    
    [data-testid="stMetricValue"] { color: #333333 !important; }
    [data-testid="stMetricLabel"] { color: #666666 !important; font-weight: 600 !important; }
    hr { border-color: #eeeeee !important; }
    </style>
""", unsafe_allow_html=True)


# FUNÇÕES AUXILIARES
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
        'Risco': lista_risco 
    })
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
        'Risco': lista_risco 
    })
    return df, x_ideal, sigma

def exibir_resumo_streamlit(df, x_alvo, titulo, texto_destaque="Quantidade Recomendada", mostrar_contexto=True):
    """Exibe o DataFrame formatado. Se mostrar_contexto for False, exibe apenas a linha do x_alvo."""
    st.subheader(titulo)
    
    if mostrar_contexto:
        # Pega a linha antes, a linha alvo e a linha depois para mostrar contexto (Usado no Optimizer)
        idx_inicio = max(0, x_alvo - 1)
        resumo = df.iloc[idx_inicio : x_alvo + 2].copy()
    else:
        # Pega apenas a linha onde x é igual ao x_alvo (Usado no Analytical)
        resumo = df[df['x'] == x_alvo].copy()
    
    resumo['P(X=x)'] = resumo['P(X=x)'].apply(lambda v: f"{v:.4%}")
    resumo['Margem Seg.'] = resumo['Margem Seg.'].apply(lambda v: f"{v:.4%}")
    resumo['Risco'] = resumo['Risco'].apply(lambda v: f"{v:.4%}")
    
    st.success(f"**{texto_destaque}:** {x_alvo} peças")
    st.dataframe(resumo, use_container_width=True, hide_index=True)


# INTERFACE PRINCIPAL
col_img1, col_img2, col_img3 = st.columns(3)
try:
    foto = Image.open('randomen.png')
    col_img2.image(foto, use_container_width=True)
except Exception:
    pass

st.markdown("<h2 style='text-align: center; color: #388E3C;'>Spare Parts Inventory Sizing System</h2>", unsafe_allow_html=True)

menu = ["Analytical", "Optimizer", "Optimizer MA"]
choice = st.sidebar.selectbox("Select here", menu)


#  ANALYTICAL

if choice == menu[0]:
    st.header(menu[0])
    
    st.subheader("Avaliação da Situação Atual do Sistema")
    st.write("Insira a quantidade de peças sobressalentes em uso e os parâmetros operacionais para calcular a margem de segurança e o custo atual.")
    
    # BARRAS DE INPUT
    Q_atual = st.number_input("Quantidade atual de peças Sobressalentes (x):", min_value=0, value=5, step=1)
    L = st.number_input("Lambda (taxa de falha):", min_value=0.0000, value=0.05, step=0.01, format="%.6f")
    N = st.number_input("Número de máquinas ativas (n):", min_value=1, value=10, step=1)
    T = st.number_input("Tempo de reposição (t):", min_value=1, value=1, step=1)
    custo_unitario = st.number_input("Custo Unitário por Peça (R$):", min_value=0.00, value=150.00, step=10.00, format="%.2f")
    
    botao_analytical = st.button("Calcular Situação Atual")
    
    if botao_analytical:
        m_val = L * N * T
        LG = L * N
        custo_total = Q_atual * custo_unitario
        
        st.subheader("Parâmetros do Sistema")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Valor Esperado de Falhas (m)", f"{m_val:.2f}")
        col_m2.metric("Custo Total (Inventário Atual)", f"R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.divider()
        
        # Gerar DataFrame de Poisson até Q_atual para exibir na tabela
        lista_x, lista_p, lista_margem, lista_risco = [], [], [], []
        prob_acumulada = 0
        for x in range(Q_atual + 1):
            p_x = poisson.pmf(x, m_val)
            prob_acumulada += p_x
            lista_x.append(x)
            lista_p.append(p_x)
            lista_margem.append(prob_acumulada)
            lista_risco.append(max(1 - prob_acumulada, 0.0))
        df_p_analitico = pd.DataFrame({'x': lista_x, 'P(X=x)': lista_p, 'Margem Seg.': lista_margem, 'Risco': lista_risco})
        
        # Exibição
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            exibir_resumo_streamlit(df_p_analitico, Q_atual, "Distribuição de Poisson", texto_destaque="Quantidade Atual", mostrar_contexto=False)
            
        with col_t2:
            if LG >= 20:
                # Gerar DataFrame da Normal até Q_atual
                lista_x_n, lista_p_n, lista_margem_n, lista_risco_n = [], [], [], []
                sigma = np.sqrt(m_val)
                for x in range(Q_atual + 1):
                    prob_acum_n = norm.cdf(x, loc=m_val, scale=sigma)
                    p_x_n = prob_acum_n if x == 0 else prob_acum_n - norm.cdf(x - 1, loc=m_val, scale=sigma)
                    lista_x_n.append(x)
                    lista_p_n.append(p_x_n)
                    lista_margem_n.append(prob_acum_n)
                    lista_risco_n.append(max(1 - prob_acum_n, 0.0))
                df_n_analitico = pd.DataFrame({'x': lista_x_n, 'P(X=x)': lista_p_n, 'Margem Seg.': lista_margem_n, 'Risco': lista_risco_n})
                
                exibir_resumo_streamlit(df_n_analitico, Q_atual, "Aproximação Normal", texto_destaque="Quantidade Atual", mostrar_contexto=False)
            else:
                st.subheader("Aproximação Normal")
                st.warning("Aproximação pela Normal não recomendada.")


# OPTIMIZER 

elif choice == menu[1]:
    st.header(menu[1])
    
    st.subheader("Insert the parameter values below:")
    
    # BARRAS DE INPUT 
    L = st.number_input("Lambda (taxa de falha):", min_value=0.0000, value=0.05, step=0.01, format="%.6f")
    N = st.number_input("Número de máquinas ativas (n):", min_value=1, value=10, step=1)
    T = st.number_input("Tempo de reposição (t):", min_value=1, value=1, step=1)
    R_PCT = st.number_input("Risco Alvo (%):", min_value=0.01, max_value=99.99, value=5.00, step=1.0, format="%.2f")
    custo_unitario = st.number_input("Custo Unitário por Peça (R$):", min_value=0.00, value=150.00, step=10.00, format="%.2f")

    st.subheader("Click on button below to run this application:")    
    botao = st.button("Calcular Dimensionamento")        
    
    if botao:
        risco = R_PCT / 100.0
        LG = L * N
        
        df_p, x_p, m_val = calcular_poisson(L, N, T, risco)
        df_n, x_n, sigma_val = calcular_normal(L, N, T, risco)
        
        custo_total = custo_unitario * x_p

        st.subheader("Parâmetros Utilizados")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Valor Esperado de Falhas (m)", f"{m_val:.2f}")
        col_m2.metric("Risco Alvo", f"{R_PCT}%")
        col_m3.metric("Custo Total (Inventário Ótimo)", f"R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.divider()

        col_tabela1, col_tabela2 = st.columns(2)
        
        with col_tabela1:
            exibir_resumo_streamlit(df_p, x_p, "Distribuição de Poisson", mostrar_contexto=True)
            
        with col_tabela2:
            if LG >= 20:
                exibir_resumo_streamlit(df_n, x_n, "Aproximação Normal", mostrar_contexto=True)
            else:
                st.subheader("Aproximação Normal")
                st.warning("Aproximação pela Normal não recomendada.")


#  OPTIMIZER MA

elif choice == menu[2]:
    st.header(menu[2])
    st.subheader("Otimização com Manutenção Aditiva (Mix de Peças)")
    st.write("Determine a combinação ótima entre peças tradicionais e impressas em 3D para minimizar custos, respeitando o risco alvo.")
    
    # Criar colunas para organizar os inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚙️ Peças Tradicionais")
        L_trad = st.number_input("Lambda Tradicional:", min_value=0.0000, value=0.05, step=0.01, format="%.6f", key="l_trad")
        T_trad = st.number_input("Tempo de reposição (t):", min_value=1, value=5, step=1, key="t_trad")
        C_trad = st.number_input("Custo Unitário (R$):", min_value=0.00, value=500.00, step=10.00, format="%.2f", key="c_trad")
        
    with col2:
        st.markdown("#### 🖨️ Peças Impressas em 3D")
        L_3d = st.number_input("Lambda 3D (maior fragilidade):", min_value=0.0000, value=0.08, step=0.01, format="%.6f", key="l_3d")
        T_3d = st.number_input("Tempo de impressão (t):", min_value=1, value=1, step=1, key="t_3d")
        C_3d = st.number_input("Custo de Impressão (R$):", min_value=0.00, value=100.00, step=10.00, format="%.2f", key="c_3d")
        
    st.divider()
    st.markdown("#### 📊 Parâmetros Globais do Sistema")
    col3, col4 = st.columns(2)
    with col3:
        N_maq = st.number_input("Número de máquinas ativas (n):", min_value=1, value=10, step=1, key="n_maq_ma")
    with col4:
        R_PCT_MA = st.number_input("Risco Alvo (%):", min_value=0.01, max_value=99.99, value=5.00, step=1.0, format="%.2f", key="r_pct_ma")

    st.subheader("Clique no botão abaixo para calcular o Mix Ótimo:")    
    botao_ma = st.button("Calcular Mix Ótimo MA")

    if botao_ma:
        risco_alvo = R_PCT_MA / 100.0
        
        melhor_custo = float('inf')
        melhor_mix = None
        melhor_risco = 1.0
        melhor_m = 0.0
        
        # Limite de busca para o Grid Search (pode aumentar se necessário para sistemas muito grandes)
        limite_busca = 40 
        
        # Algoritmo de Busca (Grid Search)
        for x_trad in range(limite_busca):
            for x_3d in range(limite_busca):
                total_pecas = x_trad + x_3d
                if total_pecas == 0:
                    continue
                    
                # -------------------------------------------------------------------
                # MODELO MATEMÁTICO (Aproximação por Média Ponderada do m)
                # O risco depende da proporção de peças no inventário
                # -------------------------------------------------------------------
                prop_trad = x_trad / total_pecas
                prop_3d = x_3d / total_pecas
                
                # m = lambda * n * t
                m_trad_puro = L_trad * N_maq * T_trad
                m_3d_puro = L_3d * N_maq * T_3d
                
                m_equivalente = (prop_trad * m_trad_puro) + (prop_3d * m_3d_puro)
                
                # Calcula o risco usando a Poisson para o total de peças com o m_equivalente
                prob_acumulada = poisson.cdf(total_pecas, m_equivalente)
                risco_atual = max(1.0 - prob_acumulada, 0.0)
                
                # Verifica se respeita o critério de risco
                if risco_atual <= risco_alvo:
                    custo_atual = (x_trad * C_trad) + (x_3d * C_3d)
                    
                    # Se respeita o risco e é mais barato, guarda como a melhor opção
                    if custo_atual < melhor_custo:
                        melhor_custo = custo_atual
                        melhor_mix = (x_trad, x_3d)
                        melhor_risco = risco_atual
                        melhor_m = m_equivalente

        # Resultados Visuais
        if melhor_mix is not None:
            st.success("✅ Combinação ótima encontrada com sucesso!")
            
            st.subheader("Resultados da Otimização")
            res_col1, res_col2, res_col3 = st.columns(3)
            
            res_col1.metric("Peças Tradicionais", f"{melhor_mix[0]} unid.")
            res_col2.metric("Peças 3D (Aditivas)", f"{melhor_mix[1]} unid.")
            res_col3.metric("Total de Peças", f"{melhor_mix[0] + melhor_mix[1]} unid.")
            
            st.divider()
            
            indicadores_col1, indicadores_col2, indicadores_col3 = st.columns(3)
            indicadores_col1.metric("Valor Esperado Falhas (m ponderado)", f"{melhor_m:.2f}")
            indicadores_col2.metric("Risco Obtido", f"{melhor_risco:.4%}")
            indicadores_col3.metric("Custo Total Mínimo", f"R$ {melhor_custo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            
            # Gráfico ou Tabela ilustrativa simples do resultado
            df_resultado = pd.DataFrame({
                "Tipo": ["Tradicional", "Impressão 3D"],
                "Quantidade": [melhor_mix[0], melhor_mix[1]],
                "Custo Unitário (R$)": [C_trad, C_3d],
                "Subtotal (R$)": [melhor_mix[0] * C_trad, melhor_mix[1] * C_3d]
            })
            st.dataframe(df_resultado, use_container_width=True, hide_index=True)
            
        else:
            st.error(f"❌ Não foi possível encontrar uma combinação que atinja o Risco Alvo de {R_PCT_MA}% dentro do limite estabelecido ({limite_busca} peças de cada). Tente relaxar os parâmetros ou aumentar o limite de busca no código.")


