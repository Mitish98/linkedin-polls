import pandas as pd
import streamlit as st

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
    st.title("Dashboard de Enquetes")

    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if uploaded_file is not None:
        # Ler o CSV carregado
        poll_df = pd.read_csv(uploaded_file)
        # Criar e mostrar o dashboard
        dashboard = PollDashboard(poll_df=poll_df)
        dashboard.create_dashboard()

if __name__ == "__main__":
    main()

