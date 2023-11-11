from django.shortcuts import render
from SwapVenues import models

weekday = {1: '周一', 2: '周二', 3: '周三', 4: '周四', 5: '周五', 6: '周六', 7: '周日'}


# Create your views here.
def index(request):
    return render(request, "index.html")


class MatchUser:
    def __init__(self, name, wechat_id,
                 venue_time, day_of_week, campus_id, venue_id,
                 swap_venue_time_start, swap_venue_time_end, swap_day_of_week, swap_campus_id,
                 is_user, pri_key):
        # info
        self.name = name
        self.wechat_id = wechat_id
        # cur
        self.venue_id = venue_id
        self.campus = "四平" if campus_id == 1 else "嘉定"
        start_time = "{:02d}:00".format(venue_time)
        end_time = "{:02d}:00".format(venue_time + 1)
        self.venue_time = f"{start_time} - {end_time}"
        self.day_of_week = weekday[day_of_week]
        # swap
        self.swap_campus = "四平" if swap_campus_id == 1 else "嘉定"
        swap_start_time = "{:02d}:00".format(swap_venue_time_start)
        swap_end_time = "{:02d}:00".format(swap_venue_time_end)
        self.swap_venue_time = f"{swap_start_time} - {swap_end_time}"
        self.swap_day_of_week = weekday[swap_day_of_week]
        # auth
        self.is_user = is_user
        self.pri_key = pri_key


def show_list(request, Tongji_campus):
    info_dict = request.session.get("info")
    cur_user = info_dict['stu_id']
    camp_id = 2 if Tongji_campus == "嘉定" else 1
    cur_wechat_id = models.UserInfo.objects.get(stu_id=cur_user).wechat_id
    # 当前user拥有的camp_id的场地
    cur_user_set = models.UserVenueTime.objects.filter(stu_id=cur_user,campus=camp_id)
    match_list = []
    for venue in cur_user_set:
        match_list.append(
            MatchUser(
                info_dict['name'],cur_wechat_id,
                venue.venue_time,venue.day_of_week,venue.campus,venue.venue_id,
                venue.swap_venue_time_start,venue.swap_venue_time_end,venue.swap_day_of_week,venue.swap_campus,
                True, venue.id
            )
        )
    for venue in cur_user_set:
        # 符合想要换的场地
        now_match = models.UserVenueTime.objects.filter(
            # 对方场地符合venue的校区
            campus=venue.swap_campus,
            # 对方场地符合venue的期望区间
            venue_time__range=(venue.swap_venue_time_start, venue.swap_venue_time_end),
            # 对方场地符合周*
            day_of_week=venue.swap_day_of_week,

            # venue场地符合对方预期
            swap_campus=venue.campus,
            swap_venue_time_start__lte=venue.venue_time,
            swap_venue_time_end__gte=venue.venue_time,
            swap_day_of_week=venue.day_of_week,
        )
        for v in now_match:
            match_info = models.UserInfo.objects.filter(stu_id=v.stu_id).first()
            match_user = MatchUser(match_info.name, match_info.wechat_id,
                                   v.venue_time, v.day_of_week, v.campus, v.venue_id,
                                   v.swap_venue_time_start, v.swap_venue_time_end, v.swap_day_of_week, v.swap_campus,
                                   cur_user == v.stu_id, v.id)
            match_list.append(match_user)

    return render(request, "tongji_campus.html",
                  {'match_list': match_list, 'campus': Tongji_campus})


def show_siping(request):
    return show_list(request, "四平")


def show_jiading(request):
    return show_list(request, "嘉定")
