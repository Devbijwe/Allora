
from ast import Pass
from optparse import Option
import time
import pyqrcode
import png
import tempfile
from captcha.image import ImageCaptcha
from PIL import Image
from itertools import product
import os
from tokenize import String
from werkzeug.utils import secure_filename
import random
import secrets
import string
import json
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError 
from flask import Flask,render_template,session,redirect,request,flash,jsonify
from jinja2 import Template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import cv2
from sqlalchemy.orm import load_only



with open("config.json","r") as c:
    params=json.load(c)['params']
with open("config.json","r") as d:
    navs=json.load(d)['navs']
with open("config.json","r") as e:
    subnavs=json.load(e)['subnavs']
with open("config.json","r") as f:
    uploads=json.load(f)['uploads']
    

app=Flask(__name__,template_folder="Templates")
app.secret_key='sdx2323@3343zbhcfew3rr3343@@###$2ffr454'
if (params['local_server']):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params['prod_url']



db=SQLAlchemy(app)    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
class Admins(db.Model):
    srNo=db.Column(db.Integer,primary_key=True)
    adminId=db.Column(db.Integer,nullable=True)
    adminName=db.Column(db.String(50),nullable=False)
    adminEmail=db.Column(db.String(50),nullable=False)
    adminMob=db.Column(db.String(15),nullable=False)
    adminPasswd=db.Column(db.String(20),nullable=False)
    emergencyKey=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(12),nullable=True)
class Customers(db.Model):
    custId=db.Column(db.Integer,primary_key=True)
    custName=db.Column(db.String(50),nullable=False)
    custEmail=db.Column(db.String(50),nullable=True)
    custMobile=db.Column(db.String(15),nullable=False)
    custPasswd=db.Column(db.String(20),nullable=False)
    custDoB=db.Column(db.String(15),nullable=False)
    custAddress=db.Column(db.String(200),nullable=False)
    custAddress2=db.Column(db.String(100),nullable=True)
    custCity=db.Column(db.String(30),nullable=False)
    custState=db.Column(db.String(50),nullable=False)
    custZip=db.Column(db.String(10),nullable=False)
    custImg=db.Column(db.String(25),nullable=True)
    custdate=db.Column(db.String(12),nullable=True)
    

class Orders(db.Model):
    orderId=db.Column(db.Integer,primary_key=True)
    customerId=db.Column(db.Integer,nullable=False)
    productId=db.Column(db.Integer,nullable=True)
    sellerId=db.Column(db.Integer,nullable=True)
    products=db.Column(db.JSON,nullable=True)
    quantity=db.Column(db.JSON,nullable=True)
    noOfProducts=db.Column(db.Integer,nullable=True)
    mode_Of_Payment=db.Column(db.String(30),nullable=False)
    total=db.Column(db.Integer,nullable=False)
    isDelivered=db.Column(db.Integer,nullable=False)
    date=db.Column(db.String(12),nullable=True)
    
class Products(db.Model):
    prodId=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(500),nullable=False)
    longDesc=db.Column(db.String(2000),nullable=True)
    tags=db.Column(db.String(100),nullable=True)
    img1=db.Column(db.String(100),nullable=True)
    img2=db.Column(db.String(100),nullable=True)
    img3=db.Column(db.String(100),nullable=True)
    img4=db.Column(db.String(100),nullable=True)
    price=db.Column(db.Integer,nullable=False)
    soldBy=db.Column(db.String(50),nullable=False)
    available=db.Column(db.String(20),nullable=True)
    date=db.Column(db.String(12),nullable=True)


