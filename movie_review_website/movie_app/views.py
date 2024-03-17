from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import DetailView

from movie_app.models import Movies, Category, FavMovies, Review, Rating


# Create your views here.
def home(request):
    obj = Movies.objects.all()
    cat_obj = Category.objects.all()
    return render(request, 'homev2.html', {'obj': obj, 'cat_obj': cat_obj})


def movie_grid_fw(request, c_slug=None):
    c_page = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        movie_list = Movies.objects.all().filter(Q(title__contains=query) | Q(category__contains=query))
    elif c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movie_list = Movies.objects.all()
    else:
        movie_list = Movies.objects.all()
    paginator = Paginator(movie_list, 18)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'moviegridfw.html', {'category': c_page, 'movie': movie_list, 'products': products})


def movie_single(request, id):
    movie = Movies.objects.get(id=id)
    if request.method == 'POST':
        review_username = request.user.username
        review_movie = movie.title
        review = request.POST['review']
        review_obj = Review(username=review_username, movie=review_movie, review=review)
        review_obj.save()
    review_obj = Review.objects.all()

    paginator = Paginator(review_obj, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, 'moviesingle.html',
                  {'id': id, 'movie': movie, 'review_obj': review_obj, 'products': products})


def user_favorite_grid(request):
    mov_obj = Movies.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        fav_obj = FavMovies.objects.all().filter(Q(favtitle__contains=query) | Q(category__contains=query))
    else:
        fav_obj = FavMovies.objects.all()

    paginator = Paginator(fav_obj, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, 'userfavoritegrid.html', {'fav_obj': fav_obj, 'mov_obj': mov_obj, 'products': products})


def user_profile(request):
    usr = request.user
    mov = Movies.objects.all()
    fav = FavMovies.objects.all()
    rev = Review.objects.all()
    if request.method == 'POST':
        update_username = request.POST['update_username']
        update_email = request.POST['update_email']
        update_firstname = request.POST['update_firstname']
        update_lastname = request.POST['update_lastname']
        update_newpass = request.POST['newpass']
        update_cnewpass = request.POST['cnewpass']
        for i in mov:
            if i.username == usr.username:
                i.username = update_username
                i.save()
        for j in fav:
            if j.username == usr.username:
                j.username = update_username
                j.save()
        for k in rev:
            if k.username == usr.username:
                k.username = update_username
                k.save()
        usr.username = update_username
        usr.first_name = update_firstname
        usr.last_name = update_lastname
        usr.email = update_email
        if update_newpass == update_cnewpass:
            usr.set_password(update_newpass)
        usr.save()

        auth.logout(request)
        return redirect('/')
    return render(request, 'userprofile.html')


def user_rate(request):
    movie = Movies.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        movie = Movies.objects.all().filter(Q(title__contains=query) | Q(category__contains=query))
    else:
        movie = Movies.objects.all()
    return render(request, 'userrate.html',{'movie':movie})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Exist")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Exist")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()
                messages.info(request, "User Registration Successfull")
                return redirect('/')
        else:
            messages.info(request, "Password Don't Match")
            return redirect('register')

    return render(request, 'homev2.html')


def login(request):
    obj = Movies.objects.all()
    cat_obj = Category.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'homev2.html', {'obj': obj, 'cat_obj': cat_obj})


def logout(request):
    auth.logout(request)
    obj = Movies.objects.all()
    cat_obj = Category.objects.all()
    return render(request, 'homev2.html', {'obj': obj, 'cat_obj': cat_obj})


def add_movie(request, c_slug=None):
    cat_list = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        poster = request.FILES['poster']
        username = request.user
        desc = request.POST.get('description')
        release_date = request.POST.get('release_date')
        actor = request.POST.get('actor')
        director = request.POST.get('director')
        writer = request.POST.get('writer')
        category = request.POST.get('cars')
        movie_link = request.POST.get('traile_url')

        movie = Movies(title=title, poster=poster, username=username, desc=desc, release_date=release_date, actor=actor,
                       director=director,
                       writer=writer, category=category, movie_link=movie_link)
        movie.save()
        return redirect('/')
    return render(request, 'addmovie.html', {'list': cat_list})


