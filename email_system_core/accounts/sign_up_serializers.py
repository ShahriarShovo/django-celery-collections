from rest_framework import serializers
from accounts.models.signup import User, EmailVerificationToken
from accounts.utils import generate_token, hash_token
from accounts.tasks import send_verification_email
from django.utils import timezone
from django.db import transaction


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=True)
        token = generate_token()
        token_hash = hash_token(token)
        EmailVerificationToken.objects.create(user=user, token_hash=token_hash)
        #send_verification_email.delay(user.email, token)
        transaction.on_commit(lambda: send_verification_email.delay(user.email, token))
        return user 
    
    
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        token = attrs.get('token')
        
        try:
            user = User.objects.get(email=email)
            ev_token = EmailVerificationToken.objects.filter(user=user).latest('created_at')
        except:
            raise serializers.ValidationError("Invalid email or token")
        
        if ev_token.is_expired():
            raise serializers.ValidationError("Token expired")
        
        from accounts.utils import verify_token_hash
        if not verify_token_hash(token, ev_token.token_hash):
            raise serializers.ValidationError("Invalid token")
        
        user.is_verified=True
        user.save()
        ev_token.delete()
        return attrs