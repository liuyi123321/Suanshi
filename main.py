from io import StringIO
from pathlib import Path
import streamlit as st
import time
import os
import sys
import argparse
from PIL import Image
import pandas as pd


def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = b+'/'+d
        if os.path.isdir(bd):
            result.append(bd)
    #print(result)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs('./yolov5-master/runs/detect'), key=os.path.getmtime)


if __name__ == '__main__':
    Root = os.getcwd()
   # print(Root)
    #print(get_detection_folder())
    
    st.title('手写算式识别')
    uploaded_file = st.sidebar.file_uploader(
        "上传图片", type=['png', 'jpeg', 'jpg'])
    if uploaded_file is not None:
        with st.spinner(text='加载中...'):
            st.sidebar.image(uploaded_file)
            picture = Image.open(uploaded_file)
            picture = picture.save(f'yolov5-master/data/images/{uploaded_file.name}')
    root1='./yolov5-master/'
    if st.button('开始检测'):
        os.system(f'python {root1}/detect.py --weights {root1}best.pt --source {root1}data/images/{uploaded_file.name} --save-crop')

        with st.spinner(text='Preparing Images'):
            #枚举结果目录里的图片，并进行展示
            for img in os.listdir(get_detection_folder()):
                print(img,"\n")
                if os.path.splitext(img)[1]=='.jpg':
                    st.image(str(Path(f'{get_detection_folder()}') / img))
            st.header('方程切割：',anchor  = None)
            path = f'{get_detection_folder()}/crops/equation'
            for img in os.listdir(Path(path)):
                st.image(str(Path(path)/img))
            print(str(Path(path)))
            os.system(f'python ./CRNN/detect.py --weights ./CRNN/weights/best.pt --source {Root}/'+str(Path(path))+'/')
            os.system('python ./CRNN/detect_result/examine_formulation.py')
            data = pd.read_csv(f'{Root}/yolov5-master/all_answer.csv')
            Data=pd.DataFrame()
            Data['左式']=data['left']
            Data['右式']=data['right']
            Data['答案']=data['answer']
            Data['结果']=data['result']
            st.dataframe(data = Data)
            
            
                
                        

     