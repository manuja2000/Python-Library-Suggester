from flask import Flask, render_template,request,make_response
import pandas as pd

app= Flask(__name__)
df=pd.read_excel("governance_lib.xlsx")
df2=pd.read_excel("python_lib.xlsx")
cnt=1
def dropdown(i):
    loc= 0
    filename="templates/index.html"
    with open(filename, 'r') as f:
        contents = f.readlines()
        for index, line in enumerate(contents):
            if line.startswith('<!-- INSERTFIELD -->'):
                loc=index+1
    s="<fieldset>\n"
    s=s+"<label for=\"select"+str(i)+"\">"+df["Field_Names"][i]+"</label>\n"
    s=s+"<select id=\"select"+str(i)+"\" name=\"select"+str(i)+"\">\n"
    s=s+"<option value=\"none\">--- Select---</option>\n"
    for j in range(2,df.shape[1]):
        if(str(df.iloc[i][j])!="nan"):
            s=s+"<option value=\""+df.iloc[i][j]+"\">"+df.iloc[i][j]+"</option>\n"
    s=s+"</select><br/>\n</fieldset>\n"
    contents.insert(loc,s)
    with open("templates/index.html", 'w', encoding="mbcs") as f:
        f.writelines(contents)
        
def refresh():
    with open("templates/file.html", 'r', encoding="mbcs") as f:
        open("templates/index.html", "w", encoding="mbcs").close()
        contents = f.readlines()
        with open("templates/index.html", 'w', encoding="mbcs") as f:
            f.writelines(contents)

def refresh2():
    with open("templates/test.html", 'r', encoding="mbcs") as f:
        open("templates/rep_index.html", "w", encoding="mbcs").close()
        contents = f.readlines()
        with open("templates/rep_index.html", 'w', encoding="mbcs") as f:
            f.writelines(contents)
            
def take_input():  
    inp={}
    fname=request.form['firstName']
    lname=request.form['lastName']
    for i in range(0,df.shape[0]):
        s='select'+str(i)
        l=request.form[s]
        inp[df["Field_Names"][i]]=l
    report(inp)
    return (inp,fname,lname)

def report(inpp):
    inp=inpp
    refresh2()
    loc= 0
    filename="templates/rep_index.html"
    with open(filename, 'r', encoding="mbcs") as f:
        contents = f.readlines()
        for index, line in enumerate(contents):
            if line.startswith('<!-- INSERTFIELD -->'):
                loc=index+1
    for i in range(df.shape[0]-1,-1,-1):
        s="<fieldset>\n"
        s=s+"<label for=\"select"+str(i)+"\">"+df["Field_Names"][i]+"</label>\n"
        s=s+"<select id=\"select"+str(i)+"\" name=\"select"+str(i)+"\" disabled>\n"
        s=s+"<option value=\"none\">"+str(inp[df["Field_Names"][i]])+"</option>\n"
        s=s+"</select><br/>\n</fieldset>\n"
        contents.insert(loc,s)
    with open("templates/rep_index.html", 'w', encoding="mbcs") as f:
        f.writelines(contents)
        
def report2(lis):
    list_cnt=lis
    emp=[]
    if(list_cnt[0][0]>0):
        return [list_cnt[0][1],list_cnt[0][0]]
    return emp 

@app.route('/')
def home():
    refresh()
    for i in range(df.shape[0]-1,-1,-1):
        if(df.iloc[i][1]=="Dropdown"):
            dropdown(i)
    return render_template('index.html')

@app.route('/generate',methods=['POST'])
def generate():
    global lis
    global fname
    global lname
    inp={}
    inp,fname,lname=take_input()
    print(inp)
    list_cnt=find_library(inp)
    lis=report2(list_cnt)
    return render_template('rep_index.html',fname=fname,lname=lname,lis=lis)

def find_library(inp):
    list_cnt=[]
    for i in range(0,df2.shape[0]):
        cnt=0
        for j in range(1,df2.shape[1]):
            a=df2.columns[j]
            if(inp[a]==df2.iloc[i][j]):
#                 print(inp[a],df2.iloc[i][j])
                cnt=cnt+1
        print(df2.iloc[i][0])
        print(cnt)
        list_cnt.append((cnt,df2.iloc[i][0]))
        list_cnt.sort(reverse=True)
#     if(list_cnt[0][0]!=0):
#         print(list_cnt[0][1])
#         print("with",list_cnt[0][0],"matches.")
    return list_cnt
    

if __name__ == '__main__':
    app.run(debug=True)
