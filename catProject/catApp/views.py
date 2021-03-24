from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, HuntingSerializer, CatSerializer
from .models import User, Cat, lootTypes


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if user != request.user:
            return Response({"response":"Access forbidden. Only owner can see his cats."}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# workaround
def validate_loots(loots):
    if loots is None or not isinstance(loots,list):
        return False
    for loot in loots:
        if loot not in lootTypes:
            return False
    return True

class HuntingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, idcat):
        try:
            cat = Cat.objects.get(id=idcat)
        except Cat.DoesNotExist:
            return Response({"response": "Cat not found."},status=status.HTTP_404_NOT_FOUND)
        if cat.owner != request.user:
            return Response({"response":"Access forbidden. Only cat's owner can manage huntings."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CatSerializer(cat)
        return Response(serializer.data)

    def post(self, request, idcat):
        try:
            cat = Cat.objects.get(id=idcat)
        except Cat.DoesNotExist:
            return Response({"response": "Cat not found."}, status=status.HTTP_404_NOT_FOUND)
        if cat.owner != request.user:
            return Response({"response":"Access forbidden. Only cat's owner can manage huntings."}, status=status.HTTP_403_FORBIDDEN)
        serializer = HuntingSerializer(data=request.data)
        if serializer.is_valid():
            if idcat != request.data['hunter']:
                return Response({"response" : "Cat id and hunter id don't match. Check request." }, status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data['dateStart'] >= serializer.validated_data['dateEnd']:
                return Response({"response" : "End date must be after start date." }, status=status.HTTP_400_BAD_REQUEST)
            if not validate_loots(request.data['loots']):
                return Response({"response" : "Invalid loot type passed. Check the list of available types." }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WelcomeAPIView(APIView):

    def get(self, request):
        return Response({'response': 'Welcome. Try ./login to get login token, later ./users/id or ./hunting/catid'}, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):

    def get(self, request, *args, **kwargs):
        return Response({'response':'Post username and password to get your access token'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
