from rest_framework.decorators import api_view
from rest_framework.response import Response
from corecode.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializers = RoomSerializer(rooms, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def getRoom(request,values):
    room = Room.objects.get(id=values)
    serializers = RoomSerializer(room, many=False)
    return Response(serializers.data)