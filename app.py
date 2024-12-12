from flask import Flask, render_template, request, session, redirect
from functools import wraps
from sql import getmylist,getalllist,additem,deleteitem,edititem,updateitem,highestbid,insertrecord,getrecord

app=Flask(__name__)
app.config['SECRET_KEY'] = '123TyU%^&'

id='uuuu'
password='8888'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form = request.form
        user_id = form['ID']
        user_password =form['password']

        if user_id == 'uuuu' and user_password == '8888':
            session['login']=user_id
            return redirect("/allitem")
        else:
            session['login']=False
            return redirect("/login")
    return render_template('login.html')

@app.route("/myitem")
def myitem():
    dat1=getmylist()
    return render_template('myitem.html', data=dat1)

@app.route("/allitem")
def allitem():
    dat1=getmylist()
    dat2=getalllist()
    return render_template('allitem.html', data=dat1+dat2)

@app.route('/add', methods=['POST'])
def add():
    form =request.form
    ITEM = form['ITEM'] 
    CONTENT =form['CONTENT']
    PRICE = form['PRICE']
    additem(ITEM, CONTENT, PRICE)
    return redirect("/myitem")

@app.route('/delete', methods=['POST'])
def delete():
    ITEM = request.form['ITEM'] 
    CONTENT =request.form['CONTENT']
    PRICE = request.form['PRICE']
    deleteitem(ITEM, CONTENT, PRICE)
    return redirect("/myitem") 

@app.route('/edititem', methods=['GET'])
def edititem():
    if request.method == 'POST':
        pass
    else:
        ITEM = request.args.get('ITEM')
        CONTENT = request.args.get('CONTENT')
        PRICE = request.args.get('PRICE')
        return render_template('edititem.html', Item = ITEM, Content = CONTENT, Price = PRICE)

@app.route('/saveitem', methods=['POST'])
def saveitem(): #儲存用戶新增的商品
    newitem = request.form['newitem']
    newcontent = request.form['newcontent']
    newprice = request.form['newprice']
    
    olditem = request.form['olditem']
    oldcontent = request.form['oldcontent']
    oldprice = request.form['oldprice']
    
    if not newitem:
        newitem = olditem
    if not newcontent:
        newcontent = oldcontent
    if not newprice:
        newprice = oldprice

    updateitem(olditem, oldcontent, oldprice, newitem, newcontent, newprice)
    return redirect("/myitem")

@app.route('/bid', methods=['GET', 'POST'])
def bid():
    if request.method == 'GET': #GET獲得商品資訊
        ITEM = request.args.get('ITEM')
        CONTENT = request.args.get('CONTENT')
        PRICE = request.args.get('PRICE')
        
        return render_template('bid.html', Item=ITEM, Content=CONTENT, Price=PRICE)
    
    elif request.method == 'POST': #POST進行競標
        ITEM = request.form['ITEM']
        PRICE = float(request.form['PRICE'])
        newbidprice = float(request.form['newbidprice'])
        bidder = session.get('login')  #session追蹤用戶

        if newbidprice > PRICE:
            highestbid(ITEM, newbidprice)
            insertrecord(ITEM, newbidprice)
            return redirect('/allitem')
        else:
            return "競標價格必須高於目前價格", 400

@app.route('/bidrecord', methods=['POST'])
def bidrecord_route():
    ITEM = request.form['ITEM']
    bidrecord = getrecord(ITEM) #用ITEM查詢已上架商品

    return render_template('bidrecord.html', records=bidrecord, Item=ITEM)

