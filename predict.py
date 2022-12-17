import librosa as lb
import pickle
import numpy as np
import os.path
from io import StringIO
import pandas as pd
import numpy as np
import asyncio
import time
from io import BytesIO


# chec the file -> T -> extract feature and predict using the model + send the data to s3 ->T 
# return prediited + s3.status
def predict(file,s3,user_values): # to pre process and detect
    check_status = check(file)
    if check_status =='ok':
        # value,status = prediciton(file,s3)
        # check_dur = check_duration(file)
        # if check_dur == 'ok':
        value = prediciton(file,s3,user_values)
        return value # list of prediciton and s3 status

    elif check_status == 'long':
        return "Please upload audio file less than 30 sec"
    elif check_status == 'wrong':
        return "Please upload only .mp3 or .wav file"
    else:
        return "Please upload a file to predict"

    
def check(file): # to check the audio

    # return 'ok'
    if file.filename == '':
        return "no"
    elif file.filename.lower().endswith(('.mp3', '.wav')):

        print(file)
        print(file.filename)
        return 'ok'
    else:
        return "wrong"

def check_duration(file):

   
    file_bytes = file.read()
    file_like_object = BytesIO(file_bytes)

    soundArr,sample_rate=lb.load(file_like_object,sr=None)
    duration = lb.get_duration(y=soundArr, sr=sample_rate)
    if duration >30 or duration == 0:

        return "long"
    else: 
        return "ok"



def prediciton(file,s3,user_values):

    value = None
    status = None

    print(file)

    user_df=pd.DataFrame(user_values,index=[0])

    soundArr,sample_rate=lb.load(file,mono=True)
    mfcc = lb.feature.mfcc(y=soundArr,sr=sample_rate)
    cstft = lb.feature.chroma_stft(y=soundArr,sr=sample_rate)
    mSpec = lb.feature.melspectrogram(y=soundArr,sr=sample_rate)
    mfcc_val = np.array(mfcc)
    cstft_val = np.array(cstft)
    mSpec_val = np.array(mSpec)

    a = np.transpose(mfcc_val)
    b =  np.transpose(cstft_val)
    c =  np.transpose(mSpec_val)

    df = pd.DataFrame()


    for index in range(a.shape[1]):

        ser = pd.Series(data=a[:,index])
        col_name = f'mfcc{index+1}'
        df[col_name] = ser

    for index in range(b.shape[1]):

        ser = pd.Series(data=b[:,index])
        col_name = f'cstft{index+1}'
        df[col_name] = ser

    for index in range(c.shape[1]):

        ser = pd.Series(data=c[:,index])
        col_name = f'mSpec{index+1}'
        df[col_name] = ser

    df_mean = df.mean()
    cols = df_mean.index
    df_mean = df_mean.values.reshape((1,-1))

    df_mean = pd.DataFrame(df_mean,columns= cols,index=[0])

    final_df = pd.concat([user_df, df_mean], axis=1)

    final_columns = final_df.columns

    #cough detection

    # cough_prob = None

    # resp_model = model_from_json("respi_model.json")

    # if cough_prob is None:
    #     pass 
    # elif cough_prob > 70:
    #     value = resp_model.predict({"mfcc":mfcc_val,"croma":cstft_val,"mpsec":mSpec_val})
    # else:
    #     value = cough_model.predict({"mfcc":mfcc_val,"croma":cstft_val,"mpsec":mSpec_val})

    # df = pd.DataFrame()

    

    status = upload_s3(s3,final_df,final_columns)

    # with open("cos_cough_90.json", 'r') as f:
    #     model_json = f.read()
    
    # model = model_from_json(model_json)

    

    # value = model.predict({"mfcc":mfcc_val,"croma":cstft_val,"mpsec":mSpec_val})


    # value = value + model_prediction

    return status

def upload_s3(s3,df,cols):

    df_s3 = None


    try:
        obj = s3.get_object(Bucket="dataset-audico", Key="dataset.csv")
        file_obj = obj['Body']
        df_s3 = pd.read_csv(file_obj, sep=',', header=0, names=cols)
    except:
        pass

    
   

    if df_s3 is None:

        #create data frame and push the feature and upload

        # create and push
        # upload
        
        csv_buf = StringIO()
        df.to_csv(csv_buf,header=True,index=False)
        csv_buf.seek(0)


        try:
            s3.put_object(Bucket="dataset-audico",Body=csv_buf.getvalue(),Key="dataset.csv")

            status = "success"

        except:

            status = "error"

        return status

    else:


        full_df = pd.concat([df_s3,df],axis=0,ignore_index=True)
        csv_buf = StringIO()
        full_df.to_csv(csv_buf,header=True,index=False)
        csv_buf.seek(0)


        try:
            s3.put_object(Bucket="dataset-audico",Body=csv_buf.getvalue(),Key="dataset.csv")

            status = "success"

        except:

            status = "error"

        return status



