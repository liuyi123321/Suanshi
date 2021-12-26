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
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs(os.path.join('runs', 'detect')), key=os.path.getmtime)


if __name__ == '__main__':

    st.title('手写算式识别')
    uploaded_file = st.sidebar.file_uploader(
        "上传图片", type=['png', 'jpeg', 'jpg'])
    if uploaded_file is not None:
        with st.spinner(text='加载中...'):
            st.sidebar.image(uploaded_file)
            picture = Image.open(uploaded_file)
            picture = picture.save(f'data/images/{uploaded_file.name}')
            
    if st.button('开始检测'):
        os.system(f'python detect.py --weights best.pt --source data/images/{uploaded_file.name} --save-crop')

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
            os.system('python ../CRNN/detect.py --weights ../CRNN/weights/best.pt --source E:/CRNN/yolov5-master/'+str(Path(path))+'/')
            os.system('python ../CRNN/detect_result/examine_formulation.py')
            data = pd.read_csv(r'E:\CRNN\yolov5-master\all_answer.csv')
            Data=pd.DataFrame()
            Data['左式']=data['left']
            Data['右式']=data['right']
            Data['答案']=data['answer']
            Data['结果']=data['result']
            st.dataframe(data = Data)
            
                
                        

     