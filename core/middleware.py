from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from core.views import send_otp_code

class MobileVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            user_profile = request.user.profile

            # Check if the user has verified their mobile number
            if user_profile.phone and not user_profile.is_mobile_verified and request.path not in [reverse('core:verify_mobile_number'),reverse('account_logout')] and not request.path.startswith('/admin/'):
                send_otp_code(request)
                return redirect('core:verify_mobile_number')
            else:
                if not user_profile.phone:
                    messages.error(request,'No mobile number found !! \n Please contact Administrator !!')
                    logout(request)
        return response
