from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.parsers import FileUploadParser

from .models import Task, Developer
from .serializer import TaskSerialzer, DeveloperSerialzer
from django.core.exceptions import ObjectDoesNotExist

# upload document
from django.core.files.storage import FileSystemStorage

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Welcome, Developers!'}
        return Response(content)


# task views

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    all_task=Task.objects.all()
    serializer=TaskSerialzer(all_task, many=True)
    return JsonResponse({'all_task' :serializer.data}, safe=False, status=status.HTTP_200_OK)
    # return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_task(request):

    data = request.POST

    if isinstance(type(data), type(None)):
        raise AssertionError("Got NoneType, something went wrong")

    try:
        if data['todo']:
            specific_task = Task.objects.get(todo=data['todo'])
            serializer = TaskSerialzer(specific_task)
            return JsonResponse({'task': serializer.data}, safe=False, status=status.HTTP_200_OK)

        if data['description']:
            specific_task = Task.objects.get(todo=data['description'])
            serializer = TaskSerialzer(specific_task)
            return JsonResponse({'task': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'No such task'}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):

    # if header content_type='application/json'
    # use request.body and json.loads()
    data = request.POST

    try:
        new_task=Task.objects.create(
            todo=data.get('todo'),
            description=data.get('description'),
        )
        serializer=TaskSerialzer(new_task)
        return JsonResponse({'new task': serializer.data},safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse ({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):

    data = request.POST

    try:
        update_task=Task.objects.get(id=task_id)
        update_task.todo=data.get('todo')
        update_task.description = data.get('description')
        serializer=TaskSerialzer(update_task)
        return JsonResponse({'update task': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse ({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse ({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    try:
        delete_task=Task.objects.get(id=task_id)
        delete_task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# developers views

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def developer_list(request):

    try:
        all_developer = Developer.objects.all()
        serializer = DeveloperSerialzer(all_developer, many=True)
        return JsonResponse({'all developer': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_developer(request):

    data = request.POST

    if isinstance(type(data), type(None)):
        raise AssertionError("Got NoneType, something went wrong")

    try:
        search_name = data.get('name')
        if search_name is not None:
            specific_developer = Developer.objects.get(name=search_name)
            serializer = DeveloperSerialzer(specific_developer)
            return JsonResponse({'developer': serializer.data}, safe=False, status=status.HTTP_200_OK)

        search_email = data.get('email')
        if search_email is not None:
            specific_developer = Developer.objects.get(email=search_email)
            serializer = TaskSerialzer(specific_developer, many=True)
            return JsonResponse({'developer(s)': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_developer(request):

    data = request.POST

    try:
        new_developer=Developer.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            position=data.get('position')
        )

        print(data.getlist('task[]'))

        developer_task=data.getlist('task[]')
        for assign_task in developer_task:
            try:
                new_developer.task.add(Task.objects.get(id=assign_task))
            except ObjectDoesNotExist:
                return JsonResponse({'error': "Object not found"}, safe=False, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer=DeveloperSerialzer(new_developer)
        return JsonResponse({'new task': serializer.data},safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse ({'error': 'Something went wrong ' + str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_developer(request, developer_id):

    data = request.POST

    print("Hi")

    try:
        update_developer = Developer.objects.get(id=developer_id)

        if data.get('name') is not None:
            update_developer.name = data.get('name')

        if data.get('email') is not None:
            update_developer.email = data.get('email')

        if data.get('position') is not None:
            update_developer.position = data.get('position')

        serializer = DeveloperSerialzer(update_developer)
        return JsonResponse({'update developer': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_developer(request, developer_id):
    try:
        delete_developer=Developer.objects.get(id=developer_id)
        delete_developer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def image_upload(request):

    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
    else:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        task = Task.objects.get(todo=request.POST['todo'])
        task.image_attachment=myfile
        task.save()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Task does not exist'}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def document_upload(request):

    if request.method == 'POST' and request.FILES['document']:
        myfile = request.FILES['document']
    else:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        task = Task.objects.get(todo=request.POST['todo'])
        task.document_attachment = myfile
        task.save()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Task does not exist'}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)