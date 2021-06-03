from django.core import paginator
from django.forms.fields import NullBooleanField
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,AuthenticationForm,CustomerProfileForm,LoginForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app.forms import SearchForm
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, message
import random
from .models import UserOTP,Product,ProductComment
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from app.templatetags import extras
from django.contrib.auth import authenticate,login
from django.urls import reverse
import json
import requests

#from django.core.paginator import Paginator

# html email required stuff starts
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# html email required stuff ends

#def home(request):
 #return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')

        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles ,'totalitem':totalitem})

#def product_detail(request):
 #return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        #views Carousel starts
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        #views Carousel ends
        #product comment filter start
        photo=NullBooleanField
        if request.user.is_authenticated:
            user=request.user
            photo=Customer.objects.filter(user=user).order_by('profile_pic').last()

        comments=ProductComment.objects.filter(product=product,parent=None)
        #product comment filter end
        #product Replies start
        replies=ProductComment.objects.filter(product=product).exclude(parent=None)
        replyDict={}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno]=[reply]
            else:
                replyDict[reply.parent.sno].append(reply)  
        #print(replyDict)          
        #product Replies end
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))    
        return render(request,'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart ,'totalitem':totalitem,'comments':comments,'replyDict':replyDict,'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles ,'totalitem':totalitem,'photo':photo})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        user=request.user
        cart=Cart.objects.filter(user=user)

        amount=0.0
        total_amount=0.0
        shipping_amount=70.0
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':total_amount, 'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'totalitem':totalitem }) 

@login_required
def plus_cart(request):
    if request.method == 'GET':
        user=request.user
        prod_id =request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:

            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount+shipping_amount
                
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        user=request.user
        prod_id =request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:

            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount+shipping_amount
                
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        user=request.user
        prod_id =request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        #c.quantity-=1
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:

            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
           # totalamount = amount+shipping_amount
                
        data={
            #'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)


'''@login_required
def Like_Product(request,pk):
    print(pk)
    product=get_object_or_404(Product,id=request.POST.get('prod_id'))
    product.likes.add(request.user)
    return HttpResponseRedirect(reverse('product-detail',args=[str(pk)])) '''
  




@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')


'''def profile(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/profile.html',{'totalitem':totalitem})
'''

@login_required
def address(request):
    user=request.user
    photo=Customer.objects.filter(user=user).order_by('profile_pic').last()
    #add=Customer.objects.filter(user=request.user)
    cust_add=[p for p in Customer.objects.all() if p.user == user]
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html',{'add':cust_add,'active':'btn-primary','totalitem':totalitem,'photo':photo})

@login_required
def delete_address(request):
    user=request.user
    custid=request.GET.get('adid')
    print(custid)
    #customer =Customer.objects.get(id=custid)
    op=Customer.objects.get(id=custid)
    op.delete()
    messages.success(request,f'Your address has been Successfully deleted {user}')
    return redirect("address")     



@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer =Customer.objects.get(id=custid)
    cart =Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")  

@login_required
def orders(request):
    if request.user.is_authenticated:
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')

        usr=request.user  
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=usr))
    
        #op=OrderPlaced.objects.filter(user=request.user)
        op_product=[p for p in OrderPlaced.objects.all() if p.user == usr]
        #print(op_product)
    #print(item_quantity)
        if op_product:
            quantity=len(op_product)
            #for p in op_product:
                #quantity=p.quantity+1
            if quantity :               
                html_content=render_to_string('app/email_template.html',{'title':'order_detail_user', 'user':usr,'quantity':quantity})
                text_content=strip_tags(html_content)
                email=EmailMultiAlternatives(

                "Welcome to ShopHUB.COM   -Your Orders Details",
                text_content,
                settings.EMAIL_HOST_USER,
                [usr.email],
                )
                email.attach_alternative(html_content,"text/html")
                email.send()
            return render(request, 'app/orders.html' ,{'order_placed':op_product,'totalitem':totalitem})
        else:
            return render(request,'app/emptyorder.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'totalitem':totalitem })

@login_required
def orderdetails(request):
    if request.user.is_authenticated:
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')

        usr=request.user  
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=usr))
        op=OrderPlaced.objects.filter(user=request.user)
        if op:
            return render(request, 'app/orders.html' ,{'order_placed':op,'totalitem':totalitem})
        else:
            return render(request,'app/emptyorder.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'totalitem':totalitem })

@login_required
def orderDelete(request):
    user=request.user
    custid=request.GET.get('prodid')
    #customer =Customer.objects.get(id=custid)
    op=OrderPlaced.objects.get(id=custid)
    op.delete()
    messages.success(request,f'Your product has been Successfully deleted {user}')
    mess=f"Hello {user},\nYour product has been Successfuly canceled, \nto buy more products GoTo ShopHUB.COM ,\n for any suggestion send ShopHUB@wildmart.com"       
    send_mail(
        "Welcome to ShopHUB.COM  -verify Your cancelation Email <@ noreply.gmail.com>",
         mess,
         settings.EMAIL_HOST_USER,
         [user.email],
         fail_silently=False
        )
    return redirect("orderdetails")    


#def change_password(request):
 #return render(request, 'app/changepassword.html')

def mobile(request,data=None):

    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product=Product.objects.all()
    if data==None:
        mobiles=Product.objects.filter(category='M')

    elif data=='Redmi' or data=='Samsung':
        mobiles=Product.objects.filter(category='M',brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)

    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000) 

        

    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem,'product':product})

