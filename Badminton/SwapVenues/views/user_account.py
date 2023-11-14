from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from SwapVenues import models
from SwapVenues.tools.md5 import md5


class StudentForm(forms.Form):
    stu_id = forms.CharField(
        max_length=7,
        min_length=7,
        label="学号",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入学号"
            }
        )
    )
    pwd = forms.CharField(
        label="输入密码",
        max_length=32,
        min_length=12,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入密码"
            },
            render_value=True
        )  # 保证密码不置空
    )

    def clean_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        return md5(pwd)


def login(request):
    if request.method == "GET":
        form = StudentForm()
        return render(request, "login.html", {"form": form})
    form = StudentForm(data=request.POST)
    if form.is_valid():
        # form.save()
        # print(form.cleaned_data)
        # 去数据库校验
        # models.StudentInfo.objects.filter(username="",pwd=).first() //ok
        obj = models.UserInfo.objects.filter(
            stu_id=form.cleaned_data['stu_id'],
            pwd=form.cleaned_data['pwd']
        ).first()
        if not obj:
            form.add_error("pwd", "用户名或者密码错误")
            return render(request, "login.html", {"form": form})

        # 写入session
        request.session["info"] = {'stu_id': obj.stu_id, 'name': obj.name}
        return redirect('/')
    return render(request, "login.html", {"form": form})


class RegisterModelForm(forms.ModelForm):
    stu_id = forms.CharField(
        max_length=7,
        min_length=7,
        label="学号"
    )
    pwd = forms.CharField(
        label="设置密码",
        max_length=32,
        min_length=12,
        widget=forms.PasswordInput(render_value=True)  # 保证密码不置空
    )
    confirm_pwd = forms.CharField(
        label="确认密码",
        max_length=32,
        min_length=12,
        widget=forms.PasswordInput(render_value=True)  # 保证密码不置空
    )

    class Meta:  # 这里meta必须首字母大写
        model = models.UserInfo
        fields = ['stu_id', 'pwd', 'confirm_pwd', 'wechat_id', 'name']

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = "请输入" + field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": "请输入" + field.label
                }  # here no s

    # 按照顺序执行
    def clean_stu_id(self):
        stu_id = self.cleaned_data.get("stu_id")
        if models.UserInfo.objects.filter(stu_id=stu_id):
            raise ValidationError("该账户已存在")
        return stu_id

    def clean_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        # 密码加密
        # print(md5(pwd))
        return md5(pwd)

    def clean_confirm_pwd(self):
        confirm = md5(self.cleaned_data.get("confirm_pwd"))
        # print(confirm)
        pwd = self.cleaned_data.get("pwd")
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入")
        return confirm


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {"form": form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, "register.html", {"form": form})


def logout(request):
    request.session.clear()
    return redirect('/')
