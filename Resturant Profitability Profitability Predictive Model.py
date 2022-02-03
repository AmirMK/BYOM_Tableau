import numpy as np
import pandas as pd


from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsRegressor

from sklearn.model_selection import GridSearchCV

from tabpy.tabpy_tools.client import Client


#Model selection function
def regressor_selection(X,y, metric = 'r2'):    
    pipe = Pipeline([('regressor' , RandomForestRegressor())])    
    param_grid = ''
    param = [        
                
        {'regressor' : [RandomForestRegressor()],
        'regressor__n_estimators' : [100,200,500],
        'regressor__max_depth' : list( range(5,25,5) ),
        'regressor__min_samples_split' : list( range(4,12,2) )
        },
        
        {'regressor' : [KNeighborsRegressor()],
         'regressor__n_neighbors' : [5,10,20,30],
         'regressor__p' : [1,2] 
        },
        {
         'regressor' : [Lasso(max_iter=500)],
         'regressor__alpha' : [0.001,0.01,0.1,1,10,100,1000]         
        }
            ]
    param_grid = param    
    clf = GridSearchCV(pipe, param_grid = param_grid, 
                       cv = 5, n_jobs=-1,scoring = metric)    
    best_clf = clf.fit(X, y)
    
    return(best_clf.best_params_['regressor'])



#Reading Data
url=  'Restaurant_Profitability_Training_Data.csv'
df = pd.read_csv(url)

Target = 'Profit'
categorical_features = ['Area', 'Age', 'Type','Price Range','Capacity','Number of Menu Items']
numerical_feature = []
target = 'Profit'

label=df[target]
data= df[categorical_features+numerical_feature]



#Data Preprocessing
numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median'))
                                      ,('scaler', StandardScaler())])
categorical_transformer = OneHotEncoder(categories='auto')

encoder = ColumnTransformer(
    transformers=[
        ('numerical', numeric_transformer, numerical_feature),
        ('categorical', categorical_transformer, categorical_features)])

encoder.fit(data)

#Model Building and Selection
clf = regressor_selection(encoder.transform(data),label, metric = 'r2')
model = clf.fit(encoder.transform(data),label)                


#Wrapper function for prediction
def Profitability_Prediction(Areas, Ages, Types, Price_Ranges, Capacities, Items):    
    input_data = np.column_stack([Areas, Ages, Types, Price_Ranges, Capacities, Items])
    X = pd.DataFrame(input_data,columns=['Area', 'Age', 'Type','Price Range','Capacity','Number of Menu Items'])
    result = model.predict(encoder.transform(X))
    return result.tolist()



#Model deployment
client = Client('http://localhost:9004/')
client.deploy('Restaurant_Profitability',
              Profitability_Prediction,
              'Returns prediction of profitability for restaurant(s).'
              , override = True)