class Sellers(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    LicenseId=db.Column(db.String(50),nullable=False)
    Email=db.Column(db.String(50),nullable=True)
    Mobile=db.Column(db.String(15),nullable=False)
    Passwd=db.Column(db.String(20),nullable=False)
    DoB=db.Column(db.String(15),nullable=False)
    Address=db.Column(db.String(200),nullable=False)
    Address2=db.Column(db.String(100),nullable=True)
    City=db.Column(db.String(30),nullable=False)
    State=db.Column(db.String(50),nullable=False)
    Zip=db.Column(db.String(10),nullable=False)
    Company=db.Column(db.String(100),nullable=False)
    Website=db.Column(db.String(100),nullable=True)
    date=db.Column(db.String(12),nullable=True)

class Messages(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    msgFrom=db.Column(db.String(15),nullable=False)
    msgTo=db.Column(db.String(15),nullable=True)
    msgDetail=db.Column(db.String(1000),nullable=True)
    fromType=db.Column(db.String(15),nullable=False)
    endReceiver=db.Column(db.String(15),nullable=False)
    date=db.Column(db.String(12),nullable=True)
class Customize(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    userType=db.Column(db.String(15),nullable=False)
    userId=db.Column(db.String(15),nullable=False)
    navColour=db.Column(db.String(15),nullable=True)
    subnavColour=db.Column(db.String(15),nullable=True)
    allNavTextColour=db.Column(db.String(15),nullable=True)
    footerColour=db.Column(db.String(15),nullable=True)
    date=db.Column(db.String(12),nullable=True)
class Carts(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    customerId=db.Column(db.Integer,nullable=False)
    productId=db.Column(db.Integer,nullable=False)
    quantity=db.Column(db.Integer,nullable=True)

class Reviews(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    rating=db.Column(db.Integer,nullable=False)
    description=db.Column(db.String(1000),nullable=True)
    customerId=db.Column(db.Integer,nullable=False)
    productId=db.Column(db.Integer,nullable=False)
    sellerId=db.Column(db.Integer,nullable=False)
    date=db.Column(db.String(12),nullable=True)

class Activitycust(db.Model):
    Id=db.Column(db.Integer,primary_key=True) 
    custId=db.Column(db.Integer,nullable=False)
    details=db.Column(db.String(500),nullable=True)
    link=db.Column(db.String(200),nullable=True)
    date=db.Column(db.String(12),nullable=True)
    
class Wishlist(db.Model):
    Id=db.Column(db.Integer,primary_key=True) 
    custId=db.Column(db.Integer,nullable=False)
    prodId=db.Column(db.Integer,nullable=False)
    rating=db.Column(db.Integer,nullable=False)
    date=db.Column(db.String(12),nullable=True)
    
with app.app_context():
    db.create_all()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route("/admin/home/inbox/<string:srNo>=view",methods=['GET','POST'] )
def admin_inbox_user(srNo):
    
    if 'admin' in session:
        customers=Customers.query.filter_by(custId=srNo).first()
        msg=Messages.query.filter_by(endReceiver=srNo).all()
        return render_template("home_inbox.html",msg=msg,customers=customers,mainType="Individual")
    return redirect("/")

@app.route("/wishlist=upt/<string:type>=<string:id>",methods=['GET','POST'])
def wishUpdate(type,id):
    if 'user' in session:
        data=Customers.query.filter_by(custMobile=session['user']).first()
        prod=Products.query.filter_by(prodId=id).first()
        review=Reviews.query.filter_by(productId=prod.prodId).all()
        sum=0
        for items in review:
            sum=+items.rating
        avg=sum/len(review)
        if type=="add":
            try:
                cred=Wishlist(custId=data.custId,prodId=prod.prodId,rating=avg,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            except IntegrityError:
                time.sleep(0.3)
                return redirect("/")
        elif type=="del":  
            cred=Wishlist.query.filter_by(custId=data.custId,prodId=id).all()
            db.session.delete(cred)
            db.session.commit()
            time.sleep(0.3)
    return redirect("/")
            
@app.route("/wishlist=view",methods=['GET','POST'])
def wishlist():
    if 'user' in session:
        prod=[]
        data=Customers.query.filter_by(custMobile=session['user']).first()
        wishes=Wishlist.query.filter_by(custId=data.custId).all()
        for key in wishes:
            prod+=Products.query.filter_by(prodId=key.prodId).all()
        return render_template("wishlist.html",wishes=wishes,prod=prod)
    flash("Pls login to access Wishlist")
    return redirect("/")
  
@app.route("/customize",methods=['GET','POST'])
def customize():
    cust=Customers.query.filter_by(custMobile=session['user']).first()
    
    if request.method=='POST':
        customize=Customize.query.filter_by(userId=cust.custId).first()
        nav=request.form.get("colourNav")
        subnav=request.form.get("colourSubnav")
        navtextcolour=request.form.get("navtextcolour")
        footercolour=request.form.get("footercolour")
        if customize:
            customize.navColour=nav
            customize.subnavColour=subnav
            customize.allNavTextColour=navtextcolour
            customize.footerColour=footercolour
            db.session.commit()
        else:
            cred=Customize(userType="customers",userId=cust.custId,navColour=nav,subnavColour=subnav,allNavTextColour=navtextcolour,footerColour=footercolour,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        
    return redirect("/account/customers")
    

@app.route("/msg/add/<string:mainstr>/<string:id>=add",methods=['GET','POST'])
def msg(mainstr,id):
    if 'user' in session and mainstr=="customer":
        cust=Customers.query.filter_by(custMobile=session['user']).first()
        msg=Messages.query.filter_by(endReceiver=cust.custId).all()
        if request.method=='POST':
            msgDetail=request.form.get("msgBrief")
            msgTo='Admin'
            msgFrom=cust.custId
            fromType='customers'
            endReceiver=cust.custId
            if msgDetail:
                cred=Messages(msgFrom=msgFrom,msgTo=msgTo,msgDetail=msgDetail,fromType=fromType,endReceiver=endReceiver,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
                time.sleep(0.5)
    elif 'admin' in session and mainstr=="admin":
        
        msg=Messages.query.filter_by(endReceiver=id).all()
        if request.method=='POST':
            msgDetail=request.form.get("msgBrief")
            msgTo='Customer'
            msgFrom="Admin"
            fromType='Admin'
            endReceiver=id
            if msgDetail:
                cred=Messages(msgFrom=msgFrom,msgTo=msgTo,msgDetail=msgDetail,fromType=fromType,endReceiver=endReceiver,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
                time.sleep(0.5)
                strng="/admin/home/inbox/"+str(id)+"=view"
            return redirect(strng)
    return redirect("/account/customers")
@app.route("/cancel/order/<string:orderId>=order",methods=['GET','POST'])
def cancelOrder(orderId):
    order=Orders.query.filter_by(orderId=orderId).first()
    db.session.delete(order)
    db.session.commit()
    flash("Order cancelled successfully")
    return redirect("/account/customers")
    
@app.route("/checkout/<string:mainstr>/<string:prodId>=order",methods=['GET','POST'])
def checkOut(mainstr,prodId):
    if 'user' in session:
        if request.method=="POST":
            Total=request.form.get("Total")
            data=Customers.query.filter_by(custMobile=session['user']).first()
            pid=[]
            pqty=[]
            noOfProducts=1
            if mainstr=='cart':  
                option='cart' 
                prodId='1'
                prod=[]
                data=Customers.query.filter_by(custMobile=session['user']).first()
                cart=Carts.query.filter_by(customerId=data.custId).all()
                for key in cart:
                    pqty.append(key.quantity)
                    
                noOfProducts=len(cart)
                for index in cart:
                    prod+=Products.query.filter_by(prodId=index.productId).all() 
                
            else:
                option='nocart'
                prodId=prodId
                cart=[{'quantity':1}]
                data=Customers.query.filter_by(custMobile=session['user']).first()
                prod=Products.query.filter_by(prodId=prodId).all() 
                noOfProducts=1
                pqty.append(1)
            for item in prod:
                pid.append( item.prodId)
                
                
                
            cred=Orders(customerId=data.custId,products=pid,quantity=pqty, noOfProducts=noOfProducts,mode_Of_Payment='cod',total=Total,isDelivered=False,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
            flash("order placed successfully...")
            return redirect("/account/customers")
        
        else:
            if mainstr=='cart': 
                option='cart'  
                prodId='1'
                prod=[]
                data=Customers.query.filter_by(custMobile=session['user']).first()
                cart=Carts.query.filter_by(customerId=data.custId).all()
                for index in cart:
                    prod+=Products.query.filter_by(prodId=index.productId).all() 
            else:
                option='nocart'
                prodId=prodId
                cart=[{'quantity':1}]
                data=Customers.query.filter_by(custMobile=session['user']).first()
                prod=Products.query.filter_by(prodId=prodId).all() 
       
        num = 6 
        res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))  
        image= ImageCaptcha(width=300,height=100)
        captchaText= str(res)
        captcha=image.generate(captchaText)
        image.write(captchaText,os.path.abspath("../"+uploads['imgCaptcha'])+'/captcha1.png')
        return render_template("checkOut.html",prodId=prodId, data=data,cart=cart,prod=prod,captchaText=captchaText,option=option)
    else:
        return redirect("/login/customers")

@app.route("/reviews/<string:prodId>=view",methods=['GET','POST'])
def reviews(prodId):
    cust=[]
    prod=Products.query.filter_by(prodId=prodId).all()
    review=Reviews.query.filter_by(productId=prodId).all()
    for items in review:
        cust+=Customers.query.filter_by(custId=items.customerId).all()
    link="https://127.0.0.1:8000/reviews/"+prodId+"=view"
    qr_code=pyqrcode.create(link)
    qr_code.png(os.path.abspath("../"+uploads['imgShare'])+'/qr_code1.png',scale=5)
    return render_template("reviews.html",prod=prod,review=review,cust=cust)    
 
 



@app.route("/customers/profUpload/<string:custId>",methods=['GET','POST'])
def profUploader(custId):
    if 'user' in session and request.method=="POST":
        data=Customers.query.filter_by(custId=custId).first()
        app.config['UPLOAD_FOLDER']= os.path.abspath("../"+uploads['custImgUpload']) 
        profImg=request.files["profileImg"]
        profImgName="cust"+str(data.custId)+profImg.filename
        profImg.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(profImgName)))
        data.custImg=secure_filename(profImgName)
        db.session.commit()
        flash("Your Profile Photo Updated successfully...")
    return redirect("/account/customers")
 
@app.route("/account/cart/<string:mainstr>/<string:prodId>/<string:quantity>",methods=['GET','POST'])
def addtoCart(mainstr,prodId,quantity):
    if 'user' in session:
        cust=Customers.query.filter_by(custMobile=session['user']).first()
        prod=Products.query.filter_by(prodId=prodId).first()
        if mainstr=='add':
            cart=Carts.query.filter_by(customerId=cust.custId , productId=prod.prodId).first()
            if cart==None:
                cred=Carts(customerId=cust.custId,productId=prod.prodId,quantity=quantity)
                db.session.add(cred)
                db.session.commit()
            else:
                cart=Carts.query.filter_by(customerId=cust.custId , productId=prod.prodId).first()
                cart.quantity+=1
                db.session.commit()
        elif mainstr=='remove':
            cartItem=Carts.query.filter_by(customerId=cust.custId,productId=prod.prodId).first()
            db.session.delete(cartItem)
            db.session.commit()
            return redirect("/cart")
        return redirect("/")
    else: 
        return redirect("/login/customers")
        
     
 
   
    
@app.route("/signup/<string:mainstr>",methods=['GET','POST'])
def signup(mainstr):
    if mainstr=='customers':
        if 'user' in session:
            return redirect("/")
        if (request.method=='POST'):
            fullName=request.form.get("fullName")
            dob=request.form.get("dob")
            phone=request.form.get("phoneNo")
            email=request.form.get("email")
            password=request.form.get("password")
            repassword=request.form.get("repassword")
            address=request.form.get("Address")
            address2=request.form.get("Address2")
            city=request.form.get("city")
            state=request.form.get("state")
            zip=request.form.get("zip")
            if(password==repassword):
                cred=Customers(custName= fullName,custMobile=phone,custDoB=dob,custEmail=email,custPasswd=password,custAddress=address,custAddress2=address2,custCity=city,custState=state,custZip=zip,custdate=datetime.now())
                try: 
                    db.session.add(cred)
                    db.session.commit()
                    return redirect("/login/customers")
                except IntegrityError:
                    flash("User "+ str(phone) +" already Exists")
                    return render_template("signup.html",params=params,navs=navs,pageDisplay=mainstr)
            else:
                flash("Password and retype-Password are not matching")
                return redirect("/signup/customers")
               
        else:
            return  render_template("signup.html",params=params,navs=navs,pageDisplay=mainstr)
    
    elif mainstr=='sellers':
        if (request.method=='POST'):
            if (request.method=='POST'):
                fullName=request.form.get("fullName")
                dob=request.form.get("dob")
                phone=request.form.get("phoneNo")
                email=request.form.get("email")
                password=request.form.get("password")
                repassword=request.form.get("repassword")
                address=request.form.get("Address")
                address2=request.form.get("Address2")
                city=request.form.get("city")
                state=request.form.get("state")
                zip=request.form.get("zip")
                Company=request.form.get("Company")
                LicenseId=request.form.get("LicenseId")
                Website=request.form.get("Website")
                if(password==repassword):
                    cred=Sellers(Name=fullName,Mobile=phone,DoB=dob,Email=email,Company=Company,LicenseId=LicenseId,Website=Website,Passwd=password,Address=address,Address2=address2,City=city,State=state,Zip=zip,date=datetime.now())
                    try: 
                        db.session.add(cred)
                        db.session.commit()
                        return redirect("/login/sellers")
                    except IntegrityError:
                        flash("User "+ str(phone) +" already Exists")
                        return render_template("signup.html",params=params,navs=navs,pageDisplay=mainstr)
                else:
                    flash("Password and retype-Password are not matching")
                    return redirect("/signup/sellers")
        else:
            return  render_template("signup.html",params=params,navs=navs,pageDisplay=mainstr)
    
@app.route("/admin/<string:mainstr>/<string:substr>")
def admin(mainstr,substr):
    if 'admin' in session:
        if mainstr=='home':
            if substr=='inbox':
                customers=Customers.query.all()
                msgFirst=Messages.query.all()
                msgFromLi=[]
                msgFromLiArr=[]
                for item in msgFirst:
                    msgFromLi.append(item.msgFrom)
                msgFromSet=set(msgFromLi) 
                for item in list(msgFromSet):
                    msgFromLiArr.append(Messages.query.filter_by(msgFrom=item).first()  )
                return render_template("home_inbox.html",msgFromSet=msgFromSet,msg=msgFromLiArr,customers=customers,mainType='Group')
        elif mainstr=='dashboard':
            if substr=='overview':
                seller=Sellers.query.filter_by(date=12/12/2022).all()
                cust=Customers.query.all()
                orders=Orders.query.all()
                flash("Hello "+session['admin']+" , Your Dashboard is ready")
                return render_template("dash_overview.html",sellers=seller,custs=cust,orders=orders)
        elif mainstr=='data':
            if substr=='customers':
                customers=Customers.query.all()
                
                return render_template("data_customers.html",customers=customers) 
            elif substr=='products':
                products=Products.query.all()
               
                return render_template("data_products.html",products=products) 
            elif substr=='sellers':
                sellers=Sellers.query.all()
                
                return render_template("data_sellers.html",sellers=sellers)
            elif substr=='orders':
                orders=Orders.query.all()
               
                return render_template("data_orders.html",orders=orders)
            elif substr=='admins':
                admins=Admins.query.all()
               
                return render_template("data_admins.html",admins=admins)    
        else:
            
           
            return render_template("admin.html")
    else:
        return redirect("/")

@app.route("/admin/data/<string:mainstr>/delete/<string:srNo>",methods=['GET','POST'])
def admin_data_delete(mainstr,srNo):
    if 'admin' in session:
        if mainstr=='customers':
            data=Customers.query.filter_by(custId=srNo).first()
            db.session.delete(data)
            db.session.commit()
            flash("Deleted Successfully...")
            return redirect("/admin/data/customers")

@app.route("/admin/data/<string:mainstr>/edit/<string:srNo>",methods=['GET','POST'])
def admin_data_editor(mainstr,srNo):
    if 'admin' in session:
        if mainstr=='customers':
            if request.method=="POST":
                fullName=request.form.get("fullName")
                dob=request.form.get("dob")
                phone=request.form.get("phoneNo")
                email=request.form.get("email")
                password=request.form.get("password")
                address=request.form.get("Address")
                address2=request.form.get("Address2")
                city=request.form.get("city")
                state=request.form.get("state")
                zip=request.form.get("zip")
                if srNo=='0':
                    cred=Customers(custName= fullName,custMobile=phone,custDoB=dob,custEmail=email,custPasswd=password,custAddress=address,custAddress2=address2,custCity=city,custState=state,custZip=zip,custdate=datetime.now())
                    try:
                        db.session.add(cred)
                        db.session.commit()
                        flash("New Entry Successfully Added..")
                        return redirect("/admin/data/customers")
                    except IntegrityError:
                        flash("User "+ str(phone) +" already Exists")
                else:
                    data=Customers.query.filter_by(custId=srNo).first()
                    data.custName=fullName
                    data.custDoB=dob
                    data.custMobile=phone
                    data.custEmail=email
                    data.custPasswd=password
                    data.custAddress=address
                    data.custAddress2=address2
                    data.custCity=city
                    data.custState= state
                    data.custZip=zip
                    db.session.commit()
                    flash("Changes Applied Successfully...")
                    return redirect("/admin/data/customers")
            if srNo=="0":
                data={"srNo":"0"}    
            else:
                data=Customers.query.filter_by(custId=srNo).first()
            
        elif mainstr=='products':
            if request.method=="POST":
                Name=request.form.get("Name")
                Desc=request.form.get("Desc")
                LongDesc=request.form.get("LongDesc")
                Tags=request.form.get("Tags")
                Img=request.form.get("Img")
                Price=request.form.get("Price")
                Available=request.form.get("Available")
                Seller=request.form.get("Seller")
                if srNo=='0':
                    cred=Products(name=Name,description=Desc,longDesc=LongDesc,tags=Tags,img=Img,price=Price,soldBy=Seller,available=Available)
                    db.session.add(cred)
                    db.session.commit()
                    flash("New Entry Successfully Added..")
                    return redirect("/admin/data/products")
                else:
                    data=Products.query.filter_by(prodId=srNo).first()
                    data.name=Name
                    data.description=Desc
                    data.longDesc=LongDesc
                    data.tags=Tags
                    data.img=Img
                    data.price=Price
                    data.soldBy=Seller
                    data.available=Available
                    db.session.commit()
                    flash("Changes saved Successfully...")
                    return redirect("/admin/data/products")
                
            if srNo=='0':
                data={"srNo":"0"} 
            else:
                data=Products.query.filter_by(prodId=srNo).first()
                
        elif mainstr=='sellers':
            if request.method=="POST":
                fullName=request.form.get("fullName")
                dob=request.form.get("dob")
                phone=request.form.get("phoneNo")
                email=request.form.get("email")
                password=request.form.get("password")
                address=request.form.get("Address")
                address2=request.form.get("Address2")
                city=request.form.get("city")
                state=request.form.get("state")
                zip=request.form.get("zip")
                company=request.form.get("Company")
                license=request.form.get("LicenseId")
                website=request.form.get("Website")
                if srNo=='0':
                    cred=Sellers(Name=fullName,Mobile=phone,DoB=dob,Email=email,Company=company,LicenseId=license,Website=website,Passwd=password,Address=address,Address2=address2,City=city,State=state,Zip=zip,date=datetime.now())
                    
                    db.session.add(cred)
                    db.session.commit()
                    flash("New Entry Successfully Added..")
                    return redirect("/admin/data/sellers")
                    
                else:
                    data=Sellers.query.filter_by(Id=srNo).first()
                    data.Name=fullName
                    data.DoB=dob
                    data.Mobile=phone
                    data.Email=email
                    data.Passwd=password
                    data.Address=address
                    data.Address2=address2
                    data.City=city
                    data.State= state
                    data.Zip=zip
                    data.Company=company
                    data.Website=website
                    data.LicenseId=license
                    db.session.commit()
                    flash("Changes Applied Successfully...")
                    return redirect("/admin/data/sellers")
            if srNo=="0":
                data={"srNo":"0"}    
            else:
                data=Sellers.query.filter_by(Id=srNo).first()
        return render_template("admin_data_editor.html",data=data,page_Display=mainstr,srNo=srNo)
    else:
        return redirect("/")
@app.route("/",methods=['GET','POST'])
def home():
    if 'user' in session:
        cred=Customers.query.filter_by(custMobile=session['user']).first()

    elif 'seller' in session:
        cred=Sellers.query.filter_by(Mobile=session['seller']).first()
        
    
           
    prod=Products.query.all()
    rev=Reviews.query.all()
   
    return render_template("index.html",params=params,navs=navs,subnavs=subnavs,prod=prod,review=rev)


@app.route("/login/<string:mainstr>",methods=['GET','POST'])
def login(mainstr):
    if mainstr=='customers':
        if 'user' in session:
            return redirect("/")
        elif 'admin' in session:
            return redirect("/admin/0/0")
        if (request.method=="POST"):
            username=request.form.get("username")
            password=request.form.get("password")  
            
            try:
                admin=Admins.query.filter_by(adminEmail=username).first()
                cred=Customers.query.filter_by(custMobile=username).first()
                if (admin != None and username==admin.adminEmail and password==admin.adminPasswd):
                    session['admin']=username
                    flash("hello Admin")
                    return redirect("/admin/dashboard/overview")
                elif (username== cred.custMobile and password==cred.custPasswd):
                    session['user']=username
                    cred=Customers.query.filter_by(custMobile=session['user']).first()
                    flash("Hello, "+cred.custName)
                    return redirect("/")
                else:
                    flash('You have Entered Wrong Credentials !!!')
                    return render_template("login.html",params=params,navs=navs,pageDisplay=mainstr)
            except AttributeError:
                flash('You have Entered Wrong Credentials !!!')
                return render_template("login.html",params=params,navs=navs,pageDisplay=mainstr)  
        else:       
            return render_template("login.html",params=params,navs=navs,pageDisplay=mainstr)
    if mainstr=='sellers':
        if 'seller' in session:
            flash("You are already logged in as seller")
            return redirect("/")
        if (request.method=="POST"):
            username=request.form.get("username")
            password=request.form.get("password")  
            
            try:
                cred=Sellers.query.filter_by(Mobile=username).first()
               
                if (username== cred.Mobile and password==cred.Passwd):
                    session['seller']=username
                    cred=Sellers.query.filter_by(Mobile=session['seller']).first()
                    flash("Hello, "+cred.Name)
                    return redirect("/")
                else:
                    flash('You have Entered Wrong Credentials !!!')
                    return render_template("login.html",params=params,navs=navs,pageDisplay=mainstr)
            except AttributeError:
                flash('You have Entered Wrong Credentials !!!')
                return render_template("login.html",params=params,navs=navs,pageDisplay=mainstr)  
        else:       
            return render_template("login.html",params=params,navs=navs,pageDisplay=mainstr)
    
@app.route("/account/<string:mainstr>",methods=['GET','POST'])  
def account(mainstr):
    if mainstr=='customers' and 'user' in session:
        
        prod=[]
        ordProd=[]
        ordqty=[]
        data=Customers.query.filter_by(custMobile=session['user']).first()
        cart=Carts.query.filter_by(customerId=data.custId).all()
        order=Orders.query.filter_by(customerId=data.custId).all()
        msg=Messages.query.filter_by(endReceiver=data.custId).all()
       
        for items in order:
            
            for key in items.products:
                print(key)
                ordqty+={key}
                
                
                
            for key in items.products:
                ordProd+=Products.query.filter_by(prodId=key).all() 
        
        for index in cart:
            prod+=Products.query.filter_by(prodId=index.productId).all() 
        prodAll=Products.query.all()
        return render_template("account.html",msg=msg,prodAll=prodAll,data=data,ordqty=ordqty,order=order,cart=cart,prod=prod,ordProd=ordProd)
    if mainstr=='sellers' and 'seller' in session:
        data=Sellers.query.filter_by(Mobile=session['seller']).first()
        prod=Products.query.filter_by(soldBy=data.Id).all() 
        order=Orders.query.filter_by()
        return render_template("account.html",data=data,products=prod)   
    else:
        return redirect("/")
@app.route("/account/sellers/products/edit/<string:srNo>", methods=["GET",'POST'])
def sellerProdEdit(srNo):
    if 'seller' in session:
        seller=Sellers.query.filter_by(Mobile=session['seller']).first()
        
        if request.method=="POST":
            
            app.config['UPLOAD_FOLDER']= os.path.abspath("../"+uploads['prodImgUpload']) 
            Name=request.form.get("Name")
            Desc=request.form.get("Desc")
            LongDesc=request.form.get("LongDesc")
            Tags=request.form.get("Tags")
            Price=request.form.get("Price")
            Available=request.form.get("Available")
        
            if srNo=='0':
                
                cred=Products(soldBy=seller.Id,name=Name,description=Desc,longDesc=LongDesc,tags=Tags,price=Price,available=Available)
                db.session.add(cred)
                db.session.commit()
                flash("New Entry Successfully Added..")
                return redirect("/account/sellers")
            else:
                
                data=Products.query.filter_by(prodId=srNo).first()
                Img1=request.files["Img1"]
                Img2=request.files["Img2"]
                Img3=request.files["Img3"]
                Img4=request.files["Img4"]
                Img1Name=str(data.prodId)+"1"+Img1.filename
                if Img1Name != str(data.prodId)+"1":
                    Img1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(Img1Name)))
                    data.img1=secure_filename(Img1Name)
                Img2Name=str(data.prodId)+"2"+Img2.filename
                if Img2Name !=str(data.prodId)+"2":
                    Img2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(Img2Name)))
                    data.img2=secure_filename(Img2Name)
                Img3Name=str(data.prodId)+"3"+Img3.filename
                if Img3Name !=str(data.prodId)+"3":
                    Img3.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(Img3Name)))
                    data.img3=secure_filename(Img3Name)
                Img4Name=str(data.prodId)+"4"+Img4.filename
                if Img4Name !=str(data.prodId)+"4":
                    Img4.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(Img4Name)))
                    data.img4=secure_filename(Img4Name)
                data.name=Name
                data.description=Desc
                data.longDesc=LongDesc
                data.tags=Tags
                data.price=Price
                data.soldBy=seller.Id
                data.available=Available
                db.session.commit()
                flash("Changes saved Successfully...")
                return redirect("/account/sellers")
                
        if srNo=='0':
            data={"srNo":"0"} 
        else:
            data=Products.query.filter_by(prodId=srNo).first()
        
     
    return render_template("sellerProdEditor.html",srNo=srNo,data=data)
