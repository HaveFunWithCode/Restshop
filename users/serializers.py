from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import ShopUser, CustomerProfile, Adress


# class AddressSerializer(serializers.ModelSerializer):
class AddressSerializer(serializers.ModelSerializer):


    class Meta:
        model=Adress
        fields='__all__'


class CustomerProfileSerializer(serializers.ModelSerializer):
    birthdate=serializers.DateField(required=False)
    adresses=serializers.SerializerMethodField()

    def get_adresses(self,obj):
        addreses=obj.user.adress_set.all()
        return AddressSerializer(addreses,read_only=True,many=True,context=self.context).data
    class Meta:
        model=CustomerProfile
        fields=('birthdate','adresses')


class LoginSerilizer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True, help_text='لطفا ایمیل به فرمت مناسب استفاده شود')
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    def validate(self, data):
        email=data.get('email')
        password=data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                raise serializers.ValidationError("چنین کاربری وجود ندارد")


        else:
            if not data.get('password'):
                raise serializers.ValidationError("لطفا فید پسورد را پر کنید!")
            elif not data.get('email'):
                raise serializers.ValidationError("لطفا ایمیل خود را وارد کنید")
        data['user']=user
        return data

    class Meta:
        model = ShopUser
        fields = ('email', 'password',)
        extra_kwargs = {'password':{'write_only':True}}




class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True, help_text='لطفا ایمیل به فرمت مناسب استفاده شود')
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    customerProfile = CustomerProfileSerializer(required=True)

    def validate_email(self, email):
        existed = ShopUser.objects.filter(email=email).first()
        if existed:
            raise serializers.ValidationError("شخص دیگری با همین ایمیل ثبت نام کرده است!")
        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("لطفا فید پسورد و تایید پسورد را پر کنید!")
        elif data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("پسوردها یکسان نیستند")
        return data

    def create(self, validated_data):
        user=ShopUser(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        if validated_data['customerProfile']!=None:
            profile_data = validated_data.pop('customerProfile')
            user.refresh_from_db()
            if 'birthdate' in profile_data:
                user.customerProfile.birth_date =profile_data['birthdate']
        return user

    class Meta:
        model = ShopUser
        fields = ('email', 'password','confirm_password', 'customerProfile',)
        # we don't want to get back the password in response
        extra_kwargs = {'password':{'write_only':True}}


