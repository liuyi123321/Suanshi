from io import StringIO
from pathlib import Path
import streamlit as st
import time
import os
import sys
import argparse
import time
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import pandas as pd
import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image
import shutil
def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = b+'/'+d
        if os.path.isdir(bd):
            result.append(bd)
    # print(result)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs('./yolov5-master/runs/detect'), key=os.path.getmtime)


def get_answer_jpg(uploaded_file,root1,Root):
    path = f'{get_detection_folder()}/labels'
    img = cv2.imread(f"{root1}data/images/{uploaded_file.name}")  # 读取图片
    # print(img.shape)
    f = open(f'{Root}/' + str(Path(path)) + '/' + str(uploaded_file.name.split(".")[0]) + '.txt')  # 读取txt文件
    # print(f.readline())
    SS = "all_answer"
    Data = pd.read_csv(f'{Root}/yolov5-master/{SS}.csv')
    # Data = pd.read_csv("C:/Users/fly tree/Desktop/final_detect/CRNN/yolov5-master/all_answer1.csv")  # 读取csv文件

    img_pil = Image.fromarray(img)
    cnt = 0
    while True:
        Line = f.readline()
        if Line:
            Str = Line.split()
            # print(Str)
            Str = Str[1:]
            Str = list(map(lambda x: float(x), Str))  # 坐标
            # 设置需要显示的字体
            fontpath = "font/simsun.ttc"
            font = ImageFont.truetype(fontpath, 32)
            draw = ImageDraw.Draw(img_pil)
            X_center = Str[0] * img.shape[1]  # 方框中心的x坐标
            Y_center = Str[1] * img.shape[0]  # 方框中心的y坐标
            Width = Str[2] * img.shape[1]  # 宽
            Height = Str[3] * img.shape[0]  # 高
            print(X_center - (Width / 2), Y_center - (Height / 2), X_center + (Width / 2), Y_center + (Height / 2),
                  X_center, Y_center)
            tup = (X_center+(Width / 2)-15, Y_center - (Height / 2))
            # print(tup)
            if Data.loc[cnt, 'result'] == 'false':
                draw.text(tup, "×", font=font, fill=(0, 0, 255))
            else:
                draw.text(tup, "√", font=font, fill=(0, 0, 255))
            img = np.array(img_pil)
            cv2.imshow("add_text", img)
            cnt = cnt + 1
        else:
            break

    cv2.imwrite(f'{os.getcwd()}/yolov5-master/res.jpg', img)
    f.close()

# @st.cache
def load_data():
    # os.system(
    #     f'python ./CRNN/detect.py --weights ./CRNN/weights/best.pt --source {Root}/' + str(Path(path)) + '/')
    # os.system('python ./CRNN/detect_result/examine_formulation.py')
    SS = "all_answer"
    data = pd.read_csv(f'{Root}/yolov5-master/{SS}.csv')
    Data = pd.DataFrame()
    Data['左式'] = data['left']
    Data['右式'] = data['right']
    Data['答案'] = data['answer']
    Data['结果'] = data['result']
    return Data
def get_wrong_pic(pic_id):
    target_path = 'CRNN/wrong_data/'
    shutil.copy(pic_id, target_path)

def get_pic(uploaded_file):
    for img in os.listdir(get_detection_folder()):
        # st.write(img)
        # st.write(os.path.splitext(img)[0])
        if os.path.splitext(img)[0] == uploaded_file.name.split('.')[0] and os.path.splitext(img)[1] == '.jpg':
            st.image(str(Path(f'{get_detection_folder()}') / img))

    st.subheader('答案判别：', anchor=None)
    path = f'{get_detection_folder()}/crops/equation'
    res_img_path = f'{os.getcwd()}/yolov5-master/res.jpg'
    res_img = Image.open(res_img_path)
    st.image(res_img)
    st.subheader('算式切割，请选出判断错误的算式：', anchor=None)
    equation_img = [str(Path(path) / img) for img in os.listdir(Path(path))]
    col1, col2, col3 = st.columns(3)
    with col1:
        for idx in range(len(equation_img)):
            if idx % 3 == 0:
                st.image(equation_img[idx])
                # st.write(equation_img[idx])
                st.button('Wrong',key = idx,args = (equation_img[idx],),on_click = get_wrong_pic)

    with col2:
        for idx in range(len(equation_img)):
            if idx % 3 == 1:
                st.image(equation_img[idx])
                st.button('Wrong',key = idx,args = (equation_img[idx],),on_click = get_wrong_pic)
    with col3:
        for idx in range(len(equation_img)):
            if idx % 3 == 2:
                st.image(equation_img[idx])
                st.button('Wrong',key = idx,args = (equation_img[idx],),on_click = get_wrong_pic)


