from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Service, Testimonial, AppointmentRequest, Contact, BlogPost, Subscriber
from .forms import ContactForm, AppointmentRequestForm, SubscriberForm

def home(request):
    services = Service.objects.filter(is_active=True).order_by('order')[:4]  # Get first 4 active services
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:3]
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3]
    
    # For newsletter subscription
    if request.method == 'POST':
        subscriber_form = SubscriberForm(request.POST)
        if subscriber_form.is_valid():
            email = subscriber_form.cleaned_data['email']
            if not Subscriber.objects.filter(email=email).exists():
                subscriber_form.save()
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.info(request, "You are already subscribed to our newsletter.")
            return redirect('public:home')
    else:
        subscriber_form = SubscriberForm()
    
    context = {
        'services': services,
        'testimonials': testimonials,
        'recent_posts': recent_posts,
        'subscriber_form': subscriber_form,
    }
    return render(request, 'public/home.html', context)

def services(request):
    services_list = Service.objects.filter(is_active=True).order_by('order')
    
    context = {
        'services': services_list,
    }
    return render(request, 'public/services.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent. We'll get back to you soon!")
            return redirect('public:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'public/contact.html', context)

def testimonials(request):
    testimonials_list = Testimonial.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'testimonials': testimonials_list,
    }
    return render(request, 'public/testimonials.html', context)

def appointment_request(request):
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your appointment request has been submitted. We will contact you shortly to confirm.")
            return redirect('public:home')
    else:
        form = AppointmentRequestForm()
    
    context = {
        'form': form,
    }
    return render(request, 'public/appointment_request.html', context)

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True, published_date__lte=timezone.now()).order_by('-published_date')
    
    context = {
        'posts': posts,
    }
    return render(request, 'public/blog_list.html', context)

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, is_published=True, published_date__lte=timezone.now())
    # Get related posts
    related_posts = BlogPost.objects.filter(is_published=True, published_date__lte=timezone.now()).exclude(pk=pk).order_by('-published_date')[:3]
    
    # For newsletter subscription
    if request.method == 'POST':
        subscriber_form = SubscriberForm(request.POST)
        if subscriber_form.is_valid():
            email = subscriber_form.cleaned_data['email']
            if not Subscriber.objects.filter(email=email).exists():
                subscriber_form.save()
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.info(request, "You are already subscribed to our newsletter.")
            return redirect('public:blog_detail', pk=pk)
    else:
        subscriber_form = SubscriberForm()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'subscriber_form': subscriber_form,
    }
    return render(request, 'public/blog_detail.html', context)
