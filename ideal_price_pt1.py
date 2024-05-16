#!/usr/bin/env python
# coding: utf-8

#importando frameworks
import pandas as pd

#importando base de dados
meal = pd.read_excel('dados.xlsx', sheet_name='Meal')

#verificando base
meal.head(4)

#verificando número de pratos únicos
len(meal['mealId'].unique())

#removendo a coluna "category"
meal.drop(columns=['category'], inplace=True)

#
meal.head(4)

#criando lista de iteração
ingredientes = []

#loop para retornar lista com todos os ingredientes e valores do df
for z in range(0,134):
    for i in range(1,25):
        ingredientes.append(meal.iloc[z,i])
        

#transformando a lista em pd.series
Ingredientes = pd.Series(ingredientes) 

#verificando array com ingredientes
Ingredientes.unique()

#removendo valores nulos (nan)
Ingredientes.dropna(inplace=True)
#removendo valores duplicados             
Ingredientes.drop_duplicates(inplace=True)    

#removendo valores "errados"
Ingredientes.drop(Ingredientes.index[Ingredientes == 'vinho-do-porto'], inplace = True)
Ingredientes.drop(Ingredientes.index[Ingredientes == ']'], inplace = True)

#reiniciando index
Ingredientes = Ingredientes.reset_index()
del Ingredientes['index']

#temos então, 334 diferentes ingredientes! 
Ingredientes

#criando colunas com os 334 ingredientes

for a in range(0,334):
    meal[Ingredientes.iloc[a,]] = 0

#preenchendo colunas dos ingredientes para cada prato

for h in range(0,133):
    for g in range(25,359):
        for f in range(1,24):
            y = meal.iloc[h,f]
            if y == meal.columns[g]:
                meal.iloc[h,g]=1


#apagando colunas com códigos dos ingredientes
meal.drop(columns = meal.columns[1:25] , inplace=True) 

#verificando base
meal.head()

#salvando dataframe
meal.to_csv('meal_encoded.csv')