@app.route("/account/sellers/products/delete/<string:srNo>", methods=["GET",'POST'])
def sellerProdDelete(srNo):
    review=Reviews.query.filter_by( productId=srNo).all()
    for item in review:
        db.session.delete(item)
    data=Products.query.filter_by(prodId=srNo).first()
    print(data.img1)
   
    if data.img1!=None:
        img1=os.path.abspath("../"+uploads['prodImgUpload'])+data.img1
        if os.path.exists(img1):
            os.remove(img1)
    if data.img2!=None:
        img2=os.path.abspath("../"+uploads['prodImgUpload'])+data.img2
        if os.path.exists(img2):
            os.remove(img2)
    if data.img3!=None:
        img3=os.path.abspath("../"+uploads['prodImgUpload'])+data.img3
        if os.path.exists(img3):
            os.remove(img3)
    if data.img4!=None:
        img4=os.path.abspath("../"+uploads['prodImgUpload'])+data.img4
        if os.path.exists(img4):
            os.remove(img4)
    flash("Deleted Successfully...")
    
    db.session.delete(data)
    db.session.commit()
    
    return redirect("/account/sellers")    
@app.route("/logout/<string:mainstr>")
def logout(mainstr):
    if mainstr=='customers':
        if 'user' in session:
            session.pop('user')
            flash("You Logged Out Successfully.")
            return redirect("/login/customers")
    if mainstr=='sellers':
        if 'seller' in session:
            session.pop('seller')
            flash("Your Seller Account Logged Out Successfully.")
            return redirect("/login/sellers")
        else:
            ("some error occured")
    elif mainstr=='admins':
        if 'admin' in session:
            session.pop('admin')
            flash("Your Admin Account Logged Out Successfully.")
            return redirect("/login/customers")
        
   
    return redirect("/")

