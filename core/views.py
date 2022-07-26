from django.utils import timezone
from django.conf import settings
from django.shortcuts import render , redirect , get_object_or_404
from requests import request
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Item , Order , OrderItem , BillingAddress
from django.views.generic import *
from .form import CheckoutForm
from allauth.account.views import LoginView
import stripe
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY
class HomeView(LoginRequiredMixin,ListView):
    model = Item
    paginate_by =  1
    template_name = 'home_page.html'


class ItemDetailView(LoginRequiredMixin,DeleteView):
    model = Item
    template_name = 'product_page.html'


class order_summary(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:     
            order = Order.objects.get(user = self.request.user , ordered=False )
            context = {
                'object':order
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"There isn't any product")
            return redirect("/")
        

@login_required
def add_to_cart(request , slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item)
    order_qs = Order.objects.filter(user=request.user,ordered = False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user ,ordered_date = ordered_date)
        order.items.add(order_item)
    return redirect('core:order_summary')

@login_required
def remove_from_cart(request , slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #! check if order item is in order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                  item = item,
                user = request.user,              
                ordered = False
            )[0]
            order.items.remove(order_item)
            return (order)
        else:
            #!  the user doesnt have this item in his/her order
            return redirect('core:order_summary')
            
    else:
            #! user doesnt have an order
            return redirect('core:order_summary' )
            


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                                item=item,
                                user=request.user,
                                ordered=False
                                )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.filter(item__slug=item.slug).delete()

        else:
            return redirect("core:order_summary")
    else:
        return redirect("core:order_summary")

    return redirect("core:order_summary")
    


# @login_required
class CheckoutView(View):
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        context = {
            'form':form
        }
        return render(self.request,'checkout.html',context)
   
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST , None)
        try:
            order = Order.objects.get(user = self.request.user , ordered=False)
            if form.is_valid():
                street = form.cleaned_data.get('street')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                # payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('core:checkout')
            messages.warning(self.request,"Your checkout failed")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request,"You dont have any order")
            return redirect('core:checkout')

class Payment(View):
    def get(self,*args,**kwargs):
        return render(self.request,"payment.html")


   
          