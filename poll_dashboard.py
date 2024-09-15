import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt

class PollDashboard:
    def __init__(self, poll_df):
        self.poll_df = poll_df

    # Função para criar o dashboard usando Streamlit
    def create_dashboard(self):
        for title, group in self.poll_df.groupby('Title'):
            st.header(title)
            
            # Exibir o link da postagem
            st.markdown(f"[Ver postagem no LinkedIn]({group['Link'].dropna().iloc[0]})")
            
            # Exibir o total de votos
            st.write(f"Total de votos: {group['Total Votes'].dropna().iloc[0]}")
            
            # Exibir as opções e porcentagens como tabela
            st.dataframe(group[['Option', 'Percentage']])  

            # Processar a porcentagem
            group['Percentage'] = group['Percentage'].str.replace('%', '').astype(float)

            # Gráfico de barra para as opções
            st.bar_chart(data=group, x='Option', y='Percentage')

            # Gráfico de Pizza
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(group['Percentage'], labels=group['Option'], autopct='%1.1f%%', startangle=90)
            ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig_pie)

            # Gráfico de Linha (exemplo simples, mais útil se os dados forem sequenciais)
           

def main():
    st.title("LinkedIn Polls Data - Dashboard")

    # Caminho para o arquivo CSV padrão
    default_csv_path = 'poll_data.csv'

    # Verifica se o arquivo CSV padrão existe
    if os.path.exists(default_csv_path):
        default_df = pd.read_csv(default_csv_path)
    else:
        st.error("O arquivo CSV padrão não foi encontrado. Por favor, faça o upload de um arquivo CSV.")
        return

    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("View my poll data on LinkedIn or upload your own CSV file in to the format 'Option,Percentage,Title,Link,Total Votes' to view charts with data from your poll posts:", type="csv")

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
