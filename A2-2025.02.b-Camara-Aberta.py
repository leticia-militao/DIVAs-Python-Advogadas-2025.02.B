# Configuração inicial do programa - importar bibliotecas necessárias
import requests
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
# matplotlib não é estritamente necessário se estiver usando Plotly/Streamlit nativo, mas foi mantido.
import matplotlib.pyplot as plt

# Apresentação
st.title("Câmara Aberta")
st.header("Uma plataforma dedicada ao acesso a informações da Câmara dos Deputados")
st.subheader("Aqui você pode buscar informações sobre Projetos de Lei, Propostas de Emenda Constitucional, ou deputados.")

# Menu 1 - Opção de Busca
st.header("O que você está procurando?")
opcoes = ["a) Projetos de Lei", "b) Propostas de Emenda Constitucional", "c) Deputados", "d) Sair"]
# O Streamlit guarda o estado da seleção.
busca = st.radio("Selecione a opção da sua busca:", opcoes)

# Lógica principal baseada na seleção
if busca == "d) Sair":
    st.subheader("Você escolheu a opção de sair da pesquisa.")
    st.subheader("Obrigado por usar o programa. Até a próxima!")

# Resultado do Menu a) PL
elif busca == "a) Projetos de Lei":
    st.subheader("Você escolheu a opção de buscar projetos de lei.")
    numero_pl = st.text_input("Digite o número do projeto de lei:")
    ano_pl = st.text_input("Digite o ano do projeto de lei:")

    if numero_pl.strip() and ano_pl.strip():
        # Lógica de busca e exibição de Projetos de Lei (mantida como original)
        url_busca_pl = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo=PL&numero={numero_pl}&ano={ano_pl}"
        response_pl = requests.get(url_busca_pl)
        
        if response_pl.status_code == 200:
            dados_pl = response_pl.json()
            if dados_pl and dados_pl.get('dados'):
                # Processa apenas o primeiro resultado encontrado
                proposicao = dados_pl['dados'][0]
                id_proposicao = proposicao['id']
                st.subheader(f"Projeto encontrado!")
                
                url_detalhes = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id_proposicao}"
                response_detalhes = requests.get(url_detalhes)
                
                if response_detalhes.status_code == 200:
                    detalhes = response_detalhes.json().get('dados', {})
                    if detalhes:
                        st.subheader("Detalhes do Projeto")
                        st.write(f"Situação atual: {detalhes.get('statusProposicao', {}).get('descricaoSituacao', 'N/A')}")
                        st.write(f"Ementa completa: {detalhes.get('ementa', 'Ementa não disponível.')}")
                        
                        autores = detalhes.get('autores', [])
                        if autores:
                            primeiro_autor = autores[0]
                            nome_autor = primeiro_autor.get('nome', 'N/A')
                            tipo_autor = primeiro_autor.get('tipo', 'N/A')
                            uri_autor = primeiro_autor.get('uri')
                            
                            st.markdown(f"**Autor Principal:** {nome_autor} ({tipo_autor})")
                            if uri_autor and 'deputados' in uri_autor:
                                st.markdown(f"[[Detalhes do Autor]({uri_autor})]")
                        else:
                            st.write("**Autor Principal:** Informação não disponível")
                            
                        url_detalhe = detalhes.get('urlDetalhe')
                        if url_detalhe:
                            st.markdown(f"**Link para Detalhamento Completo:** [Acesse a página oficial da proposição]({url_detalhe})")
                    else:
                        st.error("Detalhes do projeto não puderam ser carregados.")
                else:
                    st.error(f"Erro ao buscar detalhes. Status: {response_detalhes.status_code}")
            else:
                st.warning(f"Projeto com o número {numero_pl} do ano {ano_pl} não encontrado.")
        else:
            st.warning(f"Erro na requisição à API. Status {response_pl.status_code}")
    else:
        st.warning("Por favor, digite o **número** e o **ano** do Projeto de Lei para realizar a busca.")
    st.write("Obrigado por usar o programa. Até a próxima!")

