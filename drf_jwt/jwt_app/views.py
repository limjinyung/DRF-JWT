from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status

from .models import Task, Developer
from .serializer import TaskSerialzer

import json
from django.core.exceptions import ObjectDoesNotExist


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Welcome, Developers!'}
        return Response(content)


# @api_view(['GET'])
# def task_list(request):
#     tasks = Task.objects.all()
#
#     task_serializer = TaskSerialzer(tasks, many=True)
#     return JsonResponse(task_serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    all_task=Task.objects.all()
    serializer=TaskSerialzer(all_task, many=True)
    print(serializer, serializer.data)
    # return JsonResponse({'all task':serializer.data}, safe=False, status=status.HTTP_200_OK)
    return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):

    print("Hello")
    print(request.get())
    payload=json.loads(request.body)
    print(payload)
    try:
        new_task=Task.objects.create(
            name=payload["name"],
            description=payload["description"],
        )
        print(new_task)
        serializer=TaskSerialzer(new_task)
        return JsonResponse({'new task': serializer.data},safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse ({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse ({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # new_task=Task(name=name, desciption=desciption)
    #
    # if new_task.save():
    #     return HttpResponse(status=201)
    # else:
    #     return HttpResponse(status=400))


    return HttpResponse(status=200)