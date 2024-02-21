from datetime import datetime

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from OnlineProgrammingLab import settings
from .models import Room, Question, Solution, VerifiedUser
from .forms import RoomForm, QuestionForm, SolutionForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User



@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(name__icontains=q), verified=True
    )

    room_count = rooms.count()

    # checking for joined status
    username = request.user.get_username()
    user = User.objects.get(username=username)
    special = []
    for i in rooms:
        if len(VerifiedUser.objects.filter(room=i, user=user)) == 1:
            special.append(True)
        else:
            special.append(False)
    zip_context = zip(rooms, special)

    context = {'rooms': rooms, 'room_count': room_count, 'zip': zip_context}
    return render(request, "home.html", context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    questions = Question.objects.filter(room=room)

    username = request.user.get_username()
    user = User.objects.get(username=username)

    # for solved button
    special = []
    for i in questions:
        if len(Solution.objects.filter(question=i, user=user)) == 1:
            special.append(True)
        else:
            special.append(False)

    # print(special)
    queryset = VerifiedUser.objects.filter(room=room, user=user)
    if not queryset and username == 'admin':
        info = VerifiedUser(room=room, user=user, is_verified=True)
        info.save()

    elif not queryset:
        return redirect('verifyUser', room.id)

    zip_context = zip(questions, special)
    context = {'room': room, 'questions': questions, 'zip': zip_context}

    return render(request, "room.html", context)


# remove this view as it is moved to compiler app
def question(request, pk, pk2):
    """
    For Submission
    """
    form = SolutionForm()
    # above one for form
    question = Question.objects.get(id=pk2)
    context = {'question': question, 'form': form}
    return render(request, "question.html", context)


@login_required(login_url='login')
def createRoom(request):
    if request.method == "POST":
        name = request.POST.get('roomname')  # name of element in form
        description = request.POST['description']
        room_password = request.POST['roompassword']
        username = request.user.get_username()
        host = User.objects.get(username=username)

        # admin can directly create room
        if username == 'admin':
            room_info = Room(host=host, name=name, description=description, room_password=room_password, verified=True)
            room_info.save()
            msg = name + " room is created. "
            messages.success(request, msg, extra_tags='info')
            if request.POST['btnradio'] == 'btnradio1':
                return redirect('createQuestion', room_info.id)
            return redirect('home')

        room_info = Room(host=host, name=name, description=description, room_password=room_password)
        room_info.save()

        room = Room.objects.get(name=name)
        user = User.objects.get(username=username)
        info = VerifiedUser(room=room, user=user, is_verified=True)
        info.save()

        if username != 'admin':
            user = User.objects.get(username='admin')
            info = VerifiedUser(room=room, user=user, is_verified=True)
            info.save()

        if request.POST['btnradio'] == 'btnradio1':
            return redirect('createQuestion', room_info.id)
        else:
            msg = name + " room is created. Please wait for approval."
            messages.success(request, msg, extra_tags='info')
            return redirect('home')
    context = {}
    return render(request, "form2.html", context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        room = Room.objects.get(id=pk)
        room.name = request.POST.get('roomname')  # name of element in form
        room.description = request.POST['description']
        room.room_password = request.POST['roompassword']
        room.save()

        msg = room.name + " room successfully updated"
        messages.success(request, msg, extra_tags='warning')

        return redirect('home')

    context = {'room': room}
    return render(request, "form2.html", context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        room.delete()

        msg = room.name + " room successfully deleted"
        messages.success(request, msg, extra_tags='danger')

        return redirect('home')

    return render(request, "delete.html", {'obj': room})


@login_required(login_url='login')
def createQuestion(request, pk):
    if request.method == "POST":
        question_title = request.POST.get('questiontitle')
        question_full = request.POST['fullquestion']
        sample_test_case = request.POST['testcase']

        room = Room.objects.get(id=pk)

        question_info = Question(question_title=question_title, question_full=question_full,
                                 sample_test_case=sample_test_case, room=room)

        if request.POST['btnradio'] == 'btnradio1':
            question_info.save()
            return redirect('createQuestion', room.id)
        elif request.POST['btnradio'] == 'btnradio2':
            question_info.save()

            msg = " Question(s) added successfully "
            messages.success(request, msg, extra_tags='info')

            return redirect('room', room.id)
        else:
            return redirect('room', room.id)
    context = {}
    return render(request, "question_form2.html", context)


@login_required(login_url='login')
def updateQuestion(request, pk, pk2):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)
    # form = QuestionForm(instance=question)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        question = Question.objects.get(id=pk2)
        question.question_title = request.POST.get('questiontitle')
        question.question_full = request.POST['fullquestion']
        question.sample_test_case = request.POST['testcase']
        question.save()

        msg = " Question updated successfully "
        messages.success(request, msg, extra_tags='warning')

        return redirect('room', room.id)

    context = {'question': question}
    return render(request, "question_form2.html", context)


@login_required(login_url='login')
def deleteQuestion(request, pk, pk2):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        question.delete()

        msg = " Question deleted successfully "
        messages.success(request, msg, extra_tags='danger')

        return redirect('room', room.id)

    return render(request, "delete.html", {'obj': question})


# move to compiler-app
def finalSubmit(request):
    if request.method == "POST":
        form = SolutionForm(request.POST)
        if form.is_valid():
            form.save()
    context = {}
    return render(request, "submitted.html", context)


# responses related views
@login_required(login_url='login')
def roomResponses(request, pk):
    room = Room.objects.get(id=pk)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    solutions = Solution.objects.filter(room=room)

    context = {'solutions': solutions, 'room': room}
    return render(request, "responses.html", context)


@login_required(login_url='login')
def questionResponses(request, pk, pk2):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    solutions = Solution.objects.filter(question=question)

    context = {'solutions': solutions, 'room': room, 'question': question}
    return render(request, "responses.html", context)


# shifted to compiler-app
@login_required(login_url='login')
def viewResponses(request, pk, pk2, pk3):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)
    solution = Solution.objects.get(id=pk3)
    form = SolutionForm(instance=solution)
    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    context = {'form': form, 'question': question}
    return render(request, "view_response_question.html", context)


@login_required(login_url='login')
def deleteResponse(request, pk, pk2, pk3):
    room = Room.objects.get(id=pk)
    question = Question.objects.get(id=pk2)
    solution = Solution.objects.get(id=pk3)

    # checking for valid host
    if request.user.username not in [room.host.username, 'admin']:
        return HttpResponse("You can't do this ...")

    if request.method == "POST":
        solution.delete()
        msg = "Response of " + solution.user.username + " is successfully deleted"
        messages.success(request, msg, extra_tags='danger')
        return redirect('home')
    return render(request, "deleteResponse.html", {'obj': solution.user.username})


def unverifiedRooms(request):
    resultset = Room.objects.filter(verified=False)
    if request.user.username != "admin":
        return HttpResponse("You can't do this ...")

    context = {'rooms': resultset}
    return render(request, "unverified_rooms.html", context)


def approveRoom(request, pk):
    if request.user.username != "admin":
        return HttpResponse("You can't do this ...")

    room = Room.objects.get(id=pk)
    room.verified = True
    room.save()

    subject = "Online Programming Platform - Room Verification Details"
    context = {'room': room, }
    message = render_to_string('mails/approval_mail.html', context)
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [room.host.email])
    email.fail_silently = True
    email.send()

    msg = " Room " + room.name + " by " + room.host.username + " is approved successfully."
    messages.success(request, msg, extra_tags='info')

    return redirect('unverifiedRooms')


