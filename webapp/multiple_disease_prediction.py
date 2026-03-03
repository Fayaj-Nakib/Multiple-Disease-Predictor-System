import streamlit as st
import pandas as pd
import pickle
from streamlit_option_menu import option_menu

import json
from PIL import Image
import requests  # pip install requests
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie  # pip install streamlit-lottie

# GitHub: https://github.com/andfanilo/streamlit-lottie
# Lottie Files: https://lottiefiles.com/

# loading the saved models

diabetes_model = pickle.load(open('F:/python code/temporary/model/diabetes_trained_model.sav', 'rb'))

heart_disease_model = pickle.load(open('F:/python code/temporary/model/heart_disease_model.sav','rb'))

parkinsons_model = pickle.load(open('F:/python code/temporary/model/parkinsons_model.sav', 'rb'))

lung_cancer_model = pickle.load(open('F:/python code/temporary/model/lungCancer_trained_model.sav', 'rb'))






# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()
    

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def view_user_data(username):
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    data = c.fetchall()
    return data

def main():
    """Simple Login App"""

    st.title("Multiple Disease Prediction System")
    with st.sidebar:

        choice = option_menu('Multiple Disease Prediction System',
                              
                              ['Home',
                                'Login',
                               'SignUp',
                               ],
                              icons=['house','check-circle','plus-circle'],
                              default_index=0,)
        
    #menu = ["Home","Login","SignUp"]
    #choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        def load_lottiefile(filepath: str):
            with open(filepath, "r") as f:
                return json.load(f)
        
        
        def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
            
        
        #lottie_coding = load_lottiefile("lottiefile.json")  # replace link to local lottie file
        lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
        
        
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=400,
            width=700,
            key=None,
        )

        st.markdown('We can build a multiple diseases prediction app using machine learning. The app would take input from the user, such as age, gender, symptoms, medical history, and test results, and use machine learning algorithms to predict the probability of multiple diseases.')
        
        lottie_health = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_gmspxrnd.json")
       
        st_lottie(
            lottie_health,
            
            speed=1,
        
            reverse=False,
            loop=True,
            quality="low",
            height=400,
            width=700,
            key=None,
        )
        
        
        st.markdown('Thank you for choosing us.Praying to God for your good health.Please help us by giving an honest feedback so that we can improve more.')
        
        

    elif choice == "Login":
        st.subheader("Login Section")
        def load_lottiefile(filepath: str):
            with open(filepath, "r") as f:
                return json.load(f)
        
        
        def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
            
        
        #lottie_coding = load_lottiefile("lottiefile.json")  # replace link to local lottie file
        lottie_hello = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_ktwnwv5m.json")
        
        
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=400,
            width=700,
            key=None,
        )
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                selected = option_menu('',
                                      
                                      [
                                        'Diabetes Prediction',
                                       'Heart Disease Prediction',
                                       'Parkinsons Prediction',
                                       'Lung Cancer Prediction','Profiles'],
                                      icons=['activity','heart','person','person-fill','person-fill'],
                                      default_index=0,orientation="horizontal")
                # Diabetes Prediction Page
                if (selected == 'Diabetes Prediction'):
                    
                    # page title
                    
                    img = Image.open("F:/python code/temporary/image/1.webp")
                    st.image(img)
                    st.title('Diabetes Prediction using ML')
                    # getting the input data from the user
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        Pregnancies = st.text_input('Number of Pregnancies')
                        
                    with col2:
                        Glucose = st.text_input('Glucose Level')
                    
                    with col3:
                        BloodPressure = st.text_input('Blood Pressure value')
                    
                    with col1:
                        SkinThickness = st.text_input('Skin Thickness value')
                    
                    with col2:
                        Insulin = st.text_input('Insulin Level')
                    
                    with col3:
                        BMI = st.text_input('BMI value')
                    
                    with col1:
                        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
                    
                    with col2:
                        Age = st.text_input('Age of the Person')
                    
                    
                    # code for Prediction
                    diab_diagnosis = ''
                    
                    # creating a button for Prediction
                    
                    if st.button('Diabetes Test Result'):
                        diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
                        
                        if (diab_prediction[0] == 1):
                          diab_diagnosis = 'The person is diabetic'
                        else:
                          diab_diagnosis = 'The person is not diabetic'
                        
                    st.success(diab_diagnosis)




                # Heart Disease Prediction Page
                if (selected == 'Heart Disease Prediction'):
                    img = Image.open("F:/python code/temporary/image/2.jpg")
                    st.image(img)
                    # page title
                    st.title('Heart Disease Prediction using ML')
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        age = st.text_input('Age')
                        
                    with col2:
                        sex = st.text_input('Sex')
                        
                    with col3:
                        cp = st.text_input('Chest Pain types')
                        
                    with col1:
                        trestbps = st.text_input('Resting Blood Pressure')
                        
                    with col2:
                        chol = st.text_input('Serum Cholestoral in mg/dl')
                        
                    with col3:
                        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
                        
                    with col1:
                        restecg = st.text_input('Resting Electrocardiographic results')
                        
                    with col2:
                        thalach = st.text_input('Maximum Heart Rate achieved')
                        
                    with col3:
                        exang = st.text_input('Exercise Induced Angina')
                        
                    with col1:
                        oldpeak = st.text_input('ST depression induced by exercise')
                        
                    with col2:
                        slope = st.text_input('Slope of the peak exercise ST segment')
                        
                    with col3:
                        ca = st.text_input('Major vessels colored by flourosopy')
                        
                    with col1:
                        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')
                        
                        
                     
                     
                    # code for Prediction
                    heart_diagnosis = ''
                    
                    # creating a button for Prediction
                    
                    if st.button('Heart Disease Test Result'):
                        # convert input data to float
                        #input_data = [float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), float(ca), float(thal)]
                        heart_prediction = heart_disease_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg,thalach,exang,oldpeak,slope,ca,thal]])                          
                        
                        # make prediction using model
                        #heart_prediction = heart_disease_model.predict_proba([[float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), float(ca), float(thal)]])
                        
                        #heart_prediction is equal to 1. You can use the any() method for this. 
                        
                        
                        
                        if(heart_prediction[0] == 1):  
                          heart_diagnosis = 'The person is having heart disease'
                        else:
                          heart_diagnosis = 'The person does not have any heart disease'
                        
                    st.success(heart_diagnosis)
                        
                    

                # parkinsons Prediction Page
                if (selected == 'Parkinsons Prediction'):
                    img = Image.open("F:/python code/temporary/image/3.webp")
                    st.image(img)
                    # page title
                    st.title('Parkinsons Prediction using ML')
                    col1, col2, col3, col4, col5 = st.columns(5)  
                    
                    with col1:
                        fo = st.text_input('MDVP:Fo(Hz)')
                        
                    with col2:
                        fhi = st.text_input('MDVP:Fhi(Hz)')
                        
                    with col3:
                        flo = st.text_input('MDVP:Flo(Hz)')
                        
                    with col4:
                        Jitter_percent = st.text_input('MDVP:Jitter(%)')
                        
                    with col5:
                        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')
                        
                    with col1:
                        RAP = st.text_input('MDVP:RAP')
                        
                    with col2:
                        PPQ = st.text_input('MDVP:PPQ')
                        
                    with col3:
                        DDP = st.text_input('Jitter:DDP')
                        
                    with col4:
                        Shimmer = st.text_input('MDVP:Shimmer')
                        
                    with col5:
                        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')
                        
                    with col1:
                        APQ3 = st.text_input('Shimmer:APQ3')
                        
                    with col2:
                        APQ5 = st.text_input('Shimmer:APQ5')
                        
                    with col3:
                        APQ = st.text_input('MDVP:APQ')
                        
                    with col4:
                        DDA = st.text_input('Shimmer:DDA')
                        
                    with col5:
                        NHR = st.text_input('NHR')
                        
                    with col1:
                        HNR = st.text_input('HNR')
                        
                    with col2:
                        RPDE = st.text_input('RPDE')
                        
                    with col3:
                        DFA = st.text_input('DFA')
                        
                    with col4:
                        spread1 = st.text_input('spread1')
                        
                    with col5:
                        spread2 = st.text_input('spread2')
                        
                    with col1:
                        D2 = st.text_input('D2')
                        
                    with col2:
                        PPE = st.text_input('PPE')
                        
                    
                    
                    # code for Prediction
                    parkinsons_diagnosis = ''
                    
                    # creating a button for Prediction    
                    if st.button("Parkinson's Test Result"):
                        parkinsons_prediction = parkinsons_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ,DDP,Shimmer,Shimmer_dB,APQ3,APQ5,APQ,DDA,NHR,HNR,RPDE,DFA,spread1,spread2,D2,PPE]])                          
                        
                        if (parkinsons_prediction[0] == 1):
                          parkinsons_diagnosis = "The person has Parkinson's disease"
                        else:
                          parkinsons_diagnosis = "The person does not have Parkinson's disease"
                        
                    st.success(parkinsons_diagnosis)



                # lung cancer Prediction Page
                if (selected == 'Lung Cancer Prediction'):
                    img = Image.open("F:/python code/temporary/image/4.webp")
                    st.image(img)
                    # page title
                    st.title('Lung Cancer Prediction using ML') 
                    st.markdown('Yes = 2 And No = 1')
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        AGE = st.text_input('Age')
                        
                    with col2:
                        SMOKING = st.text_input('SMOKING')
                        
                    with col3:
                        YELLOW_FINGERS = st.text_input('YELLOW_FINGERS')
                        
                    with col1:
                        ANXIETY = st.text_input('ANXIETY')
                        
                    with col2:
                        PEER_PRESSURE = st.text_input('PEER_PRESSURE')
                        
                    with col3:
                        CHRONIC_DISEASE = st.text_input('CHRONIC DISEASE')
                        
                    with col1:
                        FATIGUE = st.text_input('FATIGUE')
                        
                    with col2:
                        ALLERGY = st.text_input('ALLERGY')
                        
                    with col3:
                        WHEEZING = st.text_input('WHEEZING')
                        
                    with col1:
                        ALCOHOL_CONSUMING = st.text_input('ALCOHOL CONSUMING')
                        
                    with col2:
                        COUGHING = st.text_input('COUGHING')
                        
                    with col3:
                        SHORTNESS_OF_BREATH = st.text_input('SHORTNESS OF BREATH')
                        
                    with col1:
                        SWALLOWING_DIFFICULTY = st.text_input('SWALLOWING DIFFICULTY')
                    with col2:
                        CHEST_PAIN = st.text_input('CHEST PAIN')
                    
                    
                    # code for Prediction
                    lung_cancer_diagnosis = ''
                    
                    # creating a button for Prediction    
                    if st.button("lung cancer Test Result"):
                         lung_cancer_prediction = lung_cancer_model.predict([[AGE,SMOKING,YELLOW_FINGERS,ANXIETY,PEER_PRESSURE,CHRONIC_DISEASE,FATIGUE,ALLERGY,WHEEZING,ALCOHOL_CONSUMING,COUGHING,SHORTNESS_OF_BREATH,SWALLOWING_DIFFICULTY,CHEST_PAIN]])                          
                         
                         if(lung_cancer_prediction[0]==2):
                             
                             lung_cancer_diagnosis ="The person has lung cancer"
                         else:
                             
                             lung_cancer_diagnosis ="The person has no lung cancer"
                             
                        
                    st.success(lung_cancer_diagnosis)
                elif selected == "Profiles":
                    img = Image.open("F:/python code/temporary/image/5.png")
                    st.image(img)
                    st.subheader("User Profiles")
                    #user_result = view_all_users()
                    user_result = view_user_data(username)
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")





    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")



if __name__ == '__main__':
    main()