if __name__ == '__main__':
    Root = os.getcwd()
    # print(Root)
    # print(get_detection_folder())
    
    st.title('手写算式识别')

    uploaded_file = st.sidebar.file_uploader(
        "上传图片", type=['png', 'jpeg', 'jpg'])
    if uploaded_file is not None:
        with st.spinner(text='加载中...'):
            # st.write(uploaded_file.name.split('.')[0])
            st.sidebar.image(uploaded_file)
            picture = Image.open(uploaded_file)
            picture = picture.save(f'yolov5-master/data/images/{uploaded_file.name}')
    root1 = './yolov5-master/'
    flag = 0
    if st.button('开始检测'):
        if uploaded_file is not None:
            time_start = time.time()  # 开始计时
            os.system(f'python {root1}/detect.py --weights {root1}best.pt --source {root1}data/images/{uploaded_file.name} --save-crop --save-txt')
            time_end = time.time()  # 结束计时
            time_a = time_end - time_start
            with st.spinner(text='Preparing Images'):
                time.sleep(0.5)
                # 枚举结果目录里的图片，并进行展示所选择的那张图片
                # get_pic(uploaded_file)
                path = f'{get_detection_folder()}/crops/equation'
                time_start = time.time()  # 开始计时
                os.system(f'python ./CRNN/detect.py --weights ./CRNN/weights/best.pt --source {Root}/'+str(Path(path))+'/')
                os.system('python ./CRNN/detect_result/examine_formulation.py')
                time_end = time.time()  # 结束计时
                time_b = time_end - time_start  # 运行所花时间
                time_c = time_a+time_b
                get_answer_jpg(uploaded_file,root1,Root)
                # print(f'{Root}/' + str(Path(path)) + '/' + str(uploaded_file.name.split(".")[0]) + '.txt')
        flag = 1
    if uploaded_file is not None or flag==1:
        get_pic(uploaded_file)
        Data = load_data()
        # corr = pd.read_csv(f'{get_detection_folder()}/{uploaded_file.name.split(".")[0]}.csv')
        corr = pd.read_csv(f'{Root}/yolov5-master/correct_rate.csv')
        if st.checkbox('Show dataframe'):
            st.write(Data)
            st.markdown("**Correct_rate:**")
            st.write(corr['correct_rate'][0])
        if st.checkbox('Shape of dataframe'):
            st.write(Data.shape)
        st.markdown('#### Data Visualization')
        fig = plt.figure()
        exp = [0, 0.1]
        labels = ['Precise', 'Error']
        X = [corr['correct_rate'][0], 1-corr['correct_rate'][0]]
        plt.pie(X, explode=exp, labels=labels, autopct='%.4f%%', pctdistance=0.8, shadow=True)
        st.pyplot(fig)
        st.subheader('用时')
        # for img in os.listdir(get_detection_folder()):
        #     if os.path.splitext(img)[0] == "res_"+uploaded_file.name.split('.')[0]:
        #         st.image(str(Path(f'{get_detection_folder()}') / img))
        #         break
        st.markdown("yolo用时：")
        st.write(time_a)
        st.markdown("CRNN用时：")
        st.write(time_b)
        st.markdown("总时长：")
        st.write(time_c)
