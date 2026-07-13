import streamlit as st

# Configuração da página do aplicativo
st.set_page_config(page_title="Calculadora de Precificação - Tattoo", page_icon="🎨", layout="centered")

st.title("🎨 Calculadora de Precificação de Tatuagens")
st.write("Insira os parâmetros abaixo para calcular o orçamento ideal do trabalho.")

st.divider()

# --- INPUTS DO USUÁRIO ---

# 1. Valor Base (Custo por hora ou valor base da sua sessão)
valor_base = st.number_input("Valor Base do seu trabalho (R$):", min_value=50, value=150, step=10)

# 2. CHAVE ATIVÁVEL: Tipo de Cobrança (Sessão vs Tamanho)
tipo_cobranca = st.radio("Forma de Cobrança:", ["Por Peça (Tamanho)", "Por Sessão / Fechamento"])

if tipo_cobranca == "Por Peça (Tamanho)":
    # 3. Tamanho (Apenas se for cobrado por peça única)
    tamanho_opcoes = ["PP (Até 3cm)", "P (4cm a 8cm)", "M (9cm a 14cm)", "G (15cm a 20cm)", "GG (21cm a 28cm)"]
    tamanho = st.selectbox("Tamanho da Tatuagem:", tamanho_opcoes)
    num_sessoes = 1
else:
    # 3. Número de Sessões (Ativado se for um projeto longo/fechamento)
    tamanho = "Sessão/Fechamento"
    num_sessoes = st.number_input("Quantidade de Sessões Estimadas:", min_value=1, value=1, step=1)

# 4. Estilo da Tatuagem (Excluindo realismo, colorido e preto/cinza)
estilo_opcoes = ["Seu Estilo", "Blackwork", "Oldschool", "Fineline", "Escrita", "Anime", "Aquarela", "Neo Tradicional"]
st.write("") # Apenas um espaçamento visual
estilo = st.selectbox("Estilo da Tatuagem:", estilo_opcoes)

# 5. Região do Corpo (Agrupadas por nível de dificuldade/dor)
corpo_facil = ["Braço parte externa", "Antebraço parte externa", "Panturrilhas"]
corpo_media = ["Mãos", "Pés", "Braço parte interna", "Antebraço parte interna", "Ombro", "Nuca", "Coxas frente", "Coxas trás", "Coxas lateral externa", "Canelas", "Lateral externa canela"]
corpo_dificil = ["Pescoço", "Peito", "Underboobs", "Barriga", "Lombar", "Coxas lateral interna", "Quadril", "Nádegas", "Lateral interna canela", "Costas parte torácica"]
corpo_extrema = ["Costela"]
corpo_fechamentos = ["Fechamento: Braço", "Fechamento: Perna", "Fechamento: Costas", "Fechamento: Torácico"]

todas_regioes = corpo_facil + corpo_media + corpo_dificil + corpo_extrema + corpo_fechamentos
regiao = st.selectbox("Região do Corpo / Localização:", todas_regioes)

# 6. Quantidade de Cores Adicionais
cores = st.number_input("Quantidade de cores adicionais:", min_value=0, max_value=20, value=0, step=1)

st.divider()

# --- LÓGICA DOS MULTIPLICADORES ---

# Multiplicador de Estilo
if estilo in ["Escrita", "Fineline"]:
    mult_estilo = 1.0
elif estilo in ["Blackwork", "Neo Tradicional"]:
    mult_estilo = 1.5
else:  # Seu Estilo, Oldschool, Anime, Aquarela
    mult_estilo = 1.3

# Multiplicador de Região do Corpo
if regiao in corpo_facil:
    mult_corpo = 1.0
elif regiao in corpo_media:
    mult_corpo = 1.2
elif regiao in corpo_dificil:
    mult_corpo = 1.4
else:  # Costela ou Fechamentos complexos
    mult_corpo = 1.6

# Custo fixo estimado por cor adicional (multiplicado pelo número de sessões, pois gasta material a cada abertura de bancada)
custo_cores = cores * 30 * num_sessoes

# --- CÁLCULO FINAL ---
if tipo_cobranca == "Por Sessão / Fechamento":
    # Multiplica o valor base pelo número de sessões estimadas e aplica a complexidade da região/estilo
    valor_total = (valor_base * num_sessoes * mult_estilo * mult_corpo) + custo_cores
else:
    # Lógica padrão baseada nos tamanhos em cm
    if tamanho == "PP (Até 3cm)":
        mult_tamanho = 1.0
    elif tamanho == "P (4cm a 8cm)":
        mult_tamanho = 1.5
    elif tamanho == "M (9cm a 14cm)":
        mult_tamanho = 2.5
    elif tamanho == "G (15cm a 20cm)":
        mult_tamanho = 4.0
    else:  # GG (21cm a 28cm)
        mult_tamanho = 6.0
        
    valor_total = (valor_base * mult_tamanho * mult_estilo * mult_corpo) + custo_cores

# Divisão dos 70%
sua_parte = valor_total * 0.70

# --- EXIBIÇÃO DOS RESULTADOS ---
st.subheader("💰 Orçamento Calculado")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Valor Total para o Cliente", value=f"R$ {valor_total:,.2f}")

with col2:
    st.metric(label="Sua Parte (70%)", value=f"R$ {sua_parte:,.2f}")

# Caso seja parcelado por sessões, mostra quanto custará em média cada sessão para o cliente
if tipo_cobranca == "Por Sessão / Fechamento" and num_sessoes > 1:
    st.info(f"📋 Média por Sessão: R$ {(valor_total / num_sessoes):,.2f} (Total de {num_sessoes} sessões)")

st.caption("Nota: Os multiplicadores levam em conta a complexidade do estilo, dificuldade da pele e os custos repetíveis a cada sessão.")
