from django.shortcuts import render

# Create your views here.
def dashboard(request):

    context = {

    }

    return render(request, 'template_dashboard/dashboard.html', context)
