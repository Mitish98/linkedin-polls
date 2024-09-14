import pandas as pd
import streamlit as st
import os

class PollDashboard:
    def __init__(self, poll_data=None, csv_file=None):
        if poll_data:
            self.poll_data = poll_data
            self.poll_df = self.polls_to_dataframe()
        elif csv_file:
            self.poll_df = pd.read_csv(csv_file)
        else:
            raise ValueError("Deve ser fornecido poll_data ou csv_file.")

    def polls_to_dataframe(self):
        dataframes = []
        for poll in self.poll_data:
            options_df = pd.DataFrame(poll['Options'])
            options_df['Title'] = poll['Title']
            options_df['Link'] = poll['Link']
            options_df['Total Votes'] = poll['Total Votes']
            dataframes.append(options_df)
        return pd.concat(dataframes, ignore_index=True)

    def create_dashboard(self):
        csv_file = os.getenv("CSV_FILE_PATH")
        if not csv_file:
            st.error("Arquivo CSV não encontrado.")
            return

        self.poll_df = pd.read_csv(csv_file)
        for title, group in self.poll_df.groupby('Title'):
            st.header(title)
            st.markdown(f"[Ver postagem no LinkedIn]({group['Link'].iloc[0]})")
            st.write(f"Total de votos: {group['Total Votes'].iloc[0]}")
            st.dataframe(group[['Option', 'Percentage']])
            group['Percentage'] = group['Percentage'].str.replace('%', '').astype(float)
            st.bar_chart(data=group, x='Option', y='Percentage')

def main():
    dashboard = PollDashboard()
    dashboard.create_dashboard()

if __name__ == "__main__":
    main()
