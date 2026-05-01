def formatar_hda(origem, queixa, caracteristicas, tempo):
    texto = f"Paciente admitido via {origem}, com quadro de {queixa}. Início há {tempo}. "
    if caracteristicas:
        texto += f"Apresenta {', '.join(caracteristicas).lower()}."
    return texto

def calcular_glasgow(ao, rv, rm):
    return ao + rv + rm

def formatar_relatorio_final(dados):
    # Recebe um dicionário com todos os campos e monta o template
    relatorio = f"""## Admissão em Sala de Emergência ##
# ID: {dados['nome']}, {dados['idade']} anos.
# HDA: {dados['hda']}
# HPP: {dados['hpp']} | MUC: {dados['muc']} | Alergias: {dados['alergias']}
# SSVV: FC: {dados['fc']} | SatO2: {dados['sat']} | PA: {dados['pa']} | FR: {dados['fr']} | Glic: {dados['gli']}
# EF ({dados['tipo_ef']}):
{dados['ef_texto']}
# POCUS: {dados['pocus']} | # ECG: {dados['ecg']}"""
    return relatorio
