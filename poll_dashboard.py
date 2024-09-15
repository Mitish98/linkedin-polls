import pandas as pd
import streamlit as st
import os

class PollDashboard:
    def __init__(self, poll_df):
        self.poll_df = poll_df

    # Função para criar o dashboard usando Streamlit
    def create_dashboard(self):
        # Exibir gráficos das enquetes
        for title, group in self.poll_df.groupby('Title'):
            st.header(title)
            
            # Exibir o link da postagem
            st.markdown(f"[Ver postagem no LinkedIn]({group['Link'].iloc[0]})")
            
            # Exibir o total de votos
            st.write(f"Total de votos: {group['Total Votes'].iloc[0]}")
            
            # Exibir as opções e porcentagens como tabela
            st.dataframe(group[['Option', 'Percentage']])  

            # Gráfico de barra para as opções
            group['Percentage'] = group['Percentage'].str.replace('%', '').astype(float)
            st.bar_chart(data=group, x='Option', y='Percentage')

def main():
    st.title("LinkedIn Polls Data - Dashboard")

    # Caminho para o arquivo CSV padrão
    default_csv_path = 'poll_data.csv'

    # Verifica se o arquivo CSV padrão existe
    if os.path.exists(default_csv_path):
        default_df = pd.read_csv(default_csv_path)
        
        
    else:
        st.error("O arquivo CSV padrão não foi encontrado. Por favor, faça o upload de um arquivo CSV.")

    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("View my poll data on LinkedIn or upload your own CSV file to view charts with data from your poll posts:", type="csv")

    if uploaded_file is not None:
        # Ler o CSV carregado
        poll_df = pd.read_csv(uploaded_file)
    elif os.path.exists(default_csv_path):
        # Usar o arquivo CSV padrão se nenhum arquivo for carregado
        poll_df = default_df
    else:
        st.error("Nenhum arquivo CSV foi carregado. Por favor, faça o upload de um arquivo CSV.")
        return

    # Criar e mostrar o dashboard
    dashboard = PollDashboard(poll_df=poll_df)
    dashboard.create_dashboard()

if __name__ == "__main__":
    main()
