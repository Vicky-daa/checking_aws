from flask import Flask, render_template, request,session
import predict as pd
import sys
import boto3
import key_config as keys



s3 = boto3.client(
    service_name='s3',
    aws_access_key_id=keys.ACCESS_KEY_ID,
    aws_secret_access_key= keys.ACCESS_SECRET_KEY)

application = Flask(__name__)
app = application
app.secret_key = "Key"


@app.route("/")
def disclaimer():
    return render_template('disclaimer.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():

    prediction = "________"

    user_values = {}

    disabled = True

    if request.method == 'GET':

        session['gender'] = request.args.get('gender')
        session['smoking']  = request.args.get('smoke')
        session['vaccine']  = request.args.get('vaccine')
        session['country']  = request.args.get('country')
        session['province']  = request.args.get('state')
        session['district']  =request.args.get('district')
        session['cold']  = request.args.get('cold') != None 
        session['cough']  = request.args.get('cough') != None 
        session['fever']  = request.args.get('fever') != None
        session['diarrhoea']  = request.args.get('diarrhoea') != None
        session['sore']  = request.args.get('sore') != None
        session['smell']  = request.args.get('loss') != None
        session['muscle']  = request.args.get('muscle') != None
        session['fatigue']  = request.args.get('fatigue') != None
        session['breathing']  = request.args.get('breathing') != None
        session['pneumonia']  = request.args.get('pneumonia') != None
        session['asthma']  = request.args.get('asthma') != None
        session['chronic']  =request.args.get('chronic') != None
        session['hyper']  =request.args.get('hyper') != None
        session['heart']  = request.args.get('heart') != None
        session['diabetes']  = request.args.get('diabetes') != None
        session['covid']  = request.args.get('covid')


        
    if request.method == 'POST':
        
        user_values['gender'] = session['gender']
        user_values['smoking']  = session['smoking']
        user_values['vaccine']  = session['vaccine']
        user_values['country']  = session['country']
        user_values['province']  = session['province']
        user_values['district']  =session['district']
        user_values['cold']  = session['cold']
        user_values['cough']  = session['cough'] 
        user_values['fever']  = session['fever']
        user_values['diarrhoea']  = session['diarrhoea']
        user_values['sore']  = session['sore']
        user_values['smell']  = session['smell']
        user_values['muscle']  = session['muscle']
        user_values['fatigue']  =  session['fatigue']
        user_values['breathing']  = session['fatigue']
        user_values['pneumonia']  = session['pneumonia']
        user_values['asthma']  = session['asthma']
        user_values['chronic']  =session['chronic']
        user_values['hyper']  = session['hyper']
        user_values['heart']  = session['heart']
        user_values['diabetes']  = session['diabetes']
        user_values['covid']  = session['covid']
        file = request.files['myfile']
        prediction = pd.predict(file,s3,user_values)

        if not prediction.startswith("Please"):
            disabled = False




    
    # gender = request.args.get('gender')
    # smoking = request.args.get('smoke')
    # vaccine = request.args.get('vaccine')
    # country = request.args.get('country')
    # province = request.args.get('state')
    # district =request.args.get('district')
    # cold = request.args.get('cold') != None 
    # cough = request.args.get('cough') != None 
    # fever = request.args.get('fever') != None
    # diarrhoea = request.args.get('diarrhoea') != None
    # sore = request.args.get('sore') != None
    # smell = request.args.get('loss') != None
    # muscle = request.args.get('muscle') != None
    # fatigue = request.args.get('fatigue') != None
    # breathing = request.args.get('breathing') != None
    # pneumonia = request.args.get('pneumonia') != None
    # asthma = request.args.get('asthma') != None
    # chronic =request.args.get('chronic') != None
    # hyper =request.args.get('hyper') != None
    # heart = request.args.get('heart') != None
    # diabetes = request.args.get('diabetes') != None
    # covid = request.args.get('covid')


    


    return render_template('predict.html',values = user_values, prediction = prediction,disabled=disabled)




# if __name__ == '__main__':
#     app.run()
