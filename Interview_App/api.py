from django.http import HttpResponse
from rest_framework import viewsets, status , permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AudioFile , AuthToken
from .forms import AudioFileSerializer , UserSerializer , AuthTokenSerializer
from .Audio_Emotion.predict import LivePredictions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

def hello_view(request):
    return HttpResponse("Hello")

class AudioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

    @action(detail=False, methods=['post'])
    def upload_audio(self, request, *args, **kwargs):
        print("upload_audio is being called")  # Debugging print statement
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            audio_file_instance = serializer.save()
            print(audio_file_instance.recording.path)
            prediction = LivePredictions.predict(audio_file_instance.recording.path)
            return Response({
                'message': 'Audio uploaded and processed successfully!',
                'prediction': prediction,
                'recording': request.build_absolute_uri(audio_file_instance.recording.url),
                'question': audio_file_instance.question_id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create tokens for the newly created user
            refresh = RefreshToken.for_user(user)
            token = AuthToken.objects.create(user=user, token=refresh.access_token)  # Implement your token generation logic
            return Response({
                'status': 'User registered',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny])
    def login(self, request):
        # Assuming you have some method of validating credentials
        serializer = AuthTokenSerializer(data=request.data)  # Define this serializer
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            token = AuthToken.objects.create(user=user, token=refresh.access_token)  # Implement your token generation logic
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