def rejectRoom(request, pk):
    if request.method == "POST":
        if request.user.username != "admin":
            return HttpResponse("You can't do this ...")

        room = Room.objects.get(id=pk)
        room.delete()

        msg = " Room " + room.name + " by " + room.host.username + " is rejected."
        messages.success(request, msg, extra_tags='danger')

        # mail to user regarding rejection.
        subject = "Online Programming Platform - Room Verification Details"
        reason = request.POST['reason']
        context = {'room': room, 'reason': reason}
        message = render_to_string('mails/rejection_mail.html', context)
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [room.host.email])
        email.fail_silently = True
        email.send()

        return redirect('unverifiedRooms')

    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'room_rejection.html', context)


@login_required(login_url='login')
def myRooms(request):
    resultset = Room.objects.filter(host=request.user, verified=True)

    unverifiedRooms = Room.objects.filter(host=request.user, verified=False)
    myroomsFlag = True

    username = request.user.get_username()
    user = User.objects.get(username=username)
    special = []
    for i in resultset:
        if len(VerifiedUser.objects.filter(room=i, user=user)) == 1:
            special.append(True)
        else:
            special.append(False)

    zip_context = zip(resultset, special)


    room_count = resultset.count()
    context = {'rooms': resultset, 'room_count': room_count, 'unverifiedRooms': unverifiedRooms,
               'myroomsFlag': myroomsFlag,'zip': zip_context}
    return render(request, "home.html", context)


@login_required(login_url='login')
def myProfile(request):
    username = request.user.get_username()  # get username
    user = User.objects.get(username=username)  # find that user using username
    resultset = Solution.objects.filter(user=user)  # get all the solutions of that user

    roomsjoined = VerifiedUser.objects.filter(user=user)

    context = {'solutions': resultset, 'user': user, 'roomsjoined': roomsjoined}
    return render(request, "myprofile.html", context)


def verifyUser(request, pk):
    if request.method == 'POST':
        room = Room.objects.get(id=pk)
        if room.room_password == request.POST['room_password']:
            # room.is_user_verified = True #not correct as only one user set enter correctly
            username = request.user.get_username()
            user = User.objects.get(username=username)
            queryset = VerifiedUser.objects.filter(room=pk, user=user)
            if not queryset:
                info = VerifiedUser(room=room, user=user, is_verified=True)
                info.save()

            msg = " User is successfully authenticated for " + room.name
            messages.success(request, msg, extra_tags='info')

            return redirect('room', room.id)
        else:
            msg = " Incorrect Room password "
            messages.success(request, msg, extra_tags='danger')
            return redirect('home')
    room = Room.objects.get(id=pk)
    username = request.user.get_username()
    user = User.objects.get(username=username)

    queryset = VerifiedUser.objects.filter(room=room, user=user)
    if queryset:
        verified = True
    else:
        verified = False
    context = {'verified': verified, 'room': room}
    return render(request, "room_verification.html", context)
