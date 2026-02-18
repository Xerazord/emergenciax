import streamlit as st

st.set_page_config(page_title="Emergência Pro - Checklist", layout="centered")

st.title("🏥 Registro Estruturado de Emergência")

# --- SEÇÃO 1: IDENTIFICAÇÃO (Texto Livre) ---
with st.expander("🆔 Identificação", expanded=True):
    nome = st.text_input("Nome do Paciente")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    origem = st.selectbox("Origem do Paciente", ["Demanda Espontânea", "SAMU", "Bombeiros", "Transferência Inter-hospitalar", "Outro"])

# --- SEÇÃO 2: HDA COM CHECKLIST ---
with st.expander("📝 História da Doença Atual (HDA)"):
    tempo_inicio = st.select_slider("Tempo de início", options=["< 1h", "1-6h", "6-12h", "12-24h", "> 24h", "Crônico"])
    
    tipo_queixa = st.multiselect("Tipo de Queixa (Selecione)", 
        ["Dor Torácica", "Dispneia", "Déficit Neurológico", "Dor Abdominal", "Trauma", "Síncope", "Febre", "Cefaleia"])
    
    caract_queixa = st.multiselect("Características/Sintomas (Checklist)",
        ["Opressiva", "Pleurítica", "Irradiação para MMSS", "Sudorese associada", "Náuseas/Vômitos", 
         "Piora ao esforço", "Início súbito", "Palpitações", "Cianose", "Uso de musculatura acessória"])
    
    hda_obs = st.text_input("Nota adicional HDA (opcional)")

# --- SEÇÃO 3: ANTECEDENTES COM CHECKLIST ---
with st.expander("💊 HPP, MUC e Alergias"):
    hpp_check = st.multiselect("Doenças Prévias (HPP)", 
        ["HAS", "DM2", "ICC", "DAC (Infarto Prévio)", "Fibrilação Atrial", "DPOC/Asma", "IRC (Diálise)", "AVC Prévio", "Neoplasia"])
    
    muc_check = st.multiselect("Medicações em Uso (MUC)",
        ["Anti-hipertensivos", "Insulina/Antidiabéticos", "Anticoagulante Oral", "Antiagregante (AAS/Clopidogrel)", "Bombinha/Corticoide", "Diuréticos", "Estatina"])
    
    alergias_check = st.radio("Alergias?", ["Nega", "Medicamentosa", "Látex", "Contraste Iodado"], horizontal=True)
    alergia_detalhe = st.text_input("Qual alergia?") if alergias_check != "Nega" else ""

# --- SEÇÃO 4: SINAIS VITAIS (Valores Numéricos) ---
with st.expander("📊 Sinais Vitais (SSVV)"):
    col1, col2 = st.columns(2)
    fc = col1.text_input("FC (bpm)")
    sat = col2.text_input("SatO2 (%)")
    pa = col1.text_input("PA (mmHg)")
    fr = col2.text_input("FR (irpm)")
    glicemia = col1.text_input("Glicemia (mg/dL)")

# --- SEÇÃO 5: EXAME FÍSICO COM CHECKLIST ---
with st.expander("🩺 Exame Físico (EF)"):
    tipo_ef = st.radio("Padrão de Exame:", ["Exame Geral", "Paciente Crítico (ABCDE)"], horizontal=True)
    
    ef_achados = st.multiselect("Achados Positivos",
        ["B1 e B2 Bulhas Normofonéticas", "Sopro Cardíaco", "MV Presente e Simétrico", "Estertores Crepitantes", 
         "Sibilos", "Abdomen Inocente", "Dor à descompressão", "RNC (Rebaixamento)", "Anisocoria", "Pulsos Periféricos Simétricos"])

# --- SEÇÃO 6: POCUS E ECG COM CHECKLIST ---
with st.expander("📡 Exames à Beira-Leito"):
    st.markdown("**POCUS**")
    pocus_c = st.selectbox("Cardíaco", ["Normal", "Disfunção VE", "Derrame Pericárdico", "VD Dilatado", "VCI Fixa/Dilatada"])
    pocus_p = st.selectbox("Pulmonar", ["Deslizamento Pleural (+)", "Linhas B (Sindrome Intersticial)", "Derrame Pleural", "Pneumotórax (Lung Point)"])
    pocus_a = st.selectbox("Abdominal", ["Livre de líquido (FAST -)", "Líquido livre (FAST +)", "Aorta normal"])
    
    st.markdown("**ECG**")
    ecg_check = st.multiselect("Achados ECG", 
        ["Ritmo Sinusal", "Supra de ST", "Infra de ST", "Inversão de Onda T", "Bloqueio de Ramo", "Taquicardia", "Bradicardia", "Fibrilação Atrial"])

# --- PROCESSAMENTO DO RELATÓRIO ---
if st.button("GERAR RELATÓRIO FINAL", type="primary"):
    
    # Formatação das listas para texto
    hda_txt = ", ".join(tipo_queixa) + " (" + ", ".join(caract_queixa) + ") " + hda_obs
    hpp_txt = ", ".join(hpp_check) if hpp_check else "Sem comorbidades relatadas"
    muc_txt = ", ".join(muc_check) if muc_check else "Nega uso de medicações"
    ef_txt = ", ".join(ef_achados)
    ecg_txt = ", ".join(ecg_check)
    alergia_final = f"{alergias_check}: {alergia_detalhe}" if alergia_detalhe else alergias_check

    relatorio = f"""## Admissão em Sala de Emergência ##

# ID: {nome}, {idade} anos. Origem: {origem}.

# HDA: {hda_txt}. Início há aproximadamente {tempo_inicio}.

# HPP: {hpp_txt}

# MUC: {muc_txt}
Alergias: {alergia_final}

# SSVV:
- FC: {fc} bpm - SatO2: {sat}% - PA: {pa} - FR: {fr} - Glicemia: {glicemia}

# EF ({tipo_ef}):
{ef_txt}

# POCUS:
- Cardíaco: {pocus_c} | Pulmonar: {pocus_p}
- Abdominal: {pocus_a} | MMII/Outros: Normal

# ECG:
{ecg_txt}
"""
    st.divider()
    st.subheader("📋 Texto Pronto para Cópia")
    st.code(relatorio, language=None)
