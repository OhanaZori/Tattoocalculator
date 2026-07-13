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

if is_fechamento:
    # Lista de Fechamentos
    fechamentos_lista = [
        "Pescoço", "Braço superior externo", "Braço superior interno", "Braço superior completo",
        "Antebraço externo", "Antebraço interno", "Antebraço completo", "Braço externo",
        "Braço interno", "Braço completo", "Costas", "Costela", "Torax", "Coxa frontal",
        "Coxa traseira", "Coxa lateral externa", "Coxa lateral interna", "Coxa completa",
        "Canela", "Panturrilha", "Panturrilha lateral externa", "Panturrilha lateral interna",
        "Perna inferior completo", "Perna completa"
    ]
    tipo_fechamento = st.selectbox("Qual o Fechamento?", fechamentos_lista)
    tamanho = "Fechamento"
    regiao = "Fechamento"
else:
    # Inputs tradicionais
    tamanho_opcoes = ["PP (Até 3cm)", "P (4cm a 8cm)", "M (9cm a 14cm)", "G (15cm a 20cm)", "GG (21cm a 28cm)"]
    tamanho = st.selectbox("Tamanho da Tatuagem:", tamanho_opcoes)
    
    corpo_facil = ["Braço parte externa", "Antebraço parte externa", "Panturrilhas"]
    corpo_media = ["Mãos", "Pés", "Braço parte interna", "Antebraço parte interna", "Ombro", "Nuca", "Coxas frente", "Coxas trás", "Coxas lateral externa", "Canelas", "Lateral externa canela"]
    corpo_dificil = ["Pescoço", "Peito", "Underboobs", "Barriga", "Lombar", "Coxas lateral interna", "Quadril", "Nádegas", "Lateral interna canela", "Costas parte torácica"]
    corpo_extrema = ["Costela", "Cotovelo", "Joelho"]
    
    regiao = st.selectbox("Região do Corpo:", corpo_facil + corpo_media + corpo_dificil + corpo_extrema)

# Estilo
estilo_opcoes = ["Seu Estilo (Autoral)", "Neo Tradicional", "Anime", "Blackwork", "Oldschool", "Aquarela", "Fineline", "Escrita"]
estilo = st.selectbox("Estilo da Tatuagem:", estilo_opcoes)

cores = st.number_input("Quantidade de cores adicionais:", min_value=0, max_value=20, value=0, step=1)

st.divider()

# --- LÓGICA DE MULTIPLICADORES ---

# Multiplicador de Estilo
if estilo == "Seu Estilo (Autoral)": mult_estilo = 2.0
elif estilo in ["Neo Tradicional", "Anime"]: mult_estilo = 1.8
elif estilo == "Blackwork": mult_estilo = 1.5
elif estilo in ["Oldschool", "Aquarela"]: mult_estilo = 1.3
else: mult_estilo = 1.0

# Multiplicador de Área/Corpo
if is_fechamento:
    # Multiplicadores baseados na magnitude do fechamento
    if tipo_fechamento in ["Costas", "Perna completa", "Braço completo"]: mult_area = 3.5
    elif tipo_fechamento in ["Torax", "Coxa completa", "Perna inferior completo"]: mult_area = 2.8
    else: mult_area = 2.0 # Fechamentos menores
else:
    # Multiplicadores de tamanho padrão
    if tamanho == "PP (Até 3cm)": mult_area = 1.0
    elif tamanho == "P (4cm a 8cm)": mult_area = 1.5
    elif tamanho == "M (9cm a 14cm)": mult_area = 2.5
    elif tamanho == "G (15cm a 20cm)": mult_area = 4.0
    else: mult_area = 6.0 # GG

# Multiplicador de Região (Para peça única apenas)
if not is_fechamento:
    if regiao in ["Braço parte externa", "Antebraço parte externa", "Panturrilhas"]: mult_regiao = 1.0
    elif regiao in ["Mãos", "Pés", "Braço parte interna", "Antebraço parte interna", "Ombro", "Nuca", "Coxas frente", "Coxas trás", "Coxas lateral externa", "Canelas", "Lateral externa canela"]: mult_regiao = 1.2
    elif regiao in ["Pescoço", "Peito", "Underboobs", "Barriga", "Lombar", "Coxas lateral interna", "Quadril", "Nádegas", "Lateral interna canela", "Costas parte torácica"]: mult_regiao = 1.4
    else: mult_regiao = 1.6 # Costela, Cotovelo, Joelho
else:
    mult_regiao = 1.0 # Já embutido no multiplicador de área do fechamento

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

if num_sessoes > 1:
    st.info(f"📋 Média por Sessão: R$ {(valor_total / num_sessoes):,.2f} (Total de {num_sessoes} sessões)")
