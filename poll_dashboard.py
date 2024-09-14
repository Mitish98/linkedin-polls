import pandas as pd
import streamlit as st

class PollDashboard:
    def __init__(self, poll_data):
        self.poll_data = poll_data
        self.poll_df = self.polls_to_dataframe()

    # Função para transformar os dados em um DataFrame
    def polls_to_dataframe(self):
        dataframes = []

        for poll in self.poll_data:
            options_df = pd.DataFrame(poll['Options'])
            options_df['Title'] = poll['Title']
            options_df['Link'] = poll['Link']  # Adiciona o link ao DataFrame
            options_df['Total Votes'] = poll['Total Votes']  # Adiciona o total de votos ao DataFrame
            dataframes.append(options_df)

        return pd.concat(dataframes, ignore_index=True)

    # Função para criar o dashboard usando Streamlit
    def create_dashboard(self):

        # Exibir gráficos das enquetes
        for title, group in self.poll_df.groupby('Title'):
            st.header(title)
            
            # Exibir o link da postagem
            st.markdown(f"[Ver postagem no LinkedIn]({group['Link'].iloc[0]})")
            
            # Exibir o total de votos
            st.write(f"Total de votos: {group['Total Votes'].iloc[0]}")
            
            # Gráfico de pizza para cada enquete
            st.dataframe(group[['Option', 'Percentage']])  # Exibe as opções e porcentagens como tabela

            # Gráfico de barra para as opções
            group['Percentage'] = group['Percentage'].str.replace('%', '').astype(float)
            st.bar_chart(data=group, x='Option', y='Percentage')

    # Função para exportar o DataFrame
    def export_dataframe(self, file_name="poll_data.csv"):
        self.poll_df.to_csv(file_name, index=False)
        st.success(f"Dados exportados para {file_name}")
