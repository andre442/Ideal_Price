#!/usr/bin/env python
# coding: utf-8

import pandas as pd

#lendo base de dados unificada
f = pd.read_excel('dados.xlsx', sheet_name='Meals Ordered')
m = pd.read_csv('meal_encoded.csv', index_col=0)
full = pd.merge(f, m, how='left', on='mealId')


#verificando se as variáveis numéricas "price", "discountTotal" e "totalvalue" estão em float
type(full['price'][0])
type(full['discountTotal'][0])
type(full['totalValue'][0])

#verificando valores na base
full.describe()

# # Data Cleaning

#encontrando o registro com preço = 0
full[full['price']==0]

#removendo o registro com preço = 0
full = full.drop(index=3469)

#verificando distribuição de preços
full.describe()

#temos agora 7610 registros na base (sem o registro com price=0 )
full

# # Criando a feature "sales" e fazendo o preço base por prato

#criando lista com os 133 pratos existentes
pratos = full['ref'].unique()

#criando data frame com os 133 pratos
df = full.drop_duplicates(subset=['ref'])
#reiniciando index
df = df.reset_index()
del df['index']

#criando coluna "sales"
df['sales']= 0

#adicionando o total de vendas por prato
k=0
for k in range(0,133):
    df.loc[k, 'sales'] = len(full.loc[full['ref'] == pratos[k]])
    
#adicionando preço base por prato
k=0
for k in range(0,133):
    df.loc[k, 'price']  = full.loc[full['ref']==pratos[k]]['price'].min()

#criando coluna "total_ing" com o número total de ingredientes por prato
df['total_ing']= 0

k=0
for k in range(0,133):
    df.loc[k, 'total_ing']  = df.loc[k,'I58':'I700'].sum()


# # Normalização das features numéricas / categóricas

#convertendo o tipo da variável "subcategory" de string->numérica utilizando o LabelEncoder
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df['subcategory'] = le.fit_transform(df['subcategory'])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['subcategory'] = scaler.fit_transform(df[['subcategory']])

#Realizando a normalização da coluna "total_ing"

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['total_ing'] = scaler.fit_transform(df[['total_ing']])

#Realizando a normalização da coluna "sales"

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['sales'] = scaler.fit_transform(df[['sales']])


# # Salvando os dados

#é necessário separar e apagar todos os registros do prato 1028
#pois ele será usado após a fase de teste do regressor
df.loc[df['ref']== 1028]  #retornando somente linhas com o prato 1028

#salvando somente os registros com o prato 1028 em um dataframe chamado "base_1028"
base_analise_1028 = df.loc[df['ref']== 1028]

base_analise_1028.to_csv('base_analise_1028.csv', index = False)

#agora visualizando a base com os registros restantes:
df.loc[df['ref']!= 1028]


#salvando os registros restantes (sem o prato 1028) em um dataframe chamado "base_r" 
base_analise_treino = df.loc[df['ref']!= 1028]

base_analise_treino.to_csv('base_analise_treino.csv', index = False)





