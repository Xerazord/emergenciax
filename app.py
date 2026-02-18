import streamlit as st

st.set_page_config(page_title="Emergência Pro - Condicional", layout="centered")

# --- ESTILIZAÇÃO PARA BOTÕES (LAYOUT DE GRID) ---
st.markdown("""
    <style>
    div.stButton > button:first-child { width: 100%; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Admissão de Emergência Dinâmica")

# --- 1. IDENTIFICAÇÃO E ORIGEM ---
with st.container():
    nome = st.text_input("Nome do Paciente")
    idade = st.number_input("Idade", min_value=0, max_value=120)
    origem = st.selectbox("Origem do Paciente", 
                         ["Demanda Espontânea", "SAMU", "Bombeiros", "Vaga Zero", "Transferência"])

# --- 2. QUEIXA PRINCIPAL (BOTÕES CLICÁVEIS) ---
st.subheader("Selecione a Queixa Principal")
lista_queixas = [
    "Dor torácica", "Dispneia", "Tosse", "Febre", "Dor abdominal", "Sangramento",
    "Dor lombar", "Dor em membros inferiores", "Edema de membros inferiores",
    "Déficit neurológico agudo", "Vertigem", "Cefaleia", "Rebaixamento do nível de consciência",
    "Agitação psicomotora", "Convulsão", "Síncope", "Trauma"
]

# Inicializa a queixa na sessão se não existir
if 'queixa_selecionada' not in st.session_state:
    st.session_state.queixa_selecionada = None

# Cria um grid de botões (3 colunas)
cols = st.columns(3)
for i, q in enumerate(lista_queixas):
    if cols[i % 3].button(q):
        st.session_state.queixa_selecionada = q

# --- 3. CARACTERÍSTICAS CONDICIONAIS ---
caracteristicas = []
if st.session_state.queixa_selecionada:
    st.info(f"Queixa Selecionada: **{st.session_state.queixa_selecionada}**")
    
    # Dicionário de opções específicas por queixa
    opcoes_especificas = {
        "Dor torácica": ["Opressiva", "Pleurítica", "Irradiação MMSS", "Sudorese", "Piora ao esforço"],
        "Déficit neurológico agudo": ["Hemiparesia", "Afasia", "Desvio de rima", "Início súbito", "Janela < 4.5h"],
        "Dor abdominal": ["Difusa", "Localizada em FID", "Sinal de Murphy", "Defesa abdominal", "Nauseas/Vomitos"],
        "Dispneia": ["Uso de musculatura acessória", "Sibilos", "Crepitações", "Ortopneia", "Súbita"],
        "Trauma": ["Mecanismo de alta energia", "Queda de nível", "Acidente MOT x AUTO", "Trauma craniano"]
        # Você pode adicionar as outras aqui seguindo o mesmo padrão
    }
    
    # Busca as opções no dicionário (ou usa uma lista padrão se não houver específica ainda)
    lista_opcoes = opcoes_especificas.get(st.session_state.queixa_selecionada, ["Início súbito", "Sintomas persistentes", "Piora progressiva"])
    
    caracteristicas = st.multiselect(f"Características de {st.session_state.queixa_selecionada}:", lista_opcoes)
    tempo_inicio = st.text_input("Tempo de início da queixa")

# --- 4. OUTROS CAMPOS (CHECKLISTS RÁPIDOS) ---
with st.expander("Antecedentes e Sinais Vitais"):
    hpp = st.multiselect("HPP", ["HAS", "DM2", "ICC", "AVC", "DAC", "IRC", "DPOC"])
    muc = st.text_input("Medicações em uso")
    alergias = st.text_input("Alergias", "Nega")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    fc = c1.text_input("FC")
    sat = c2.text_input("Sat")
    pa = c3.text_input("PA")
    fr = c4.text_input("FR")
    gli = c5.text_input("Glic")

with st.expander("Exames Beira-Leito (POCUS/ECG)"):
    ef_tipo = st.radio("EF:", ["Geral", "Crítico"], horizontal=True)
    ef_achados = st.text_area("Achados Exame Físico")
    pocus = st.text_input("POCUS (C/P/A)", "Normal")
    ecg = st.text_input("ECG", "Ritmo Sinusal")

# --- 5. GERAÇÃO DO TEXTO ESTRUTURADO ---
if st.button("GERAR RELATÓRIO", type="primary"):
    # Lógica para compor a HDA incluindo a Origem conforme solicitado
    hda_composta = f"Paciente admitido via {origem}, com quadro de {st.session_state.queixa_selecionada}. "
    if caracteristicas:
        hda_composta += f"Apresenta-se com {', '.join(caracteristicas).lower()}. "
    hda_composta += f"Início dos sintomas há {tempo_inicio}."

    relatorio = f"""## Admissão em Sala de Emergência ##

# ID: {nome}, {idade} anos.

# HDA: {hda_composta}

# HPP: {', '.join(hpp)}
# MUC: {muc}
Alergias: {alergias}

# SSVV:
- FC: {fc} bpm - SatO2: {sat}% - PA: {pa} - FR: {fr} - Glicemia: {gli} mg/dL

# EF ({ef_tipo}):
{ef_achados}

# POCUS: {pocus}
# ECG: {ecg}
"""
    st.divider()
    st.code(relatorio, language=None)
