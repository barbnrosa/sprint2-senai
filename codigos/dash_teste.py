import streamlit as st
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

# Load your dataset or use the existing one
# For example, you can load it from a CSV file
df_pj = pd.read_csv('../dados/PJ_tratados.csv')

selected_setor_ibge = st.selectbox('Select Setor IBGE', df_pj['Setor IBGE'].unique())
selected_porte = st.selectbox('Select Porte', df_pj['Porte'].unique())

filtered_df = df_pj[(df_pj['Setor IBGE'] == selected_setor_ibge) & (df_pj['Porte'] == selected_porte)]

transacoes_agrupadas = filtered_df.groupby(['ID Cliente', 'Setor IBGE', 'Porte'])['Produto GPOM'].apply(list).reset_index()
transacao = transacoes_agrupadas['Produto GPOM'].tolist()
te = TransactionEncoder()
transacao_te = te.fit(transacao).transform(transacao)
transacao_transformado = pd.DataFrame(transacao_te, columns=te.columns_)
items_frequentes_apriori = apriori(transacao_transformado, min_support=0.02, use_colnames=True)
regras_apriori = association_rules(items_frequentes_apriori, metric='confidence', min_threshold=0.5)

# Streamlit app
st.title('Apriori Association Rules Dashboard')

# Display the original data
st.subheader('Filtred DataSet')
st.dataframe(filtered_df)

# Display the association rules
st.subheader('Association Rules')
regras_apriori['antecedents'] = regras_apriori['antecedents'].apply(lambda x: list(x))
regras_apriori['consequents'] = regras_apriori['consequents'].apply(lambda x: list(x))

# Display the modified dataframe
st.dataframe(regras_apriori.sort_values("support", ascending = False))
