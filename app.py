import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Precificação - Tattoo", page_icon="🎨", layout="centered")

st.title("🎨 Calculadora de Precificação de Tatuagens")
st.write("Insira os parâmetros para calcular o orçamento ideal.")

st.divider()

# --- INPUTS GERAIS ---
valor_base = st.number_input("Valor Base do seu trabalho (R$):", min_value=50, value=150, step=10)
num_sessoes = st.number_input("Quantidade de Sessões Estimadas:", min_value=1, value=1, step=1)

# --- CHAVE DE FECHAMENTO ---
is_fechamento = st.checkbox("É um projeto de Fechamento?")

# Definição dos grupos de Fechamento por Dificuldade
fechamento_facil = ["Antebraço externo", "Braço superior externo", "Panturrilha", "Canela", "Panturrilha lateral externa"]
fechamento_medio = ["Antebraço interno", "Braço superior interno", "Braço externo", "Braço interno", "Coxa frontal", "Coxa traseira", "Coxa lateral externa", "Panturrilha lateral interna"]
fechamento_dificil = ["Pescoço", "Torax", "Antebraço completo", "Braço superior completo", "Coxa lateral interna", "Perna inferior completo", "Pé"]
fechamento_extremo = ["Braço completo", "Costas", "Costela", "Coxa completa", "Perna completa"]

if is_fechamento:
    # Lista unificada para o menu do usuário
    fechamentos_lista = fechamento_facil + fechamento_medio + fechamento_dificil + fechamento_extremo
    tipo_fechamento = st.selectbox("Qual o Fechamento?", fechamentos_lista)
    tamanho = "Fechamento"
    regiao = "Fechamento"
else:
    # Inputs tradicionais para peças isoladas
    tamanho_opcoes = ["PP (Até 3cm)", "P (4cm a 8cm)", "M (9cm a 14cm)", "G (15cm a 20cm)", "GG (21cm a 28cm)"]
    tamanho = st.selectbox("Tamanho da Tatuagem:", tamanho_opcoes)
    
    corpo_facil = ["Braço parte externa", "Antebraço parte externa", "Panturrilha"]
    corpo_media = ["Mão", "Braço parte interna", "Antebraço parte interna", "Ombro", "Nuca", "Coxas frente", "Coxas trás", "Coxas lateral externa", "Canelas", "Lateral externa canela"]
    corpo_dificil = ["Pescoço", "Peito", "Underboob", "Barriga", "Lombar", "Coxas lateral interna", "Quadril", "Nádegas", "Lateral interna canela", "Costas parte torácica", "Pé"]
    corpo_extrema = ["Costela", "Cotovelo", "Joelho"]
    
    regiao = st.selectbox("Região do Corpo:", corpo_facil + corpo_media + corpo_dificil + corpo_extrema)

# Estilo
estilo_opcoes = ["Meu Estilo", "Neo Tradicional", "Anime", "Blackwork", "Oldschool", "Aquarela", "Fineline", "Escrita"]
estilo = st.selectbox("Estilo da Tatuagem:", estilo_opcoes)

cores = st.number_input("Quantidade de cores adicionais:", min_value=0, max_value=20, value=0, step=1)

st.divider()

# --- LÓGICA DE MULTIPLICADORES ---

# 1. Multiplicador de Estilo
if estilo == "Meu Estilo": mult_estilo = 2.0
elif estilo in ["Neo Tradicional", "Anime"]: mult_estilo = 1.8
elif estilo == "Blackwork": mult_estilo = 1.5
elif estilo in ["Oldschool", "Aquarela"]: mult_estilo = 1.3
else: mult_estilo = 1.0

# 2. Multiplicador de Área / Fechamento (Equivalente à lógica de tamanho e dificuldade combinadas)
if is_fechamento:
    if tipo_fechamento in fechamento_facil: 
        mult_area = 2.0
        classe_dif = "Fácil/Padrão"
    elif tipo_fechamento in fechamento_medio: 
        mult_area = 2.6
        classe_dif = "Média"
    elif tipo_fechamento in fechamento_dificil: 
        mult_area = 3.4
        classe_dif = "Difícil"
    else: 
        mult_area = 4.5
        classe_dif = "Extrema"
    mult_regiao = 1.0 # Embutido na categoria do fechamento
else:
    # Multiplicadores de tamanho padrão para peças isoladas
    if tamanho == "PP (Até 3cm)": mult_area = 1.0
    elif tamanho == "P (4cm a 8cm)": mult_area = 1.5
    elif tamanho == "M (9cm a 14cm)": mult_area = 2.5
    elif tamanho == "G (15cm a 20cm)": mult_area = 3.5
    else: mult_area = 4.8 # GG

    # Multiplicador de Região Isolada
    if regiao in corpo_facil: mult_regiao = 1.0
    elif regiao in corpo_media: mult_regiao = 1.4
    elif regiao in corpo_dificil: mult_regiao = 1.8
    else: mult_regiao = 2.0 # Costela, Cotovelo, Joelho

# Custo de insumos por cor (multiplicado pelo número de sessões abertas)
custo_cores = cores * 30 * num_sessoes

# --- CÁLCULO ---
valor_total = (valor_base * num_sessoes * mult_estilo * mult_area * mult_regiao) + custo_cores
sua_parte = valor_total * 0.70
parte_estudio = valor_total * 0.30

# --- RESULTADOS ---
st.subheader("💰 Divisão do Orçamento")
st.metric(label="Valor Total cobrado do Cliente", value=f"R$ {valor_total:,.2f}")

col1, col2 = st.columns(2)
with col1: st.metric(label="Sua Parte (70%)", value=f"R$ {sua_parte:,.2f}")
with col2: st.metric(label="Parte do Estúdio (30%)", value=f"R$ {parte_estudio:,.2f}")

# Notas informativas adicionais na tela
if is_fechamento:
    st.caption(f"ℹ️ Complexidade do Fechamento selecionado: **{classe_dif}** (Multiplicador de Área: {mult_area})")

if num_sessoes > 1:
    st.info(f"📋 Média por Sessão: R$ {(valor_total / num_sessoes):,.2f} (Total de {num_sessoes} sessões)")

st.caption("Nota: Os multiplicadores dão prioridade máxima ao valor da arte autoral, além de considerar a dificuldade da pele, relevo e custos de bancada.")
