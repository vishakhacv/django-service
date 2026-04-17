import hashlib
from datetime import date

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task, User, PersonalAccessToken
from .serializers import TaskSerializer


def get_authenticated_user(request):
    """
    Verify the Sanctum bearer token from the Authorization header.
    Returns the User or None.
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None

    raw_token = auth_header[7:]  # strip "Bearer "

    # Sanctum stores SHA-256 hash of the token part after the pipe
    if '|' in raw_token:
        token_value = raw_token.split('|', 1)[1]
    else:
        token_value = raw_token

    token_hash = hashlib.sha256(token_value.encode('utf-8')).hexdigest()

    try:
        pat = PersonalAccessToken.objects.get(token=token_hash)
        user = User.objects.get(id=pat.tokenable_id)
        return user
    except (PersonalAccessToken.DoesNotExist, User.DoesNotExist):
        return None


@api_view(['POST'])
def check_overdue(request):
    """
    Scan all tasks and mark overdue ones:
    - Tasks with due_date < today AND status NOT IN (DONE, OVERDUE) → set OVERDUE
    """
    today = date.today()
    overdue_tasks = Task.objects.filter(
        due_date__lt=today
    ).exclude(
        status__in=['DONE', 'OVERDUE']
    )

    count = overdue_tasks.count()
    overdue_tasks.update(status='OVERDUE')

    return Response({
        'message': f'{count} task(s) marked as overdue.',
        'marked_count': count,
    })


@api_view(['POST'])
def close_overdue_task(request, task_id):
    """
    Close (mark as DONE) an overdue task. Only admin can do this.
    """
    user = get_authenticated_user(request)
    if not user:
        return Response(
            {'error': 'Authentication required.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if user.role != 'admin':
        return Response(
            {'error': 'Only admin can close overdue tasks.'},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if task.status != 'OVERDUE':
        return Response(
            {'error': 'Only overdue tasks can be closed via this endpoint.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    task.status = 'DONE'
    task.save()

    return Response({
        'message': f'Task "{task.title}" has been closed.',
        'task': TaskSerializer(task).data,
    })


@api_view(['GET'])
def list_overdue_tasks(request):
    """
    List all tasks with status = OVERDUE.
    """
    tasks = Task.objects.filter(status='OVERDUE')
    serializer = TaskSerializer(tasks, many=True)

    return Response({
        'count': tasks.count(),
        'tasks': serializer.data,
    })
