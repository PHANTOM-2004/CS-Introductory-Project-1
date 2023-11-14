from django.shortcuts import render, HttpResponse, redirect, reverse
from SwapVenues.models import UserVenueTime
from django import forms
from django.core.exceptions import ValidationError

CAMPUS_CHOICES = (
    (1, '四平'),
    (2, '嘉定'),
)
DAYS_OF_WEEK_CHOICES = (
    (1, '星期一'),
    (2, '星期二'),
    (3, '星期三'),
    (4, '星期四'),
    (5, '星期五'),
    (6, '星期六'),
    (7, '星期日'),
)


class VenueInfoAddForm(forms.Form):
    swap_start_time = forms.IntegerField(
        max_value=20,
        min_value=9,
        label="交换场地起始时间-24小时制",
        widget=forms.NumberInput(
            attrs={
                'required': 'required',
                "class": "form-control",
                "placeholder": "请输入场地起始时间"
            }
        )
    )
    swap_end_time = forms.IntegerField(
        max_value=21,
        min_value=10,
        label="交换场地终止时间-24小时制",
        widget=forms.NumberInput(
            attrs={
                'required': 'required',
                "class": "form-control",
                "placeholder": "请输入场地终止时间"
            }
        )
    )

    swap_campus = forms.ChoiceField(
        label="交换场地校区",
        choices=CAMPUS_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "form-check-input",
                # choices=CAMPUS_CHOICES
            }
        ),
    )
    swap_day_of_week = forms.ChoiceField(
        choices=DAYS_OF_WEEK_CHOICES,
        label="交换场地星期*",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                'required': 'required'
            }
        )
    )

    campus = forms.ChoiceField(
        label="我的场地校区",
        choices=CAMPUS_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "form-check-input",
                # choices=CAMPUS_CHOICES
            }
        ),
    )
    day_of_week = forms.ChoiceField(
        choices=DAYS_OF_WEEK_CHOICES,
        label="我的场地星期*",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                'required': 'required'
            }
        )
    )
    venue_id = forms.IntegerField(
        max_value=6,
        min_value=1,
        label="输入我的场地号 (129小场地1,2号续为5,6号)",
        widget=forms.NumberInput(
            attrs={
                'required': 'required',
                "class": "form-control",
                "placeholder": "请输入我的场地号"
            }
        )
    )
    venue_time = forms.IntegerField(
        max_value=20,
        min_value=9,
        label="我的场地起始时间-24小时制(单场)",
        widget=forms.NumberInput(
            attrs={
                'required': 'required',
                "class": "form-control",
                "placeholder": "请输入我的场地时间"
            }
        )
    )

    def clean_swap_end_time(self):
        swap_start_time = self.cleaned_data.get("swap_start_time")
        swap_end_time = self.cleaned_data.get("swap_end_time")
        if (not swap_start_time) or (int(swap_start_time) >= int(swap_end_time)):
            raise ValidationError("终止时间应当大于起始时间，请重新输入")
        return swap_end_time

    def clean_venue_id(self):
        campus = self.cleaned_data.get("campus")
        venue_id = self.cleaned_data.get("venue_id")
        # print("haode", campus, venue_id)
        if int(campus) == 2 and int(venue_id) >= 5:
            print("haode", campus, venue_id, "raise")
            raise ValidationError("嘉定校区只有四个场地")
        return venue_id


def addinfo(request, tongji_campus):
    if request.method == "GET":
        form = VenueInfoAddForm()
        return render(request, "venue_edit.html",
                      {"form": form, "msg": "添加"})
    form = VenueInfoAddForm(data=request.POST)
    if form.is_valid():
        swap_start_time = form.cleaned_data['swap_start_time']
        swap_end_time = form.cleaned_data['swap_end_time']
        swap_day_of_week = form.cleaned_data['swap_day_of_week']
        swap_campus = form.cleaned_data['swap_campus']

        venue_time = form.cleaned_data['venue_time']
        venue_id = form.cleaned_data['venue_id']
        day_of_week = form.cleaned_data['day_of_week']
        campus = form.cleaned_data['campus']

        info_dict = request.session.get("info")
        cur_user = info_dict['stu_id']
        # print(start_time, end_time, venue_id, day_of_week, campus)

        CurQset = UserVenueTime.objects.filter(
            stu_id=cur_user, venue_id=venue_id,
            campus=campus, venue_time=venue_time,
            day_of_week=day_of_week,

            swap_day_of_week=swap_day_of_week,
            swap_campus=swap_campus,
            swap_venue_time_start=swap_start_time,
            swap_venue_time_end=swap_end_time,
        )
        if len(CurQset) == 0:
            UserVenueTime.objects.create(
                stu_id=cur_user, venue_id=venue_id,
                campus=campus, venue_time=venue_time,
                day_of_week=day_of_week,

                swap_day_of_week=swap_day_of_week,
                swap_campus=swap_campus,
                swap_venue_time_start=swap_start_time,
                swap_venue_time_end=swap_end_time,
            )
        else:
            pass
        return redirect("/siping" if tongji_campus == 1 else "/jiading")
    return render(request, "venue_edit.html", {"form": form, "msg": "添加"})


def addvenu_jiading(request):
    return addinfo(request, 2)


def addvenu_siping(request):
    return addinfo(request, 1)


def match_list(request):
    info_dict = request.session.get("info")
    # print(info_dict)
    pass


def delete_info(request, prefix, nid):
    # delete
    url = '/' + prefix + '/'
    UserVenueTime.objects.filter(id=nid).delete()
    # print(url)
    return redirect(url)


def edit_info(request, prefix, nid):
    # delete
    if request.method == "GET":
        cur = UserVenueTime.objects.filter(id=nid).first()
        # print(cur)
        form = VenueInfoAddForm(
            initial={
                'venue_time': cur.venue_time,
                'day_of_week': cur.day_of_week,
                'venue_id': cur.venue_id,
                'campus': cur.campus,

                'swap_start_time': cur.swap_venue_time_start,
                'swap_end_time': cur.swap_venue_time_end,
                'swap_day_of_week': cur.swap_day_of_week,
                'swap_campus': cur.swap_campus,
            }
        )
        return render(request, "venue_edit.html", {"form": form, "msg": "编辑"})
    # UserVenueTime.objects.filter(id=nid).update()
    form = VenueInfoAddForm(data=request.POST)
    if form.is_valid():
        UserVenueTime.objects.filter(id=nid).update(
            venue_id=form.cleaned_data['venue_id'],
            venue_time=form.cleaned_data['venue_time'],
            campus=form.cleaned_data['campus'],
            day_of_week=form.cleaned_data['day_of_week'],

            swap_venue_time_start=form.cleaned_data['swap_start_time'],
            swap_venue_time_end=form.cleaned_data['swap_end_time'],
            swap_campus=form.cleaned_data['swap_campus'],
            swap_day_of_week=form.cleaned_data['swap_day_of_week'],
        )
        url = '/' + prefix + '/'
        return redirect(url)
    else:
        return render(request, "venue_edit.html", {"form": form, "msg": "编辑"})
