from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View



from .forms import LoginForm, UserActivityForm
from .models import UserActivity

User = get_user_model()


class UsersActivityView(View):
    def get(self, request, *args, **kwargs):
        #print(UserActivity.objects.all().count())
        #print(UserActivity.objects.all().today().count())
        query = request.GET.get("q")
        users = User.objects.all()
        checked_in = []
        checked_out = []
        unknown = []
        all_activity  =UserActivity.objects.all()
        for u in users:
            act = all_activity.filter(user=u).today().recent()
            #act = u.useractivity_set.all().today()
            if act.exists():
                current_user_obj = act.first()
                if current_user_obj.activity == 'checkin':
                    checked_in.append(current_user_obj.id)
                else:
                    checked_out.append(current_user_obj.id)
            else:
                unknown.append(u)
            
        queryset_checkedin = UserActivity.objects.filter(id__in=checked_in)
        queryset_checkedout = UserActivity.objects.filter(id__in=checked_out)
        all_activity = all_activity.today().recent()

        if query:
            queryset_checkedin=queryset_checkedin.filter(user__username__iexact=query)
            queryset_checkedout=queryset_checkedout.filter(user__username__iexact=query)
            all_activity=all_activity.filter(
                Q(user__username__iexact=query) |
                Q(user__first_name__iexact=query)
            )
        context = {
            "queryset_checkedin":queryset_checkedin,
            "queryset_checkedout":queryset_checkedout,
            "inactive_users": unknown,
            "all_activity": all_activity,
            "query":query,
        }
        return render(request, "timeclock/users-activity-view.html", context)


# LOGIN REQUIRED
class ActivityView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login/")
        username_ses=None
        username_auth=None
        if request.session.get("username"):
            username_auth = request.user.username
            username_ses = request.session.get("username")
        if username_ses == username_auth:
            username = username_auth
            context = {}
            if username:
                form = UserActivityForm(initial={"username": username})
                context["form"] = form
                if request.user.is_authenticated:
                    obj = UserActivity.objects.current(request.user)
                    context['object'] = obj
        else:
            logout(request)
            return HttpResponseRedirect("/login/")
        return render(request, "timeclock/activity-view.html", context)

    def post(self, request, *args, **kwargs):
        form = UserActivityForm(request.POST)
        obj = UserActivity.objects.current(request.user)
        context = {"form": form, "object": obj}
        if form.is_valid():
            toggle = UserActivity.objects.toggle(request.user)
            context['object'] = toggle            
            return HttpResponseRedirect("/")
        return render(request, "timeclock/activity-view.html", context)


class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "timeclock/login-view.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
            return HttpResponseRedirect("/")
        context = {"form": form}
        return render(request, "timeclock/login-view.html", context)



class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/")


# Django Class Based Views http://joincfe.com/projects
def activity_view(request, *args, **kwargs):
    # get
    if request.method == 'POST':
        # post 
        new_act = UserActivity.objects.create(user=request.user, activity='checkin')
    return render(request, "timeclock/activity-view.html", {})