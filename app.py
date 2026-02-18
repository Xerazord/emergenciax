import streamlit as st

st.set_page_config(page_title="Emergência Pro - Protocolo ABCDE", layout="wide")

# Estilização
st.markdown("""
    <style>
    div.stButton > button:first-child { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    .stSelectbox label, .stMultiSelect label, .stRadio label { font-weight: bold; color: #1E88E5; }
    .section-head { background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Registro de Emergência Avançado")

# --- 1. IDENTIFICAÇÃO E ORIGEM ---
with st.container():
    nome = st.text_input("Nome do Paciente")
    idade = st.slider("Idade do Paciente", 0, 110, 30)
    origem = st.selectbox("Origem do Paciente", ["Demanda Espontânea", "SAMU", "Bombeiros", "Vaga Zero", "Transferência"])

# --- 2. QUEIXA PRINCIPAL (BOTÕES) ---
st.subheader("Queixa Principal")
lista_queixas = [
    "Dor torácica", "Dispneia", "Tosse", "Febre", "Dor abdominal", "Sangramento",
    "Dor lombar", "Dor em membros inferiores", "Edema de membros inferiores",
    "Déficit neurológico agudo", "Vertigem", "Cefaleia", "Rebaixamento do nível de consciência",
    "Agitação psicomotora", "Convulsão", "Síncope", "Trauma"
]

if 'queixa_sel' not in st.session_state: st.session_state.queixa_sel = None
q_cols = st.columns(4)
for i, q in enumerate(lista_queixas):
    if q_cols[i % 4].button(q):
        st.session_state.queixa_sel = q

caract_selecionadas = []
tempo_inicio = ""
if st.session_state.queixa_sel:
    st.info(f"Selecionado: **{st.session_state.queixa_sel}**")
    tempo_inicio = st.text_input("Tempo de início")

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
if ef_col1.button("Exame Físico Ambulatorial"): st.session_state.tipo_ef = "Ambulatorial"
if ef_col2.button("Exame Físico do Paciente Crítico"): st.session_state.tipo_ef = "Crítico"

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
    
    # --- ITEM A ---
    with st.expander("A - Via Aérea", expanded=True):
        va_estado = st.radio("Estado da VA:", ["Pérvia e Patente", "Obstruída"], horizontal=True)
        fonacao = st.radio("Fonação:", ["Preservada", "Prejudicada/Ausente"], horizontal=True)
        colar = st.radio("Colar Cervical:", ["Não indicado", "Colocado/Mantido"], horizontal=True)
        a_txt = f"VA {va_estado.lower()}, fonação {fonacao.lower()}. Colar cervical: {colar.lower()}."

    # --- ITEM B ---
    with st.expander("B - Respiração", expanded=True):
        b_simetria = st.radio("Expansibilidade:", ["Simétrica", "Assimétrica"], horizontal=True)
        mv = st.radio("Murmúrio Vesicular:", ["Presente e Simétrico", "Reduzido", "Abolido"], horizontal=True)
        ruidos = st.multiselect("Ruídos Adventícios:", ["Crépitos", "Sibilos"])
        esforco = st.multiselect("Esforço/Padrão:", ["Taquipneia", "Dispneia", "Uso de musculatura acessória"])
        ferimentos = st.text_input("Ferimentos torácicos/Assimetrias específicas:")
        
        # Lógica Taquidispneia
        padrao_resp = "Normal"
        if "Taquipneia" in esforco and "Dispneia" in esforco: padrao_resp = "Taquidispneia"
        elif "Taquipneia" in esforco: padrao_resp = "Taquipneia"
        elif "Dispneia" in esforco: padrao_resp = "Dispneia"
        
        b_txt = f"Tórax {b_simetria.lower()}, MV {mv.lower()}. {padrao_resp}. Ruídos: {', '.join(ruidos) if ruidos else 'nfn'}. Musc. acessória: {'Sim' if 'Uso de musculatura acessória' in esforco else 'Não'}. {ferimentos}"

    # --- ITEM C ---
    with st.expander("C - Circulação", expanded=True):
        tec = st.radio("TEC:", ["< 3 segundos", "> 3 segundos", "> 5 segundos", "Em flush"], horizontal=True)
        ausculta = st.multiselect("Ausculta Cardíaca:", ["Regular", "Irregular", "Reduzida", "Abolida", "Sopro grosseiro"])
        pulsos = st.radio("Pulsos Periféricos:", ["Simétricos", "Assimétricos/Filiformes"], horizontal=True)
        abd_clinico = st.multiselect("Abdome:", ["Flácido", "Dor à palpação", "Defesa", "Descompressão dolorosa"])
        c_txt = f"TEC {tec}. Ausculta: {', '.join(ausculta)}. Pulsos {pulsos.lower()}. PA: {pa_v}. Abdome: {', '.join(abd_clinico)}."

    # --- ITEM D ---
    with st.expander("D - Neurológico", expanded=True):
        c_oc, c_verb, c_mot = st.columns(3)
        ao = c_oc.selectbox("Abertura Ocular (GCS)", [4, 3, 2, 1])
        rv = c_verb.selectbox("Resposta Verbal (GCS)", [5, 4, 3, 2, 1])
        rm = c_mot.selectbox("Resposta Motora (GCS)", [6, 5, 4, 3, 2, 1])
        pupilas = st.radio("Pupilas:", ["Isocóricas e Reativas", "Anisocóricas", "Midriáticas", "Mióticas", "Fotorreagentes", "Não reagentes"], horizontal=True)
        tem_deficit = st.checkbox("Presença de Déficit Neurológico?")
        deficits = []
        if tem_deficit:
            deficits = st.multiselect("Déficits detectados:", ["Hemiparesia", "Hemihipoestesia", "Paralisia facial central", "Paralisia facial periférica", "Disartria", "Disfonia", "Disfagia", "Vertigem"])
        d_txt = f"GCS: {ao+rv+rm} (O:{ao} V:{rv} M:{rm}). Pupilas {pupilas.lower()}. Déficits: {', '.join(deficits) if deficits else 'Nega'}."

    # --- ITEM E ---
    with st.expander("E - Exposição / Adicional", expanded=True):
        edema = st.radio("Edema MMII:", ["Ausente", "Presente"], horizontal=True)
        cacifo = st.radio("Cacifo:", ["Com cacifo", "Sem cacifo"], horizontal=True) if edema == "Presente" else ""
        pele_mmii = st.multiselect("Achados Adicionais:", ["Palidez", "Frialdade de membros", "Lesões em membros"])
        e_txt = f"Edema MMII: {edema} {cacifo}. Pele/Membros: {', '.join(pele_mmii)}."
    
    ef_final_txt = f"-A: {a_txt}\n-B: {b_txt}\n-C: {c_txt}\n-D: {d_txt}\n-E: {e_txt}"

# --- 5. EXAMES E RESULTADO ---
with st.expander("Exames Complementares"):
    pocus = st.text_input("POCUS (Cardio/Pulm/Abd/MMII)")
    ecg = st.text_area("Achados de ECG")

if st.button("GERAR RELATÓRIO FINAL", type="primary"):
    hda = f"Paciente admitido via {origem}, com quadro de {st.session_state.queixa_sel}. Início há {tempo_inicio}."
    
    relatorio = f"""## Admissão em Sala de Emergência ##

# ID: {nome}, {idade} anos.

# HDA: {hda}

# HPP: {', '.join(hpp)}
# MUC: {muc}
Alergias: {alergias}

# SSVV:
- FC: {fc} bpm - SatO2: {sat}% - PA: {pa_v} - FR: {fr} - Glicemia: {gli} mg/dL

# EF ({st.session_state.tipo_ef}):
{ef_final_txt}

# POCUS: {pocus}
# ECG: {ecg}
"""
    st.divider()
    st.code(relatorio, language=None)
