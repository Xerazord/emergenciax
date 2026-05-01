import streamlit as st

st.set_page_config(page_title="Emergência Pro", layout="wide")

# --- ESTILIZAÇÃO CUSTOMIZADA (BOTÕES AZUIS E FOCO) ---
st.markdown("""
    <style>
    /* Estilo para botões de Queixa e Exame Físico */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #1E88E5;
        color: white !important;
        font-weight: bold;
        border: none;
        margin-bottom: 10px;
    }
    div.stButton > button:hover {
        background-color: #1565C0;
        border: 1px solid white;
    }
    /* Títulos de seções */
    .section-head {
        background-color: #f0f2f6;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #1E88E5;
        margin: 15px 0;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Admissão de Emergência Dinâmica")

# --- 1. IDENTIFICAÇÃO E ORIGEM ---
with st.container():
    nome = st.text_input("Nome do Paciente")
    idade = st.slider("Idade do Paciente", 0, 110, 30)
    origem = st.selectbox("Origem do Paciente", ["Demanda Espontânea", "SAMU", "Bombeiros", "Vaga Zero", "Transferência"])

# --- 2. QUEIXA PRINCIPAL (LÓGICA DE REDUÇÃO E FOCO) ---
st.subheader("Queixa Principal")

lista_queixas = [
    "Dor torácica", "Dispneia", "Tosse", "Febre", "Dor abdominal", "Sangramento",
    "Dor lombar", "Dor em membros inferiores", "Edema de membros inferiores",
    "Déficit neurológico agudo", "Vertigem", "Cefaleia", "Rebaixamento do nível de consciência",
    "Agitação psicomotora", "Convulsão", "Síncope", "Trauma"
]

# Inicialização do estado
if 'queixa_sel' not in st.session_state: st.session_state.queixa_sel = None

# Se nenhuma queixa foi selecionada, mostra todas. Se selecionou, mostra apenas a escolhida (redução).
if st.session_state.queixa_sel is None:
    q_cols = st.columns(3)
    for i, q in enumerate(lista_queixas):
        if q_cols[i % 3].button(q):
            st.session_state.queixa_sel = q
            st.rerun()
else:
    col_sel, col_reset = st.columns([3, 1])
    col_sel.info(f"Queixa Selecionada: **{st.session_state.queixa_sel}**")
    if col_reset.button("🔄 Mudar Queixa"):
        st.session_state.queixa_sel = None
        st.rerun()

    # --- DICIONÁRIO DE CARACTERÍSTICAS CONDICIONAIS ---
    opcoes_dict = {
        "Dor torácica": ["Opressiva", "Pleurítica", "Irradiação MMSS", "Sudorese", "Piora ao esforço", "Início súbito"],
        "Déficit neurológico agudo": ["Hemiparesia", "Afasia", "Desvio de rima", "Janela < 4.5h", "Hemihipoestesia"],
        "Dor abdominal": ["Difusa", "Sinal de Murphy", "Defesa abdominal", "Descompressão Dolorosa", "Náuseas/Vômitos"],
        "Dispneia": ["Uso de musculatura acessória", "Sibilos", "Crepitações", "Ortopneia", "Início súbito"],
        "Trauma": ["Mecanismo de alta energia", "Queda de nível", "Atropelamento", "Trauma craniano", "Vítima de agressão"]
    }
    
    lista_opcoes = opcoes_dict.get(st.session_state.queixa_sel, ["Início súbito", "Piora progressiva", "Sintomas persistentes"])
    
    st.markdown("<div class='section-head'>🔍 Detalhes da Queixa</div>", unsafe_allow_html=True)
    caract_selecionadas = st.multiselect(f"Características de {st.session_state.queixa_sel}:", lista_opcoes)
    tempo_inicio = st.text_input("Tempo de início (Ex: 2 horas, 30 min)")

# --- 3. ANTECEDENTES E SSVV ---
with st.expander("Dados Clínicos e Sinais Vitais"):
    hpp = st.multiselect("HPP", ["HAS", "DM2", "ICC", "AVC", "DAC", "IRC", "DPOC"])
    muc = st.text_input("Medicações em uso")
    alergias = st.text_input("Alergias", "Nega")
    c1, c2, c3, c4, c5 = st.columns(5)
    fc = c1.text_input("FC")
    sat = c2.text_input("Sat")
    pa_v = c3.text_input("PA")
    fr = c4.text_input("FR")
    gli = c5.text_input("Glic")

# --- 4. EXAME FÍSICO CONDICIONAL ---
st.subheader("Exame Físico")
if 'tipo_ef' not in st.session_state: st.session_state.tipo_ef = None

ef_col1, ef_col2 = st.columns(2)
if ef_col1.button("Ambulatorial"): st.session_state.tipo_ef = "Ambulatorial"
if ef_col2.button("Paciente Crítico (ABCDE)"): st.session_state.tipo_ef = "Crítico"

ef_final_txt = ""

if st.session_state.tipo_ef == "Ambulatorial":
    st.markdown("<div class='section-head'>📋 Padrão Ambulatorial</div>", unsafe_allow_html=True)
    g = st.text_input("-GERAL:")
    cv = st.text_input("-AP CV:")
    re = st.text_input("-AR RESPIRATÓRIO:")
    ab = st.text_input("-ABDOME:")
    ne = st.text_input("-NEURO:")
    pe = st.text_input("-PELE E MMII:")
    ef_final_txt = f"-GERAL: {g}\n-AP CV: {cv}\n-AR RESP: {re}\n-ABD: {ab}\n-NEURO: {ne}\n-PELE/MMII: {pe}"

elif st.session_state.tipo_ef == "Crítico":
    st.markdown("<div class='section-head'>🚨 Padrão Crítico (ABCDE)</div>", unsafe_allow_html=True)
    
    # A - VIA AÉREA
    with st.expander("A - Via Aérea", expanded=True):
        va_estado = st.radio("Estado da VA:", ["Pérvia e Patente", "Obstruída"], horizontal=True)
        fonacao = st.radio("Fonação:", ["Preservada", "Prejudicada/Ausente"], horizontal=True)
        colar = st.radio("Colar Cervical:", ["Não indicado", "Colocado/Mantido"], horizontal=True)
        a_txt = f"VA {va_estado.lower()}, fonação {fonacao.lower()}. Colar cervical: {colar.lower()}."

    # B - RESPIRAÇÃO
    with st.expander("B - Respiração", expanded=True):
        b_simetria = st.radio("Expansibilidade:", ["Simétrica", "Assimétrica"], horizontal=True)
        mv = st.radio("Murmúrio Vesicular:", ["Presente e Simétrico", "Reduzido", "Abolido"], horizontal=True)
        ruidos = st.multiselect("Ruídos Adventícios:", ["Crépitos", "Sibilos"])
        esforco = st.multiselect("Esforço/Padrão:", ["Taquipneia", "Dispneia", "Uso de musculatura acessória"])
        ferimentos = st.text_input("Ferimentos/Assimetrias:")
        padrao_resp = "Normal"
        if "Taquipneia" in esforco and "Dispneia" in esforco: padrao_resp = "Taquidispneia"
        elif "Taquipneia" in esforco: padrao_resp = "Taquipneia"
        elif "Dispneia" in esforco: padrao_resp = "Dispneia"
        b_txt = f"Tórax {b_simetria.lower()}, MV {mv.lower()}. {padrao_resp}. Ruídos: {', '.join(ruidos)}. {ferimentos}"

    # C - CIRCULAÇÃO
    with st.expander("C - Circulação", expanded=True):
        tec = st.radio("TEC:", ["< 3 segundos", "> 3 segundos", "> 5 segundos", "Em flush"], horizontal=True)
        ausculta = st.multiselect("Ausculta Cardíaca:", ["Regular", "Irregular", "Reduzida", "Abolida", "Sopro grosseiro"])
        pulsos = st.radio("Pulsos Periféricos:", ["Simétricos", "Assimétricos/Filiformes"], horizontal=True)
        abd_clinico = st.multiselect("Abdome:", ["Flácido", "Dor à palpação", "Defesa", "Descompressão dolorosa"])
        c_txt = f"TEC {tec}. Ausculta: {', '.join(ausculta)}. Pulsos {pulsos.lower()}. PA: {pa_v}. Abdome: {', '.join(abd_clinico)}."

    # D - NEUROLÓGICO
    with st.expander("D - Neurológico", expanded=True):
        c_oc, c_verb, c_mot = st.columns(3)
        ao = c_oc.selectbox("Abertura Ocular", [4, 3, 2, 1])
        rv = c_verb.selectbox("Resposta Verbal", [5, 4, 3, 2, 1])
        rm = c_mot.selectbox("Resposta Motora", [6, 5, 4, 3, 2, 1])
        pupilas = st.radio("Pupilas:", ["Isocóricas e Reativas", "Anisocóricas", "Midriáticas", "Mióticas", "Não reagentes"], horizontal=True)
        tem_deficit = st.checkbox("Presença de Déficit Neurológico?")
        deficits = st.multiselect("Déficits:", ["Hemiparesia", "Hemihipoestesia", "Paralisia facial central", "Paralisia facial periférica", "Disartria", "Vertigem"]) if tem_deficit else []
        d_txt = f"GCS: {ao+rv+rm} (O:{ao} V:{rv} M:{rm}). Pupilas {pupilas.lower()}. Déficits: {', '.join(deficits) if deficits else 'Nega'}."

    # E - EXPOSIÇÃO
    with st.expander("E - Exposição / Adicional", expanded=True):
        edema = st.radio("Edema MMII:", ["Ausente", "Presente"], horizontal=True)
        cacifo = st.radio("Cacifo:", ["Com cacifo", "Sem cacifo"], horizontal=True) if edema == "Presente" else ""
        pele_mmii = st.multiselect("Achados:", ["Palidez", "Frialdade", "Lesões"])
        e_txt = f"Edema MMII: {edema} {cacifo}. Pele: {', '.join(pele_mmii)}."
    
    ef_final_txt = f"-A: {a_txt}\n-B: {b_txt}\n-C: {c_txt}\n-D: {d_txt}\n-E: {e_txt}"

# --- 5. RESULTADO ---
st.markdown("<div class='section-head'>📋 Registro Final</div>", unsafe_allow_html=True)
pocus = st.text_input("POCUS")
ecg = st.text_area("ECG")

if st.button("GERAR RELATÓRIO FINAL"):
    hda = f"Paciente admitido via {origem}, com quadro de {st.session_state.queixa_sel}. Início há {tempo_inicio}. "
    if 'caract_selecionadas' in locals() and caract_selecionadas: hda += f"Apresenta {', '.join(caract_selecionadas).lower()}."
    
    relatorio = f"""## Admissão em Sala de Emergência ##
# ID: {nome}, {idade} anos.
# HDA: {hda}
# HPP: {', '.join(hpp)} | MUC: {muc} | Alergias: {alergias}
# SSVV: FC: {fc} | SatO2: {sat} | PA: {pa_v} | FR: {fr} | Glic: {gli}
# EF ({st.session_state.tipo_ef}):
{ef_final_txt}
# POCUS: {pocus} | # ECG: {ecg}"""
    st.code(relatorio, language=None)