# Resultado Menu b) PEC
elif busca == "b) Propostas de Emenda Constitucional":
    st.subheader("Você escolheu a opção de buscar propostas de emenda constitucional.")
    numero_pec = st.text_input("Digite o número da proposta de emenda constitucional:")
    ano_pec = st.text_input("Digite o ano da proposta de emenda constitucional:")
    
    if numero_pec.strip() and ano_pec.strip():
        # Lógica de busca e exibição de PECs (mantida como original)
        url_busca_pec = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo=PEC&numero={numero_pec}&ano={ano_pec}"
        response_pec = requests.get(url_busca_pec)
        
        if response_pec.status_code == 200:
            dados_pec = response_pec.json()
            if dados_pec and dados_pec.get('dados'):
                proposicao = dados_pec['dados'][0]
                id_proposicao = proposicao['id']
                st.subheader(f"PEC encontrada!")
                
                url_detalhes = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id_proposicao}"
                response_detalhes = requests.get(url_detalhes)
                
                if response_detalhes.status_code == 200:
                    detalhes = response_detalhes.json().get('dados', {})
                    if detalhes:
                        st.subheader("Detalhes da PEC")
                        st.write(f"Situação atual: {detalhes.get('statusProposicao', {}).get('descricaoSituacao', 'N/A')}")
                        st.write(f"Ementa completa: {detalhes.get('ementa', 'Ementa não disponível.')}")
                        
                        autores = detalhes.get('autores', [])
                        if autores:
                            primeiro_autor = autores[0]
                            nome_autor = primeiro_autor.get('nome', 'N/A')
                            tipo_autor = primeiro_autor.get('tipo', 'N/A')
                            uri_autor = primeiro_autor.get('uri')
                            
                            st.markdown(f"**Autor Principal:** {nome_autor} ({tipo_autor})")
                            if uri_autor and 'deputados' in uri_autor:
                                st.markdown(f"[[Detalhes do Autor]({uri_autor})]")
                        else:
                            st.write("**Autor Principal:** Informação não disponível")
                            
                        url_detalhe = detalhes.get('urlDetalhe')
                        if url_detalhe:
                            st.markdown(f"**Link para Detalhamento Completo:** [Acesse a página oficial da proposição]({url_detalhe})")
                    else:
                        st.error("Detalhes da PEC não puderam ser carregados.")
                else:
                    st.error(f"Erro ao buscar detalhes. Status: {response_detalhes.status_code}")
            else:
                st.warning(f"PEC {numero_pec}/{ano_pec} não encontrada.")
        else:
            st.warning(f"Erro na requisição à API. Status: {response_pec.status_code}")
    else:
        st.warning("Por favor, digite o **número** e o **ano** da PEC para realizar a busca.")
    st.write("Obrigado por usar o programa. Até a próxima!")

