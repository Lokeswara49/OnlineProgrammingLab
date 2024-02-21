import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from base.models import Question, Room, Solution

from datetime import datetime, timedelta
from threading import Thread


def question(request, pk, pk2):
    question = Question.objects.get(id=pk2)
    submitFlag = True

    room = Room.objects.get(id=pk)
    username = request.user.get_username()
    user = User.objects.get(username=username)

    # as multiple submissions are possible we are using this, change this after submission is changed
    # no need change too it can handle single submission too
    solution = Solution.objects.filter(room=room, question=question, user=user)
    sol = solution.last()
    if sol:
        code = sol.code
        input = sol.input
    else:
        code = ""
        input = ""
    output = ""

    context = {'question': question, "code": code, "input": input, "output": output, 'submitFlag': submitFlag}
    return render(request, "question.html", context)


RUN_TIME_LIMIT = 5


def runCode(request, pk, pk2):
    if 'run' in request.POST:
        if request.method == 'POST':
            code = request.POST['code']
            input = request.POST['input']
            y = input
            input_part = input.replace("\n", " ").split(" ")

            def input():
                a = input_part[0]
                del input_part[0]
                return a

            try:
                """ def monitorProgress():
                    isCompleted = False
                    start_time = datetime.now()
                    while not isCompleted:
                        if datetime.now() > start_time + timedelta(seconds=RUN_TIME_LIMIT):
                            isCompleted = True
                            raise RuntimeError("Time Out!!!")

                t = Thread(target=monitorProgress())
                t.start()"""
                orig_stdout = sys.stdout
                sys.stdout = open('file.txt', 'w')
                exec(code)
                sys.stdout.close()
                sys.stdout = orig_stdout
                output = open('file.txt', 'r').read()
            except RuntimeError as re:
                output = re
            except Exception as e:
                sys.stdout.close()
                sys.stdout = orig_stdout
                output = e
            print(output)
        submitFlag = True
        question = Question.objects.get(id=pk2)
        context = {'question': question, "code": code, "input": y, "output": output, 'submitFlag': submitFlag}
        return render(request, 'question.html', context)

    if 'final_submit' in request.POST:
        if request.method == "POST":
            room = Room.objects.get(id=pk)
            question = Question.objects.get(id=pk2)
            username = request.user.get_username()
            user = User.objects.get(username=username)
            solution = Solution.objects.filter(room=room, question=question, user=user)
            if len(solution) >= 1:
                sol = solution.last()
                sol.code = request.POST['code']
                sol.input = request.POST['input']
                sol.save()
            else:
                code = request.POST['code']
                input = request.POST['input']
                sol_info = Solution(code=code, user=user, question=question, room=room, input=input)
                sol_info.save()
        context = {'room': room}
        return render(request, "submitted.html", context)


# this view is not being used as runCode is handling both
def finalSubmit(request, pk, pk2):
    if request.method == "POST":
        code = request.POST['code']
        input = request.POST['input']
        username = request.user.get_username()
        user = User.objects.get(username=username)
        question = Question.objects.get(id=pk2)
        room = Room.objects.get(id=pk)

        sol_info = Solution(code=code, user=user, question=question, room=room, input=input)
        sol_info.save()

    context = {'room': room}
    return render(request, "submitted.html", context)


@login_required(login_url='login')
def viewResponses(request, pk, pk2, pk3):
    question = Question.objects.get(id=pk2)
    solution = Solution.objects.get(id=pk3)
    code = solution.code
    if solution.input == None:
        input = ""
    else:
        input = solution.input
    output = ""
    submitFlag = False
    context = {'question': question, "code": code, "input": input, 'output': output, 'submitFlag': submitFlag}
    return render(request, 'question.html', context)


@login_required(login_url='login')
def runResponse(request, pk, pk2, pk3):
    if request.method == 'POST':
        code = request.POST['code']
        input = request.POST['input']
        y = input
        input_part = input.replace("\n", " ").split(" ")

        def input():
            a = input_part[0]
            del input_part[0]
            return a

        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(code)
            sys.stdout.close()
            sys.stdout = orig_stdout
            output = open('file.txt', 'r').read()
        except RuntimeError as re:
            output = re
        except Exception as e:
            sys.stdout.close()
            sys.stdout = orig_stdout
            output = e
        print(output)

    question = Question.objects.get(id=pk2)
    context = {'question': question, "code": code, "input": y, "output": output}
    return render(request, 'question.html', context)