#def login(request):
 #return render(request, 'app/login.html')

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self,request):
        
        get_otp=request.POST.get('otp')
        if get_otp:
            get_usr=request.POST.get('usr')
            usr=User.objects.get(username=get_usr)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                messages.success(request, f'Congratulations !! Account is created for {usr}')
                return redirect('login')
            else:
                messages.warning(request, f'You entered a wrong otp {usr} kindly Entered a valid OTP')
                return render(request,'app/customerregistration.html',{'otp':True, 'usr':usr})   


        form=CustomerRegistrationForm(request.POST)    
        if form.is_valid():    
            form.save() 
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            #name=form.cleaned_data.get('name').split('')

            usr=User.objects.get(username=username)
            usr.email=email
            usr.is_active=False
            #usr.first_name=name[0]
            #usr.last_name=name[1]
            usr_otp=random.randint(1000,9999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            #usr.otp=usr_otp
            usr.save()
            mess=f"Hello {usr},\nYour OTP is @{usr_otp},\n Do not Share this OTP Thanks!!!"
            
            send_mail(
                "Welcome to ShopHUB.COM  -verify Your Email",
                 mess,
                 settings.EMAIL_HOST_USER,
                 [usr.email],
                 fail_silently=False
            )
            return render(request,'app/customerregistration.html',{'otp':True, 'usr':usr})

        return render(request,'app/customerregistration.html',{'form':form})        



def resendOTP(request):
    if request.method== "GET":
        get_usr=request.GET['usr']
        print(get_usr)
        if User.objects.filter(username= get_usr).exists() and not User.objects.get(username=get_usr).is_active:
            usr=User.objects.get(username=get_usr)
            usr_otp=random.randint(1000,9999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess=f"Hello {usr},\nYour resend OTP is {usr_otp},\n Do not Share this OTP Thanks!!!"
            
            send_mail(
                "Welcome to ShopHUBt.COM  -verify Your Email",
                 mess,
                 settings.EMAIL_HOST_USER,
                 [usr.email],
                 fail_silently=False
            )
            return HttpResponse('send')

    return HttpResponse("can't send")  


#user=User.objects.create_user(username=form.username,email=form.email)
#email=request.POST.get('email')
#if User.objects.filter(email = email).first():
#user.is_active=False
#email_subject='Active your account'
            #email_body=''
            #email = EmailMessage(
                #email_subject, 
                #email_body,
                #'noreply@wildmart.com',
                #[email],
            #)




@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    #order_user=OrderPlaced.objects.filter(user=user)
    #item_quantity=OrderPlaced.objects.filter(Q(product=order_user.quantity) & Q(user=request.user)).exists()
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    cart_product=[p for p in Cart.objects.all() if p.user == user]

    #c= Cart.objects.filter(user=user)
    #item_quantity=c.quantity
    if cart_product: 
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
    total_amount=amount+shipping_amount    
    return render(request, 'app/checkout.html', {'add':add,'totalamount':total_amount,'cart_items':cart_items,'amount':amount, 'totalitem':totalitem,'active':'btn-primary'})

  




@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        usr=request.user
        photo=Customer.objects.filter(user=usr).order_by('profile_pic').last()
        form=CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem,'photo':photo})

    def post(self,request):
        usr=request.user
        #cust_add=[p for p in Customer.objects.all() if p.user == usr]
        photo=Customer.objects.order_by('profile_pic').last()
        form=CustomerProfileForm(request.POST,request.FILES)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            profile_pic=form.cleaned_data['profile_pic']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode,profile_pic=profile_pic)
            reg.save()
            form=CustomerProfileForm()

            messages.success(request,f'Congratulations !! profile update Successfully {usr} click adress button ')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem,'photo':photo})






