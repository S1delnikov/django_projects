from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from .models import Task, Subtask
from datetime import datetime

def index(request):
    """Домашняя страница приложения todo_list"""
    return render(request, 'todo_list/index.html')


@login_required
def tasks(request):
    """Страница с задачами"""
    tasks = Task.objects.filter(owner=request.user)
    subtasks = dict()
    for task in tasks:
        subtasks[task.id] = task.subtask_set.all()                                              # Подзадачи каждой конкретной задачи
        if len(task.subtask_set.filter(status=True).all()) == len(task.subtask_set.all()):      # Изменение статуса задачи, если все подзадачи
                                                                                                # были выполнены
            task.status = True
            task.save()
        else:
            task.status = False
            task.save()
    context = {'tasks': tasks, 'subtasks': subtasks}
    return render(request, 'todo_list/tasks.html', context)


@login_required
@csrf_exempt
def new_task(request):
    task = Task()
    task.owner = request.user
    task.text = request.POST.get('new-task-name')

    if request.POST.get('new-task-startdate') == "0000-00-00T00:00":
        task.date_added = datetime.now    
    else:
        task.date_added = request.POST.get('new-task-startdate')
    
    if request.POST.get('new-task-deadline') == "0000-00-00T00:00":
        task.deadline = datetime.now
    else:
        task.deadline = request.POST.get('new-task-deadline')
    print(f'{task.text} {task.date_added} {task.deadline}')
    task.save()
    return redirect('todo_list:tasks')


@login_required
@csrf_exempt
def update_task_data(request):
    task_id = request.POST.get('task_id')
    task_on_update = Task.objects.get(id=task_id)
    task_on_update.text = request.POST.get('task_name')
    task_on_update.date_added = request.POST.get('add_date')
    task_on_update.deadline = request.POST.get('deadline')

    task_on_update.save()

    csrf_token = get_token(request)

    return JsonResponse({'csrf_token': csrf_token}, status=200)


@login_required
@csrf_exempt
def delete_task(request):
    task_id = request.POST.get('task_id')
    task_on_delete = Task.objects.get(id=task_id)
    task_on_delete.delete()
    return JsonResponse({}, status=200)


@login_required
def savemark(request, task_id, subtask_id, status):
    """Изменение статуса подзадачи"""
    # JavaScript возвращает 'false' с маленькой буквы, а в Python используется 'False'
    task = Task.objects.get(id=task_id)
    if task.owner != request.user:
        raise Http404
    if status == 'false':
        status = False
    task = Task.objects.get(id=task_id)
    subtask = task.subtask_set.get(id=subtask_id)
    subtask.status = status
    subtask.save()
    print(f"Checkbox marked - {task_id} {subtask_id} {status}")
    return redirect('todo_list:tasks')
    # return HttpResponse(status=200)
    # return render(request, request.META.get('HTTP_REFERER'))
    # Переход на предыдущую страницу
    # return redirect(request.META.get('HTTP_REFERER'))


@login_required
@csrf_exempt
def update_task(request, task_id, subtask_id, text):
    """Обновляет текст подзадачи"""
    task = Task.objects.get(id=task_id)
    if task.owner != request.user:
        raise Http404
    if request.POST.get('subtask_text') != text:
        subtask = Subtask.objects.get(id=subtask_id)
        subtask.text = request.POST.get('subtask_text')     # Получение текста из textbox'а
        subtask.save()
        #print(f"Got it! task_id {task_id}   subtask_id {subtask_id} text    {request.POST.get('subtask_text')}")
        return redirect('todo_list:tasks')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@csrf_exempt
def new_subtask(request):
    """Создаёт новую подзадачу"""
    # print("AJAX is working!")
    # print(request.POST.get('subtask_text'), request.POST.get('task_id'))

    # task_id = request.POST.get('task_id')
    if len(request.POST.get('subtask_text')) == 0:
        return JsonResponse({'error': True, 'message': "Поле абсолютно пустое."}, status=200)
    task = Task.objects.get(id=request.POST.get('task_id'))
    subtask_text = request.POST.get('subtask_text')

    new_subtask = Subtask()
    new_subtask.task = task
    new_subtask.text = subtask_text
    new_subtask.status = False

    new_subtask.save()

    csrf_token = get_token(request)
    new_subtask_id = new_subtask.id
    # name = 'Misha'

    return JsonResponse({'csrftoken': csrf_token, 'new_subtask_id': new_subtask_id}, status=200)


@login_required
@csrf_exempt
def delete_subtask(request):
    print(request.POST.get('subtask_id'))
    subtask_id = request.POST.get('subtask_id')
    subtask_on_delete = Subtask.objects.get(id=subtask_id)
    subtask_on_delete.delete()
    return JsonResponse({}, status=200)


@login_required
@csrf_exempt
def get_csrftoken(request):
    csrf_token = get_token(request)

    return JsonResponse({'csrftoken': csrf_token}, status=200)