# Resultado do Menu c) Deputados
elif busca == "c) Deputados":
    st.subheader("Você escolheu a opção de buscar informações de deputados.")
    nome_deputado = st.text_input("Digite o nome do deputado(a):")
    
    if nome_deputado:
        url_deputados = f"https://dadosabertos.camara.leg.br/api/v2/deputados?nome={nome_deputado}&ordem=ASC&ordenarPor=nome"
        response = requests.get(url_deputados)
        
        # Informações Gerais do Deputado(a)
        if response.status_code == 200:
            dados_deputado = response.json().get('dados', [])
            
            if dados_deputado:
                # Usa o primeiro resultado da busca (o mais provável)
                deputado_selecionado = dados_deputado[0]
                deputado_id = deputado_selecionado['id']
                deputado_nome = deputado_selecionado['nome']
                deputado_partido = deputado_selecionado['siglaPartido']
                deputado_uf = deputado_selecionado['siglaUf']

                st.subheader(f"Deputado(a) encontrado(a): {deputado_nome}")
                st.write(f"Nome: {deputado_nome}")
                st.write(f"Partido: {deputado_partido}")
                st.write(f"UF: {deputado_uf}")
                
                # Detalhes do Deputado (Busca adicional para foto e e-mail)
                url_detalhes_dep = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputado_id}"
                response_detalhes_dep = requests.get(url_detalhes_dep)

                if response_detalhes_dep.status_code == 200:
                    detalhes_dep = response_detalhes_dep.json().get('dados', {})
                    if detalhes_dep:
                        st.image(detalhes_dep['urlFoto'], width=150)
                        st.write(f"E-mail: {detalhes_dep['email']}")
                else:
                    st.warning("Não foi possível carregar detalhes adicionais.")

                # Frentes do Deputado(a)
                url_frentes = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputado_id}/frentes"
                response_frentes = requests.get(url_frentes)
                if response_frentes.status_code == 200 and response_frentes.json().get('dados'):
                    df_frentes = pd.DataFrame(response_frentes.json()['dados'])
                    st.subheader("Frentes parlamentares que o(a) deputado(a) integra")
                    st.dataframe(df_frentes[['titulo']],
                                 column_config={'titulo': 'Frente Parlamentar'},
                                 use_container_width=True)
                else:
                    st.info("Nenhuma frente parlamentar encontrada ou erro na requisição.")

                # Órgãos do Deputado(a)
                url_orgaos = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputado_id}/orgaos"
                response_orgaos = requests.get(url_orgaos)
                if response_orgaos.status_code == 200 and response_orgaos.json().get('dados'):
                    dados_orgaos = response_orgaos.json()['dados']
                    df_orgaos = pd.DataFrame(dados_orgaos)
                    st.subheader("Órgãos que o(a) deputado(a) integra")
                    st.dataframe(df_orgaos[['siglaOrgao', 'nomePublicacao', 'titulo']],
                                 column_config={'siglaOrgao': 'Sigla do Órgão',
                                                'nomePublicacao': 'Nome do Órgão',
                                                'titulo': 'Status do Deputado'},
                                 use_container_width=True)
                else:
                    st.info("Nenhum órgão encontrado ou erro na requisição.")

                # Despesas do Deputado(a) - Adicionado tratamento de erro/vazio mais robusto
                url_despesas = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputado_id}/despesas?ordem=DESC&ordenarPor=dataDocumento&itens=10"
                response_despesas = requests.get(url_despesas)
                
                if response_despesas.status_code == 200 and response_despesas.json().get('dados'):
                    dados_despesas = response_despesas.json()['dados']
                    df_despesas = pd.DataFrame(dados_despesas)
                    
                    if not df_despesas.empty:
                        # Converte 'valorDocumento' para numérico para o gráfico
                        df_despesas['valorDocumento'] = pd.to_numeric(df_despesas['valorDocumento'], errors='coerce').fillna(0)
                        
                        st.subheader("Primeiras despesas do Deputado(a) (últimos 10 lançamentos)")
                        
                        # Agrupa as despesas por tipo para o gráfico de barras
                        df_grouped_despesas = df_despesas.groupby('tipoDespesa')['valorDocumento'].sum().reset_index()
                        
                        fig_despesas = px.bar(df_grouped_despesas,
                                             x='tipoDespesa',
                                             y='valorDocumento',
                                             title=f'Total de Despesas por Tipo de {deputado_nome}',
                                             labels={'tipoDespesa': ' Tipo de Despesa ',
                                                     'valorDocumento': ' Valor Total (em R$) '},
                                             template="plotly_white")
                        fig_despesas.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_despesas, use_container_width=True)

                        # Exibe a tabela de dados brutos
                        st.subheader("Detalhe das Despesas")
                        st.dataframe(df_despesas[['dataDocumento', 'tipoDespesa', 'valorDocumento', 'nomeFornecedor']],
                                     column_config={'dataDocumento': 'Data',
                                                    'tipoDespesa': 'Tipo',
                                                    'valorDocumento': st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f"),
                                                    'nomeFornecedor': 'Fornecedor'},
                                     use_container_width=True)
                    else:
                        st.warning(f"Nenhuma despesa encontrada para {deputado_nome} no período.")
                else:
                    st.info(f"Não foi possível buscar as despesas ou a API retornou um erro (Status: {response_despesas.status_code}).")
                    
            else:
                st.warning(f"Nenhum deputado(a) encontrado com o nome '{nome_deputado}'.")
        else:
            st.warning(f"Erro na requisição à API. Status: {response.status_code}")
    else:
        st.warning("Por favor, digite o **nome** do deputado para realizar a busca.")
    st.write("Obrigado por usar o programa. Até a próxima!")
