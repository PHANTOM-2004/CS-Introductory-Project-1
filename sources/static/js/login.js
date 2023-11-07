//一来就判断是否登陆如果登陆了导航条变化
function checkLoginStatus() {
  if (localStorage.getItem("loginjudge") == 1) {
    $("#username_c").text(localStorage.getItem("username"));
    //去掉login
    $("#userlogin").addClass("hide");
  }
}
// 手动显示模态框
$("#userlogin").on("click", function () {
  $("#myModal").modal("show");
});

$("#myModal").on("click", function () {
  // 在这里执行关闭模态框的操作
  // 例如，可以执行 Login() 函数，然后关闭模态框
  Login();
  $("#myModal").modal("hide");
});
function Login() {
  event.preventDefault(); // 阻止表单的默认提交行为
  //获取用户写入内容:姓名 密码 微信
  var username = $("#username").val();
  var password = $("#password").val();
  var weixin = $("#weixin").val();

  //加判断条件是否密码正确，有没有用户信息，是否需要注册
  // if(){};
  // 存储用户信息到本地存储
  localStorage.setItem("username", username);
  localStorage.setItem("password", password);
  localStorage.setItem("weixin", weixin);
  localStorage.setItem("loginjudge", 1);
  //加入到username_login里面
  $("#username_c").text(username);

  //去掉login
  $("#userlogin").addClass("hide");

  // 清空输入框
  $("#username").val("");
  $("#password").val("");
  $("#weixin").val("");
  $(".btn-default[data-dismiss='modal']").trigger("click");
}

// 退出登陆
function Logout() {
  //加入到username_login里面
  $("#username_c").text("请先登录");
  //去掉login
  $("#userlogin").removeClass("hide");
  localStorage.clear();
  window.location.href = "/index.html";
}

function navigateToPage(page) {
  // 检查本地存储中是否登陆
  if (localStorage.getItem("loginjudge") == 1) {
    // 用户已登录，可以跳转到指定页面
    window.location.href = page;
  } else {
    // 用户未登录，显示提示框
    alert("请先登录");
  }
}
