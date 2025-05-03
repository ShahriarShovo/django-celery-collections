
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, EmailVerificationToken
from .utils import generate_token, hash_token
from .tasks import send_verification_email
from django.utils import timezone
from datetime import timedelta
from accounts.sign_up_serializers import RegisterSerializer, VerifyEmailSerializer


@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "User created, check email"})

@api_view(['POST'])
def resend_otp_view(request):
    email = request.data.get("email")
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"error": "User not found"}, status=404)
    # Rate Limit: per two min 1 time
    latest_token = EmailVerificationToken.objects.filter(user=user).order_by('-created_at').first()
    if latest_token and timezone.now() - latest_token.created_at < timedelta(minutes=2):
        return Response({"error": "Please wait before resending."}, status=429)

    token = generate_token()
    token_hash = hash_token(token)
    EmailVerificationToken.objects.create(user=user, token_hash=token_hash)
    send_verification_email.delay(user.email, token)
    
    return Response({"message": "Token resent."})



from rest_framework import status
@api_view(['GET'])
def verify_email_view(request):
    email = request.query_params.get('email')
    token = request.query_params.get('token')

    if not email or not token:
        return Response({"error": "Missing email or token"}, status=400)

    try:
        user = User.objects.get(email=email)
        ev_token = EmailVerificationToken.objects.filter(user=user).latest('created_at')
    except:
        return Response({"error": "Invalid email or token"}, status=400)

    if ev_token.is_expired():
        return Response({"error": "Token expired"}, status=400)

    from accounts.utils import verify_token_hash
    if not verify_token_hash(token, ev_token.token_hash):
        return Response({"error": "Invalid token"}, status=400)

    user.is_verified = True
    user.save()
    ev_token.delete()
    return Response({"message": "Email verified!"}, status=200)






