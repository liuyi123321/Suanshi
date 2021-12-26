import operator
import pandas as pd
import os
result = pd.read_csv(f'{os.getcwd()}/CRNN/detect_result/result.csv')
result.dropna(inplace=True)
opMap = {'+': operator.add, '-': operator.sub, "÷": operator.truediv, "×": operator.mul}
proMap = {'(': 100, '+': 3, '-': 3, '×': 8, '÷': 8, ')': 1, '#': 0}
left_exp = []
right_exp = []
def split_exp():
    for i in result.detection:
        temp = str(i).split('=', 1)
        left_exp.append(temp[0])
        if len(temp) == 2 and temp[1].isnumeric():
            right_exp.append(float(temp[1]))
        else:
            right_exp.append(-9999999)
# 获取下个操作数
def getNext(leftExpress):
    t = leftExpress[0:1]
    if t.isnumeric():
        for s in leftExpress[1:]:
            if s.isnumeric() or s=='.':
                t += s
            else:
                break
        return t

    else:
        return t


def popStack():
    while opStack[-1] != '(':
        nStack.append(opStack.pop())
    opStack.pop()


def popStack2(s):
    pro1 = proMap[s]
    for i in range(len(opStack)):
        op = opStack[-1]
        if op == '(':
            opStack.append(s)
            break
        else:
            pro0 = proMap[op]
            if pro0 < pro1:
                opStack.append(s)
                break
            else:
                nStack.append(opStack.pop())


def calculate():
    num = len(nStack)
    i = 0
    while num > 1:
        c = nStack[i]
        if c.isnumeric() or c.split('.')[0].isnumeric():
            i+=1
        else:
            x = nStack[i-1]
            y = nStack[i-2]
            # print(x)
            # print(y)
            if c !='÷' and c != '-':
                res = opMap.get(c)(float(x),float(y))
            else:
                res = opMap.get(c)(float(y), float(x))
            nStack[i] = str(res)
            nStack.remove(x)
            nStack.remove(y)
            i = 0
        num = len(nStack)
    return nStack.pop()


def dealwith(s):
    if s.isnumeric()  or s.split('.')[0].isnumeric():
        nStack.append(s)
    elif s == '(':
        opStack.append(s)
    elif s == ')':
        popStack()
    elif opStack[-1] == '(':
        opStack.append(s)
    else:
        op = opStack[-1]
        pro0 = proMap[op]
        pro1 = proMap[s]
        if pro1 > pro0:
            opStack.append(s)
        else:
            popStack2(s)


def meger():
    while len(opStack) > 1:
        nStack.append(opStack.pop())


# express = '256/4'
opStack = ['#']
nStack = []


def run(express):
    i = 0
    l = len(express)
    while i < l:
        token = getNext(express[i:])
        dealwith(token)
        i += len(token)
    meger()
    # print(nStack)
    answer = calculate()
    return answer


if __name__ == '__main__':
    split_exp()
    flag=0
    test=0
    a1=[]
    a2=[]
    a3=[]
    a4=[]
    for i,j in zip(left_exp,right_exp):
        test+=1
        # print(i)
        answer=run(i)
        a1.append(i);
        a2.append(int(j));
        a3.append((answer))
        
        print(i,j)
        print(answer,float(j))
        if(float(answer)==float(j)):
            print('right')
            a4.append('right')
            flag+=1
        else:
            a4.append('false')
            print('false')
    print(flag/test)
    right_rate_ = {'correct_rate':[flag/test]}
    right_rate = pd.DataFrame(data=right_rate_)
    result['left']=a1;
    result['right']=a2;
    result['answer']=a3;
    result['result']=a4;
    result.to_csv(f'{os.getcwd()}/yolov5-master/all_answer.csv')
    right_rate.to_csv(f'{os.getcwd()}/yolov5-master/correct_rate.csv')
    
   
        
        