from django.shortcuts import render, redirect
from forum.models import Thread, Comment, Board
from forum.forms import CommentForm, ThreadForm, SearchForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.decorators import check_signup_complete
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404
# Create your views here.

@login_required
@user_passes_test(check_signup_complete, login_url='accounts/profile_info/')
def new_comment(request, board_slug, thread_slug, parent_id=None):
    try:
        board=Board.objects.get(slug=board_slug)
        thread=Thread.objects.get(slug=thread_slug, board=board)
    except ObjectDoesNotExist:
        raise Http404("This thread does not exist")
    form=CommentForm(request.POST)
    if form.is_valid():
        if parent_id is not None:
            try: 
                parent=Comment.objects.get(pk=parent_id, thread=thread)
            except ObjectDoesNotExist:
                raise Http404("The comment you are replying to does not exist")
        else:
            parent=None
        comment = Comment(
            user = request.user,
            thread = thread,
            parent= parent,
            text=form['text'],
        )
        comment.save()
    return redirect(thread)

@login_required
@user_passes_test(check_signup_complete, login_url='accounts/profile_info/')
def edit_comment(request, comment_id):
    try:
        comment=Comment.objects.get(pk=comment_id, user=request.user)
    except ObjectDoesNotExist:
        raise Http404("The comment you are trying to edit does not exist or your action is unauthorized.")
    form = CommentForm(request.POST)
    if form.is_valid():
        comment.text = form['text']
        comment.save()
    return redirect(comment.thread)

@login_required
@user_passes_test(check_signup_complete, login_url='accounts/profile_info/')
def new_thread(request, board_slug):
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                board = Board.objects.get(slug=board_slug)
            except ObjectDoesNotExist:
                raise Http404("This board does not exist.")
            thread = form.save(commit=False)
            thread.board=board
            thread.user=request.user
            thread.save()
            return redirect(thread)
        else:
            form.add_error(None, "Invalid input. Try again.")
    else:
        form = ThreadForm()
    return render(request, 'forum/thread.html', {'form': form})

@login_required
@user_passes_test(check_signup_complete, login_url='accounts/profile_info/')
def edit_thread(request, board_slug, thread_slug):
    try:
        board = Board.objects.get(slug=board_slug)
    except:
        raise Http404("This board does not exist.")
    try:
        thread = Thread.objects.get(slug=thread_slug, user=request.user, board=board)
    except:
        raise Http404("This thread does not exist or you are not authorized to edit it.")
    if request.method=='POST':
        form = ThreadForm(request.POST, request.FILES, instance=thread)
        if form.is_valid():
            form.save()
            return redirect(thread)
        else:
            form.add_error(None, "Something went wrong. Try again.")
    else:
        form=ThreadForm(instance=thread)
    return render(request, 'forum/thread.html', {'form': form})

@login_required
@user_passes_test(check_signup_complete, login_url='accounts/profile_info/')
def new_board(request):
    context = {}
    if request.method=='POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.moderators.add(request.user)
            a.save()
            a.save_m2m()
        else:
            form.add_error(None,"Form submission invalid. Please try again.")
    else:
        form = BoardForm()
    context['form'] = form
    return render(request, 'forum/board.html', context)

@login_required
@user_passes_test(check_signup_complete, login_url='accounts/profile_info/')
def edit_board(request, board_slug):
    context={}
    try:
        board = Board.objects.get(slug=board_slug)
        if not request.user in board.moderators.all():
            return HttpResponse("403 FORBIDDEN", status=403)
    except ObjectDoesNotExist:
        raise Http404("Board not found")
    if request.method=='POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect(board)
        else:
            form.add_error(None, "Please try again")
    else:
        form = BoardForm(instance=board)
    return render(request, 'forum/board.html', {'form': form})


@login_required
@user_passes_test(check_signup_complete, login_url='accounts/profile_info/')
def vote(request):
    kind = request.POST.get('kind', None)
    pk = request.POST.get('pk', None)
    if kind is None or pk is None:
        return HttpResponse(status=400, "BAD REQUEST")
    else:
        if kind == 'comment':
            try:
                com = Comment.objects.get(pk=pk)
            except ObjectDoesNotExist:
                return HttpResponse(status=404, "COMMENT DOES NOT EXIST")
            prev_likes = Upvote.objects.filter(user=request.user, comment=com)
            if prev_likes is not None:
                prev_likes.first().delete()
            else:
                upvote = Upvote(user=request.user, comment=com)
                upvote.save()
        elif kind == 'thread':
            try:
                thread = Thread.objects.get(pk=pk)
            except ObjectDoesNotExist:
                return HttpResponse(status=404, "THREAD DOES NOT EXIST")
            prev_liked = Upvote(user=request.user, thread=thread)
            if prev_liked is not None:
                prev_liked.first().delete()
            else:
                upvote = Upvote(user=request.user, thread=thread)
                upvote.save()
        else:
            return HttpResponse(status=400, "BAD REQUEST")
    return HttpResponse(status=200, "OK")
 
##auth not required views

def view_thread(request, board_slug, thread_slug):
    try:
        board = Board.objects.get(slug=board_slug)
    except ObjectDoesNotExist:
        raise Http404("This board does not exist.")
    try:
        thread = Thread.objects.get(slug=thread_slug, board=board)
    except ObjectDoesNotExist:
        raise Http404("The thread you are looking for does not exist.")
    comments = Comment.objects.filter(thread=thread, parent=None).annotate(vote_count=Count('upvotes')).order_by('-vote_count')
    context={
        'thread': thread,
        'comment_form': CommentForm(),
        'search_form': SearchForm(),
        'top_level_comments': comments
    }
    return render(request, 'forum/view_thread.html', context)

def view_board(request, board_slug, method="hot"):
    try:
        board = Board.objects.get(slug=board_slug)
    except ObjectDoesNotExist:
        raise Http404("this board does not exist")
    time = request.GET.get('time', '')
    context = {
        'board': board,
        'threads': board.threads.all().rank(method, time),
        'search_form': SearchForm()
    }
    return render(request, 'forum/view_board.html', context)

def search(request):
    search_term = request.GET.get('search_term', '')
    board = request.GET.get('board', '')
    try:
        board = Board.objects.get(slug=board)
        threads = board.threads.all()
    except ObjectDoesNotExist:
        threads = Thread.objects.all()
    threads = threads.filter(Q(title__icontains=search_term) | Q(text__icontains=search_term))
    return render(request, 'forum/search.html', {'form': SearchForm(), 'results': threads})

def index(request):
    hot_threads = Thread.objects.all().order_by('-hot_score')
    return render(request, 'forum/index.html', {'search_form': SearchForm(), 'boards': Board.objects.all(), 'threads': hot_threads})







