import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Product, Order, Payment

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def product_detail(request, product_id):
    """Display product details and checkout options"""
    product = get_object_or_404(Product, id=product_id, isActive=True)
    
    context = {
        'product': product,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'store/product_detail.html', context)

@login_required
def create_checkout_session(request, product_id):
    """Create a Stripe checkout session for the specified product"""
    product = get_object_or_404(Product, id=product_id, isActive=True)
    
    # Skip payment process if the product is free
    if product.price == 0:
        # Create order and mark as completed
        order = Order.objects.create(
            user=request.user,
            product=product,
            status='completed'
        )
        return redirect('store:order_success', order_id=order.id)
    
    # For paid products, create Stripe checkout session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                        'description': product.description,
                    },
                    'unit_amount': product.get_stripe_price(),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('store:payment_success')
            ) + f'?session_id={{CHECKOUT_SESSION_ID}}&product_id={product_id}',
            cancel_url=request.build_absolute_uri(reverse('store:payment_cancel')),
            metadata={
                'product_id': product.id,
                'user_id': request.user.id,
            }
        )
        
        # Create a pending order
        order = Order.objects.create(
            user=request.user,
            product=product,
            stripe_payment_intent_id=checkout_session.payment_intent,
            status='pending'
        )
        
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def payment_success(request):
    """Handle successful payment redirect"""
    session_id = request.GET.get('session_id')
    product_id = request.GET.get('product_id')
    
    if not session_id:
        return redirect('store:store', 1)
    
    try:
        # Retrieve the session
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Get the payment intent
        payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
        
        # Find the order by payment intent
        order = Order.objects.get(stripe_payment_intent_id=session.payment_intent)
        
        # Update order status
        if payment_intent.status == 'succeeded':
            order.status = 'completed'
            order.save()
            
            # Create payment record
            Payment.objects.create(
                order=order,
                stripe_charge_id=payment_intent.latest_charge,
                amount=payment_intent.amount,
            )
            
            context = {
                'order': order,
                'product': order.product,
            }
            return render(request, 'store/payment_success.html', context)
        else:
            order.status = 'failed'
            order.save()
            return redirect('store:payment_failed')
            
    except Exception as e:
        print(str(e))
        return redirect('store:payment_failed')

@login_required
def payment_cancel(request):
    """Handle canceled payment"""
    return render(request, 'store/payment_cancel.html')

@login_required
def payment_failed(request):
    """Handle failed payment"""
    return render(request, 'store/payment_failed.html')

@login_required
def order_success(request, order_id):
    """Display success page for free products"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'product': order.product,
    }
    return render(request, 'store/payment_success.html', context)

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
        
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Retrieve the payment intent
        payment_intent_id = session.get('payment_intent')
        
        if payment_intent_id:
            try:
                # Find and update the order
                order = Order.objects.get(stripe_payment_intent_id=payment_intent_id)
                order.status = 'completed'
                order.save()
                
                # Create payment record if it doesn't exist
                if not hasattr(order, 'payment'):
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                    Payment.objects.create(
                        order=order,
                        stripe_charge_id=payment_intent.latest_charge,
                        amount=payment_intent.amount,
                    )
            except Order.DoesNotExist:
                print(f"Order with payment intent {payment_intent_id} not found")
    
    return HttpResponse(status=200)

@login_required
def my_purchases(request):
    """Display user's purchased products"""
    completed_orders = Order.objects.filter(
        user=request.user,
        status='completed'
    ).order_by('-created_at')
    
    context = {
        'orders': completed_orders
    }
    return render(request, 'store/my_purchases.html', context)