@app.route("/account/edit/<string:mainstr>/<string:srNo>", methods=["GET",'POST'])
def accountEdit(mainstr,srNo):
    if mainstr=='customers':
        if  'user' in session:
            if request.method=="POST":
                fullName=request.form.get("fullName")
                dob=request.form.get("dob")
                phone=request.form.get("phoneNo")
                email=request.form.get("email")
                password=request.form.get("password")
                repassword=request.form.get("repassword")
                address=request.form.get("Address")
                address2=request.form.get("Address2")
                city=request.form.get("city")
                state=request.form.get("state")
                zip=request.form.get("zip")
                if srNo=='0':
                    cred=Customers(custName= fullName,custMobile=phone,custDoB=dob,custEmail=email,custAddress=address,custAddress2=address2,custCity=city,custState=state,custZip=zip,custdate=datetime.now())
                    try:
                        db.session.add(cred)
                        db.session.commit()
                   
                    except IntegrityError:
                        flash("User "+ str(phone) +" already Exists")
                    
                else:
                    data=Customers.query.filter_by(custMobile=session['user']).first()
                    data.custName=fullName
                    data.custDoB=dob
                    data.custMobile=phone
                    data.custEmail=email
                    data.custAddress=address
                    data.custAddress2=address2
                    data.custCity=city
                    data.custState= state
                    data.custZip=zip
                    db.session.commit()
                    return redirect("/account/customers")
        if srNo=="0":
            data={"srNo":"0"}    
        else:
            data=Customers.query.filter_by(custMobile=srNo).first()
    if mainstr=='sellers':
        if  'seller' in session:
            if request.method=="POST":
                fullName=request.form.get("fullName")
                dob=request.form.get("dob")
                phone=request.form.get("phoneNo")
                email=request.form.get("email")
                password=request.form.get("password")
                address=request.form.get("Address")
                address2=request.form.get("Address2")
                city=request.form.get("city")
                state=request.form.get("state")
                zip=request.form.get("zip")
                LicenseId=request.form.get("LicenseId")
                Website=request.form.get("Website")
                Company=request.form.get("Company")
                
                if srNo=='0':
                    cred=Sellers(Name= fullName,Mobile=phone,DoB=dob,Email=email,Company=Company,LicenseId=LicenseId,Website=Website,Address=address,Address2=address2,City=city,State=state,Zip=zip,date=datetime.now())
                    try:
                        db.session.add(cred)
                        db.session.commit()
                      
                    except IntegrityError:
                        flash("Seller "+ str(phone) +" already Exists")
                    
                else:
                    data=Sellers.query.filter_by(Mobile=srNo).first()
                    data.Name=fullName
                    data.DoB=dob
                    data.Mobile=phone
                    data.Email=email
                    data.Address=address
                    data.Address2=address2
                    data.City=city
                    data.State= state
                    data.Zip=zip
                    data.Passwd=password
                    data.Company=Company
                    data.Website=Website
                    data.LicenseId=LicenseId
                    db.session.commit()
                    flash("Changes saved successfully...")
                    return redirect("/account/sellers")
        if srNo=="0":
            data={"srNo":"0"}    
        else:
            data=Sellers.query.filter_by(Mobile=srNo).first()
    return render_template("accountEditor.html",data=data,srNo=srNo,pageDisplay=mainstr)

