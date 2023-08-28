from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from . models import Customer, Product,  Cart
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.http import HttpResponseBadRequest



from django.shortcuts import render

# Create your views here.
def home (request):
    return render (request,"app/home.html")

def aboutus (request):
    return render (request,"app/aboutus.html")

def lounges (request):
    return render (request,"app/lounges.html")

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
class CatergoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title')
        return render(request,"app/category.html",locals())    
    

class ProductDetail(View):
 def get(self,request,pk):
    product = Product.objects.get(pk=pk)
    return render(request,"app/productdetail.html",locals()) 
 

class CustomerRegistrationView(View):
     def get(self,request):
         form=CustomerRegistrationForm()
         return render(request,'app/customerregistration.html',locals())
     def post(self,request):
         form = CustomerRegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             messages.success(request,"Congratulations! User Registration successful")
         else :
             messages.warning(request,"Opps! User Registration failed")
         return render(request,'app/customerregistration.html',locals())   
     
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',locals())
    def post(self,request):

        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data[ 'city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data[ 'state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality,mobile=mobile, city=city, state=state,zipcode=zipcode) 
            reg.save()
            messages.success(request,"Congrats!!! Profile Saved Successfully")
        else:
            messages.warning((request,"Opps!!! Invalid Data"))

        return render (request, 'app/profile.html',locals())
    


def address(request):
    add=Customer.objects.filter(user=request.user)
    return render (request, 'app/address.html',locals())


class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render (request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)  
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile updated successfully.")
        else:
            messages.warning(request, "Invalid Input Data")

        return redirect("address")
    
#def add_to_cart(request):
    #user=request.user
    #product_id=request.GET.get('prod_id')
    #product= Product.objects.get(id=product_id)
    #Cart(user=user,product=product).save()
   # return redirect("/cart")

def add_to_cart(request):
    user = request.user

    # Retrieve product_id from GET parameters
    product_id_str = request.GET.get('prod_id')

    # Check if product_id is valid
    if not product_id_str:
        return HttpResponseBadRequest("Missing product_id parameter")

    try:
        product_id = int(product_id_str)
        product = Product.objects.get(id=product_id)
    except (ValueError, Product.DoesNotExist):
        return HttpResponseBadRequest("Invalid product_id")

    Cart(user=user, product=product).save()
    return redirect("/cart")



def show_cart(request):
    user=request.user
    cart= Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', locals())





        