#def searchItem(request):
    #form=SearchForm()
    #res=render(request,'app/base.html',{'form':form})
    #return res



def search(request):
    query=request.GET['query']


    if len(query)>78:
        products=Product.objects.none()
    else:
        productsTitle=Product.objects.filter(title__icontains=query)
        productsContent=Product.objects.filter(description__icontains=query)
        products=productsTitle.union(productsContent) 
    
    #if products.count()== 0:
        #messages.error(request,"please fill the form correctly")
    
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/search.html',{'totalitem':totalitem,'query':query,'products':products})

def autocomplete(request):
    if 'term' in request.GET:
        qt=Product.objects.filter(title__icontains=request.GET.get('term'))
        qd=Product.objects.filter(description__icontains=request.GET.get('term'))
        qs=qt.union(qd)
        titles=list()
        for product in qs:
            titles.append(product.title)
        return JsonResponse(titles,safe=False)

'''def search(request):
  query = request.GET.get('query')
  if query is None:
      return redirect('home')
  else:
      item = Product.objects.all().order_by('query')
      if item:
          itemTitle = item.filter(
                  Q(title__icontains=query)  
              ).distinct()
          itemContent = item.filter(
                  Q(title__icontains=query)  
              ).distinct()
          item=itemTitle.union(itemContent)    

 # if item.count() == 0:
      #messages.error(request, "No search results found")

  paginator = Paginator(item, 1)
  page = request.GET.get('page')
  try:
      queryset = paginator.get_page(page)
  except PageNotAnInteger:
      queryset = paginator.get_page(1)
  except EmptyPage:
      queryset = paginator.get_page(paginator.num_pages)

  context = {
      'search': item,
      'pagination': queryset,
      'query': query,
  }
  return render(request,'app/search.html', context)'''

   
            
