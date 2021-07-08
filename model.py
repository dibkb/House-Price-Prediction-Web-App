import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
import pickle
#initaize the scaler
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

df = pd.read_csv('data/USA_Housing.csv')

X = df.drop(['Price','Address'],axis = 1)
y = df['Price']

X = scaler_x.fit_transform(X)
y = scaler_y.fit_transform(pd.DataFrame(y))

lin_model = pickle.load(open('pickle/house_pred.pkl', 'rb'))