@app.route("/cart/quantity/edit/<string:prodId>/<string:plusminus>", methods=["GET",'POST'])
def cartQuantity(prodId,plusminus):
    
    if  'user' in session:
        cust=Customers.query.filter_by(custMobile=session['user']).first()
        data=Carts.query.filter_by(productId=prodId,customerId=cust.custId).first()
        if plusminus=='plus':
            data.quantity=data.quantity+1
        else:
            data.quantity=data.quantity-1
        if data.quantity<1:
            data.quantity=1
        db.session.commit()
        return redirect("/cart")
    else:
        return redirect("/")

@app.route("/cart")
def cart():
    if 'user' in session:
        prod=[]
        data=Customers.query.filter_by(custMobile=session['user']).first()
        cart=Carts.query.filter_by(customerId=data.custId).all()
        for index in cart:
            prod+=Products.query.filter_by(prodId=index.productId).all() 
    else:
        return redirect("login/customers")
    return render_template("cart.html",cart=cart,prod=prod)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.context_processor
def inject_user():
    User=False
    Seller=False
    data=None
    customize=None
    if "user" in session:
        data=Customers.query.filter_by(custMobile=session['user']).first()
        customize=Customize.query.filter_by(userId=data.custId).first()
        User=True
        Seller=False
    elif 'seller' in session:
        data=Sellers.query.filter_by(Mobile=session['seller']).first()
        Seller=True
        User=False
    else:
        User=False
        Seller=False
    return dict(userAvail=User,data=data,sellerAvail=Seller,params=params,navs=navs,subnavs=subnavs,customize=customize)   

if __name__=='__main__':
    app.run(debug=True,port=8000)