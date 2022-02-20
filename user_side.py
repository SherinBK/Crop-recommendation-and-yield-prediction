import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests 
import json

# Load the pickled Crop classifier model
crop_clf = joblib.load('crop_classifier.pkl')

def predict_crop(Nitrogen,Phosphorous,Pottassium,Temp,humd,ph,rain):
      df = pd.DataFrame([[Nitrogen,Phosphorous,Pottassium,Temp,humd,ph,rain]],columns = ['N','P','K','temperature','humidity','ph','rainfall'])
      prediction = crop_clf.predict(df)
      #print(prediction)
      return prediction[0]
      
def get_details_put_crop():
       Temp,humd = get_loc_weather_details()
       Nitrogen = st.slider("Nitrogen (mineral ratio in the soil)",30,60,45)
       Pottassium = st.slider("Pottassium(mineral ratio in the soil)",30,90,60)
       Phosphorous = st.slider("Phosphorous(mineral ratio in the soil)",30,50,40)
       pH = st.number_input("pH(1-14) ",4.5,7.5,6.0)
       rain = st.number_input("Rainfall( in cm)",50.0,250.0,100.0)
       
       result =""
       
       if st.button("Predict"):
             result = predict_crop(Nitrogen,Phosphorous,Pottassium,Temp,humd,pH,rain)
             result = result.upper()
             st.success('The suitable crop is {}'.format(result))    
  
def get_loc_weather_details():
      dist = np.array(['ARIYALUR', 'COIMBATORE', 'CUDDALORE', 'DHARMAPURI', 'DINDIGUL','ERODE', 'KANCHIPURAM', 'KANNIYAKUMARI', 'KARUR', 'KRISHNAGIRI','MADURAI', 'NAGAPATTINAM', 'NAMAKKAL', 'PERAMBALUR', 'PUDUKKOTTAI','RAMANATHAPURAM', 'SALEM', 'SIVAGANGA', 'THANJAVUR','THE NILGIRIS','THENI', 'THIRUVALLUR', 'THIRUVARUR','TIRUCHIRAPPALLI', 'TIRUNELVELI', 'TIRUPPUR', 'TIRUVANNAMALAI','TUTICORIN', 'VELLORE', 'VILLUPURAM', 'VIRUDHUNAGAR'])
      
      district = st.selectbox('Enter your District ',dist)
      
      BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
      API_KEY = //"your api key"
      URL = BASE_URL + "q=" + district + "&appid=" + API_KEY
  
      # Request for weather information
      response = requests.get(URL)
      
      if response.status_code == 200:
            report = response.json()
            main = report['main']
            main_df = pd.DataFrame.from_dict(pd.json_normalize(main), orient='columns')  
      else:
            print("cannot access weather api")
            return
          
      temper = main_df['temp'].values
      humd = main_df['humidity'].values
      
      return temper[0],humd[0] 
      

def main():
      
      # giving the webpage a title
      st.title("CROP CLASSIFICATION")
      get_details_put_crop()
   
    
if __name__=='__main__':
      main()
      
