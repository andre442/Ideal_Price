#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import math
import numpy as np
from sklearn.metrics import mean_absolute_error
import sklearn.metrics as metrics
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score

#carregando base de treino
base_r = pd.read_csv('base_analise_treino.csv')

#carregando registro do prato 1028
Q = pd.read_csv('base_analise_1028.csv')

#Apgando as colunas "mealid", discountTotal, totalValue e ref da base de treino
base_r = base_r.loc[:,'price':]
base_r.drop(columns = base_r.columns[1], inplace = True)
base_r.drop(columns = base_r.columns[1], inplace = True)
base_r.drop(columns = base_r.columns[1], inplace = True)
base_r.drop(columns = base_r.columns[2], inplace = True)

#formatando o registro com o prato 1028 no mesmo formato dos dados de treino 
Q = Q.loc[:,'price':]
Q.drop(columns = Q.columns[1], inplace = True)
Q.drop(columns = Q.columns[1], inplace = True)
Q.drop(columns = Q.columns[1], inplace = True)
Q.drop(columns = Q.columns[2], inplace = True)


# # Separando atributos previsores e target (price)

#atribuindo as colunas "subcategory", 'sales', 'total_ing' e as colunas dos ingredientes como features
X = base_r.iloc[:, 1:].values

#atribuindo o preço como variável dependente da regressão
y = base_r.iloc[:, 0].values    

# aqui a amostra do prato 1028 é formatada como as amostras de treino (sem a coluna price)
Z = Q.iloc[0, 1:].values

# # Treinamento do algoritmo RandomForest
#separando dados de treino e teste
from sklearn.model_selection import train_test_split
X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(X, y,
                                                                  test_size = 0.15,
                                                                  random_state = 0, shuffle=True)

#importando regressores
from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(n_estimators = 200, max_depth=15,  random_state = 0)

regressor.fit(X_treinamento, y_treinamento)


#realizando previsões e calculando métricas
previsoes = regressor.predict(X_teste)
score_treinamento = regressor.score(X_treinamento, y_treinamento)

mae = mean_absolute_error(y_teste, previsoes)
print("MAE:", mae)
mse = metrics.mean_squared_error(y_teste, previsoes)
rmse = np.sqrt(mse)
print("RMSE:", rmse)
print('score_tr:',score_treinamento)
score_teste = regressor.score(X_teste, y_teste)
print('score_te:',score_teste)
print('qte de amostras:',len(X_teste))


# # Regressão para o preço do prato 1028 com RandomForest

rf_price = regressor.predict([Z])
rf_price[0]

######################

# # Treinamento do algoritmo XGBoost
Z=Z.reshape(1,-1)


#separando dados de treino e teste
from sklearn.model_selection import train_test_split
X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(X, y,
                                                                  test_size = 0.2,
                                                                  random_state = 0, shuffle=True)

#importando regressores
import xgboost

regressor=xgboost.XGBRegressor(n_estimators=60, max_depth=7, learning_rate=0.1)

regressor.fit(X_treinamento, y_treinamento)

#realizando previsões e calculando métricas
previsoes = regressor.predict(X_teste)

mae = mean_absolute_error(y_teste, previsoes)
print("MAE:", mae)
mse = metrics.mean_squared_error(y_teste, previsoes)
rmse = np.sqrt(mse)
print("RMSE:", rmse)
score_treinamento = regressor.score(X_treinamento, y_treinamento)
print('score_tr:',score_treinamento)
score_teste = regressor.score(X_teste, y_teste)
print('score_te:',score_teste)
print('qte de amostras:',len(X_teste))


# # Regressão para o preço do prato 1028 com XGBoost
xgb_price = regressor.predict(Z)
xgb_price[0]





