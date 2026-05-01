import streamlit as st
from logic import formatar_hda, calcular_glasgow, formatar_relatorio_final

# ... (Aqui entra todo o código de st.markdown, st.columns e st.button que já criamos)

# Exemplo de como chamar o back-end no botão final:
if st.button("GERAR RELATÓRIO FINAL"):
    hda_texto = formatar_hda(origem, st.session_state.queixa_sel, caract_selecionadas, tempo_inicio)
    
    # Prepara dicionário para o back-end
    dados_paciente = {
        "nome": nome, "idade": idade, "hda": hda_texto, 
        "hpp": ", ".join(hpp), "muc": muc, "alergias": alergias,
        "fc": fc, "sat": sat, "pa": pa_v, "fr": fr, "gli": gli,
        "tipo_ef": st.session_state.tipo_ef, "ef_texto": ef_final_txt,
        "pocus": pocus, "ecg": ecg
    }
    
    relatorio = formatar_relatorio_final(dados_paciente)
    st.code(relatorio, language=None)