@login_required
def productComment(request):
    #views Carousel starts
    topwears=Product.objects.filter(category='TW')
    bottomwears=Product.objects.filter(category='BW')
    mobiles=Product.objects.filter(category='M')

    #views Carousel ends
    prod_id=request.POST.get("prod_id")
    product=Product.objects.get(pk=prod_id)
    comments=ProductComment.objects.filter(product=product,parent=None)


    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
    item_already_in_cart=False
    if request.user.is_authenticated:
        item_already_in_cart=Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).exists()        

    if request.method=="POST":
        comment=request.POST.get("comment")
        rate=request.POST.get("rating")
        user=request.user
        prod_id=request.POST.get("prod_id")
        product=Product.objects.get(pk=prod_id)
        parentSno=request.POST.get("parentSno")
        #print(parentSno)
        photo=Customer.objects.filter(user=user).order_by('profile_pic').last()
        #parent=  
        if parentSno == " ":
            if rate:
                comment=ProductComment(comment=comment,rate=rate,user=user,product=product)
            else:
                comment=ProductComment(comment=comment,user=user,product=product)  
            comment.save()
            messages.success(request,"Your comments has successfilly added")
        else:
            parent= ProductComment.objects.get(pk=parentSno)
            print(parent)
            comment=ProductComment(comment=comment,user=user,product=product, parent=parent)   
            comment.save()
            messages.success(request,"Your reply has successfilly added")

        #product Replies start
        replies=ProductComment.objects.filter(product=product).exclude(parent=None)
        replyDict={}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno]=[reply]
            else:
                replyDict[reply.parent.sno].append(reply)  
        #print(replyDict)          
        #product Replies end 

    return render(request,'app/productdetail.html',{'product':product,'totalitem':totalitem,'item_already_in_cart':item_already_in_cart ,'comments':comments,'replyDict':replyDict,'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles ,'totalitem':totalitem,'photo':photo})

    #return HttpResponseRedirect(request.path_info)    



def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_usr=request.POST.get('usr')
            usr=User.objects.get(username=get_usr)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                login(request,usr)
                return redirect('home')
            else:
                messages.warning(request, f'You entered a wrong otp {usr} kindly Entered a valid OTP')
                return render(request,'app/login.html',{'otp':True, 'usr':usr}) 
        

        if request.method == 'POST':
            usrname=request.POST['username']
            passwd=request.POST['password']
            user=authenticate(request,username=usrname,password=passwd)

            if user is not None:
                # Google recaptcha validation stuff starts
                clientkey=request.POST['g-recaptcha-response']
                secretkey='your secret key'
                data={
                    'secret':secretkey,
                    'response':clientkey
                }
                r=requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                response=json.loads(r.text)
                verify=response['success']
                if verify:
                    login(request,user)
                    return redirect('home')
                else:
                    messages.warning(request, f'please enter a valid username ,password also validate recaptcha to unauthenticate user   !!')
                    return redirect('login') 

                # Google recaptcha validation stuff ends


            elif not User.objects.filter(username=usrname).exists():
                messages.warning(request, f'please enter a valid username and password  {usrname} both are case Sensitive !!')
                return redirect('login')
            elif not User.objects.get(username=usrname).is_active:
                usr=User.objects.get(username=usrname)
                usr_otp=random.randint(1000,9999)
                UserOTP.objects.create(user=usr, otp=usr_otp)
                usr.save()
                mess=f"Hello {usr},\nYour OTP is {usr_otp},\n Do not Share this OTP Thanks!!!"
            
                send_mail(
                "Welcome to ShopHUB.COM  -verify Your Email",
                 mess,
                 settings.EMAIL_HOST_USER,
                 [usr.email],
                 fail_silently=False
                )
                return render(request,'app/login.html',{'otp':True, 'usr':usr})
            else:
                messages.warning(request, f'please enter a valid username and password  {usrname} both are case Sensitive !!')
                return redirect(login)
    form=LoginForm()
    return render(request, 'app/login.html',{'form':form})





'''  name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            #profile_pic=form.cleaned_data['profile_pic']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()

                clientkey=request.POST['g-recaptcha-response']
                secretkey='6LfDLvIaAAAAAL1htimTwxoCND69lGNKuVYDpnZ5'
                capthchaData={
                'secret':secretkey,
                'response':clientkey
                }
                r=request.post('https://www.google.com/recaptcha/api/siteverify', data=capthchaData)
                response=json.loads(r.text)
                verify=response['success']
                print('your success is',verify) 

'''


