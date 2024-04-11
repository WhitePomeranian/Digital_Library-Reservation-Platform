from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils import timezone
from .forms import SignUpForm, SignInForm
from .models import UserProfile, Book, ReservedBook


#首頁
def homepage(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')

    search_type = request.GET.get('searchtype') 
    search_query = request.GET.get('search')

    if search_type and search_query:
        if search_type.lower() == 'booktitle':
            search_results = Book.objects.filter(bname__icontains=search_query)
            cache.set('search_results', search_results, 6000)
        elif search_type.lower() == 'author':
            search_results = Book.objects.filter(author__icontains=search_query)
            cache.set('search_results', search_results, 6000)
        elif search_type == 'ISBN':
            search_results = Book.objects.filter(ISBN__icontains=search_query)
            cache.set('search_results', search_results, 6000)
        else:
            search_results = []
    else:
        search_results = cache.get('search_results')
        if search_results is None:
            search_results = Book.objects.all()


    user_profile_id = request.session.get('user_profile_id')
    try:
        user_profile = UserProfile.objects.get(id=user_profile_id)
    except UserProfile.DoesNotExist:
        user_profile = None

    search_results = search_results or []
    paginator = Paginator(search_results, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user_profile': user_profile,
        'results': page_obj,
    }

    return render(request, 'homepage.html', context)

#預約清單
def appointment(request):

    if not request.user.is_authenticated:
        return redirect('sign_in')
    

    user_profile_id = request.session.get('user_profile_id')
    try:
        user_profile = UserProfile.objects.get(id=user_profile_id)
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        print("this is post")
        user = request.POST.get('user') 
        book = request.POST.get('book')
        first_matches = ReservedBook.objects.filter(user__exact=user_profile.user)
        print("1 match: ",first_matches)
        
        second_matches = []
        for rb in first_matches:
            str1=str(rb.book)
            str2=book
            print("str1: ",str1,".")
            print("str2: ",str2,".")
            if str1.lower() == str2.lower():
                second_matches.append(rb)

        print("2 match: ",second_matches)
        for rb in second_matches:
            # print("user_profile1",user_profile.borrowing_quantity)
            user_profile.borrowing_quantity -= 1
            # print("user_profile2",user_profile.borrowing_quantity)
            user_profile.save()
            string = book
            result = string.split(" ")[0]
            # print("result: ",result)
            tb = Book.objects.get(bname = result)
            tb.status = 'available'
            tb.save()
            rb.delete()

    

    print("id: ",user_profile.user)
    search_results_reserved = ReservedBook.objects.filter(user__exact=user_profile.user)
    cache.set('search_results_reserved', search_results_reserved, 600)
    search_results_reserved = cache.get('search_results_reserved')
    search_results_reserved = search_results_reserved or []
    paginator = Paginator(search_results_reserved, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print("this: ",search_results_reserved)

    context = {
        'user_profile': user_profile,
        'results': page_obj,
    }


    return render(request, 'appointment.html',context)


#書籍詳細資訊
def bookdetails(request, id):

    if not request.user.is_authenticated:
        return redirect('sign_in')

    bookdetails = Book.objects.get(id=id)
    if request.method == 'POST' and 'reservation' in request.POST:
        if bookdetails.status == 'available':
            user_profile = request.user.userprofile
            ReservedBook.objects.create(user=request.user, book=bookdetails, reservation_date=timezone.now())
            user_profile.borrowing_quantity += 1
            user_profile.save()
            bookdetails.status = 'unavailable'
            bookdetails.save()
            print('1oth')
            return redirect('bookdetails', id=id)
    else:
        print('noth')

    user_profile_id = request.session.get('user_profile_id')
    try:
        user_profile = UserProfile.objects.get(id=user_profile_id)
    except:
        context = {
            'bookdetails': bookdetails,
        }
        return render(request, 'bookdetails.html', context)

    context = {
        'user_profile': user_profile,
        'bookdetails': bookdetails,
    }

    return render(request, 'bookdetails.html', context)

#註冊
def sign_up(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, gender=form.cleaned_data['gender'], birthday=form.cleaned_data['birthday'])
            success_sign_up = "註冊成功!"
            context = {
                'success_sign_up': success_sign_up
            }
            return render(request, 'sign_up.html', context)
        else:
            failure_sign_up = "註冊失敗!"
            context = {
                'form': form,
                'failure_sign_up': failure_sign_up
            }
            return render(request, 'sign_up.html', context)

    context = {
        'form': form
    }

    return render(request, 'sign_up.html', context)

#登入
def sign_in(request):
    form = SignInForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                user_profile = UserProfile.objects.get(user=user)
                request.session['user_profile_id'] = user_profile.id
                cache.delete('search_results')
                
                return redirect('/homepage')
            except UserProfile.DoesNotExist:
                return redirect('/homepage')
        else:
            failure_sign_in = "登入失敗! 無效的帳號或密碼"
            context = {
                'form': form,
                'user': request.user,
                'failure_sign_in': failure_sign_in
            }
            return render(request, 'sign_in.html', context)

    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'sign_in.html', context)

#登出
def sign_out(request):
    logout(request)
    return redirect('/sign_in')