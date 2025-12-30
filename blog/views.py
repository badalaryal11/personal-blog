from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Project, BlogPost

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            try:
                send_mail(
                    subject=f'Portfolio Contact: {name}',
                    message=f'From: {name} <{email}>\n\n{message}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['badal.aryal@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, 'An error occurred while sending your message. Please try again later.')
        else:
            messages.error(request, 'Please fill in all fields.')
            
        return redirect('home')

    projects = Project.objects.all().order_by('-created_at')
    posts = BlogPost.objects.all().order_by('-date_posted')
    return render(request, 'blog/home.html', {'projects': projects, 'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

from .forms import SubscriptionForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            
            # Send confirmation email
            try:
                send_mail(
                    subject='Welcome to my Newsletter!',
                    message='Thank you for subscribing to my newsletter. I will keep you updated with my latest blog posts and projects.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[subscriber.email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log error but don't fail the response
                print(f"Error sending email: {e}")

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
            else:
                messages.success(request, 'Thank you for subscribing!', extra_tags='subscription')
                return redirect('/#newsletter')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Invalid email or already subscribed.'})
            else:
                messages.error(request, 'Invalid email or already subscribed.', extra_tags='subscription')
                return redirect('/#newsletter')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    else:
        return redirect('/')

# --- Buy Me a Coffee (Esewa Integration) ---
from .forms import DonationForm
from .models import Donation
from .models import Donation
import uuid

def buy_coffee_view(request):
    form = DonationForm()
    return render(request, 'blog/buy_coffee.html', {'form': form})

def initiate_payment(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            amount = form.cleaned_data['amount']
            transaction_id = str(uuid.uuid4())
            
            # Create Pending Donation
            Donation.objects.create(
                name=name,
                amount=amount,
                transaction_id=transaction_id,
                status="Pending"
            )
            
            # Esewa Config (Test/Production)
            # For Test Environment
            esewa_url = "https://rc-epay.esewa.com.np/api/epay/main/v2/form" 
            merchant_id = "EPAYTEST" 
            success_url = request.build_absolute_uri('/buy-coffee/verify/')
            failure_url = request.build_absolute_uri('/buy-coffee/fail/')
            
            # Signature Calculation (Required for v2)
            # Message = "total_amount,transaction_uuid,product_code"
            # Signature = HMAC-SHA256(Message, SecretKey)
            # Test Secret Key: 8gBm/:&EnhH.1/q
            
            import hmac
            import hashlib
            import base64
            
            secret_key = "8gBm/:&EnhH.1/q"
            data_to_sign = f"total_amount={amount},transaction_uuid={transaction_id},product_code={merchant_id}"
            
            # Calculate signature
            # Note: For Esewa v2 form submission, the signature logic is specific. 
            # Actually, the form submission documentation recommends using client-side or server-side simple binding.
            # But let's check if we strictly need signature for Form submission in Test mode.
            # Yes, v2 requires it.
            
            secret_bytes = secret_key.encode('utf-8')
            data_bytes = data_to_sign.encode('utf-8')
            
            signature = base64.b64encode(hmac.new(secret_bytes, data_bytes, hashlib.sha256).digest()).decode('utf-8')

            context = {
                'esewa_url': esewa_url,
                'amount': amount,
                'tax_amount': 0,
                'total_amount': amount,
                'transaction_uuid': transaction_id,
                'product_code': merchant_id,
                'product_service_charge': 0,
                'product_delivery_charge': 0,
                'success_url': success_url,
                'failure_url': failure_url,
                'signed_field_names': 'total_amount,transaction_uuid,product_code',
                'signature': signature,
            }
            
            return render(request, 'blog/esewa_redirect.html', context)
        else:
             messages.error(request, "Invalid amount.")
             return redirect('buy_coffee')
    return redirect('buy_coffee')

def verify_payment(request):
    # Esewa v2 redirects with encoded data
    # ?data=... (Base64 encoded JSON)
    
    encoded_data = request.GET.get('data')
    
    if not encoded_data:
        # Fallback or error
        return render(request, 'blog/payment_failed.html')
        
    import base64
    import json
    
    try:
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_string = decoded_bytes.decode('utf-8')
        data = json.loads(decoded_string)
        
        # Data structure: { "transaction_code": "...", "status": "COMPLETE", "total_amount": ..., "transaction_uuid": "..." }
        
        status = data.get('status')
        transaction_uuid = data.get('transaction_uuid')
        ref_id = data.get('transaction_code')
        amount = data.get('total_amount')
        
        if status == 'COMPLETE':
            donation = get_object_or_404(Donation, transaction_id=transaction_uuid)
            
            if donation.status != 'Completed':
                donation.status = 'Completed'
                donation.esewa_ref_id = ref_id
                donation.save()
                
            return render(request, 'blog/payment_success.html', {'donation': donation})
        else:
             return render(request, 'blog/payment_failed.html')
             
    except Exception as e:
        print(f"Payment verification failed: {e}")
        return render(request, 'blog/payment_failed.html')

def payment_failed(request):
    return render(request, 'blog/payment_failed.html')
