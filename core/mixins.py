from django.shortcuts import render
from django.contrib import messages

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'admin':
            return render(request, 'error/page-not-authorized.html', status=403)
        return super().dispatch(request, *args, **kwargs)

class EmployeeRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'employee':
            return render(request, 'error/page-not-authorized.html', status=403)
        return super().dispatch(request, *args, **kwargs)

class ResidentRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'resident':
            return render(request, 'error/page-not-authorized.html', status=403)
        return super().dispatch(request, *args, **kwargs)
