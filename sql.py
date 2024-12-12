import mysql.connector

try:
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="test"
	)
    cursor=conn.cursor(dictionary = True)
    
except mysql.connector.Error as e:
    print(e)
    print("Fail in connecting to DB")
    exit(1)
    
def getmylist():
    sql="select Item,Content,Price from myitem;"
    cursor.execute(sql)
    return cursor.fetchall()

def getalllist():
    sql="select Item,Content,Price from allitem;"
    cursor.execute(sql)
    return cursor.fetchall()

def additem(ITEM, CONTENT, PRICE):
    sql="insert into myitem (Item, Content, Price) VALUES (%s,%s,%s);"
    param=(ITEM, CONTENT, PRICE)
    cursor.execute(sql,param)
    conn.commit()
    return
    
def deleteitem(ITEM, CONTENT, PRICE):
    sql="delete from myitem where Item=%s AND Content=%s AND Price=%s;"
    param=(ITEM, CONTENT, PRICE)
    cursor.execute(sql,param)
    conn.commit()
    return

def edititem(ITEM, CONTENT, PRICE): #編輯商品資訊
    sql="update myitem set Content=%s, Price=%s where Item=%s;"
    param=(ITEM, CONTENT, PRICE)
    cursor.execute(sql,param)
    conn.commit()
    return

def updateitem(olditem, oldcontent, oldprice, newitem, newcontent, newprice): #將編輯後的商品資訊更新至資料庫
    sql = """
    UPDATE myitem
    SET Item = %s, Content = %s, Price = %s
    WHERE Item = %s AND Content = %s AND Price = %s;
    """
    params = (newitem, newcontent, newprice, olditem, oldcontent, oldprice)
    cursor.execute(sql, params)
    conn.commit()

def highestbid(ITEM, newprice): #更新最高價格
    sql = "UPDATE allitem SET Price = %s WHERE Item = %s"
    sql = "UPDATE myitem SET Price = %s WHERE Item = %s"
    params = (newprice, ITEM)
    cursor.execute(sql, params)
    conn.commit()

def insertrecord(Item, Price): #競標紀錄新增至mysql
    sql = """
    INSERT INTO bidrecord (Item, Price, Time)
    VALUES (%s, %s, NOW())
    """
    params = (Item, Price)
    cursor.execute(sql, params)
    conn.commit()

def getrecord(Item): #將競標歷史從mysql中抓下來
    sql = """
    SELECT Item, Price, Time  
    FROM bidrecord 
    WHERE Item = %s
    ORDER BY Time DESC
    """
    params = (Item,)
    cursor.execute(sql, params)
    records = cursor.fetchall()
    
    return records