def delete_movie(request, id):
    movie = Movies.objects.all()
    mov = Movies.objects.get(id=id)
    fav = FavMovies.objects.all()
    category = Category.objects.all()
    if request.user.username == mov.username:
        for i in fav:
            if mov.title == i.favtitle:
                mov.delete()
                i.delete()
            else:
                mov.delete()
                break
        else:
            mov.delete()
    return render(request, "moviegridfw.html", {'category': category, 'movie': movie})


def edit_movie(request, id):
    movie = Movies.objects.get(id=id)
    if request.method == 'POST':
        if request.user.username == movie.username:
            editposter = request.FILES['editposter']
            editdescription = request.POST['editdescription']
            editrelease_date = request.POST['editrelease_date']
            edittraile_url = request.POST['edittraile_url']
            movie.poster = editposter
            movie.desc = editdescription
            movie.release_date = editrelease_date
            movie.movie_link = edittraile_url
            movie.save()
    return render(request, 'moviesingle.html', {'id': id, 'movie': movie})


def fav_movie(request, id):
    movie = Movies.objects.get(id=id)
    fav = FavMovies.objects.all()
    user = request.user
    count = 0
    new = 0
    a = 0
    for i in fav:
        if movie.title == i.favtitle and user.username != i.username:
            a += 1
            count = 0
            new = 0
        elif user.username == i.username and movie.title != i.favtitle:
            new = 0
            count += 1
            a = 0
        elif user.username != i.username and movie.title != i.favtitle:
            count = 0
            new += 1
            a = 0
        elif user.username == i.username and movie.title == i.favtitle:
            count = 0
            new = 0
            a = 0
            break

    if count > 0 or new > 0 or a > 0:
        favtitle = movie.title
        poster = movie.poster
        user = user.username
        desc = movie.desc
        release_date = movie.release_date
        actor = movie.actor
        director = movie.director
        writer = movie.writer
        category = movie.category
        movie_link = movie.movie_link

        favmovie = FavMovies(favtitle=favtitle, poster=poster, username=user, desc=desc,
                             release_date=release_date,
                             actor=actor,
                             director=director,
                             writer=writer, category=category, movie_link=movie_link)
        favmovie.save()

    if not fav:
        favtitle = movie.title
        poster = movie.poster
        user = user.username
        desc = movie.desc
        release_date = movie.release_date
        actor = movie.actor
        director = movie.director
        writer = movie.writer
        category = movie.category
        movie_link = movie.movie_link

        favmovie = FavMovies(favtitle=favtitle, poster=poster, username=user, desc=desc, release_date=release_date,
                             actor=actor,
                             director=director,
                             writer=writer, category=category, movie_link=movie_link)
        favmovie.save()
    review_obj = Review.objects.all()
    paginator = Paginator(review_obj, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, "moviesingle.html",
                  {'id': id, 'review_obj': review_obj, 'movie': movie, 'products': products})


def del_fav_movie(request, id):
    movie = Movies.objects.get(id=id)
    fav = FavMovies.objects.all()
    user = request.user
    for i in fav:
        if user.username == i.username:
            if movie.title == i.favtitle:
                i.delete()
                break
    return render(request, "moviesingle.html", {'id': id, 'movie': movie})


def rate_movie(request,id):
    movie = Movies.objects.get(id=id)
    user=request.user
    if request.method == 'GET':
        rating = request.GET.get('star-input')
        rate = Rating(username=user.username, movie=movie.title,rating=rating)
        rate.save()
    rat_list = Rating.objects.all()
    count=0
    rat_sum=0
    for rat in rat_list:
        if movie.title == rat.movie:
            count+=1
            rat_sum+=rat.rating
    avg=round(((rat_sum/(count*5))*5),2)
    movie.rating=avg
    movie.save()
    return render(request,'moviesingle.html',{'id': id, 'movie': movie,'avg':avg})