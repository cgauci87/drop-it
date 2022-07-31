var apiBaseUrl = "https://5500-cgauci87-dropit-yzj1t7isrwm.ws-eu54.gitpod.io/";
var userRegistrationUrl = apiBaseUrl + "/users/registration/";
var userLoginUrl = apiBaseUrl + "/users/sign-in/";
var productUrl = apiBaseUrl + "/products/";


// COOKIES

function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  let expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}



// END COOKIES




function registerUser() {
    var $inputs = $('#user-registrations-form :input');
    var data = {};
    $inputs.each(function() {
        data[this.name] = $(this).val();
    });
    $.ajax({
        url: userRegistrationUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        async: false,
        success: function(resp){
            console.log(resp);
            // showing response message
            alert(resp.message);
            // redirect to login page

            window.location.href = "login.html";
            return false;
        },
        error: function(resp){
            console.log(resp);
            alert(resp.message);
        }
    });
}

function loginUser() {
    var $inputs = $('#user-login-form :input');
    var data = {};
    $inputs.each(function() {
        data[this.name] = $(this).val();
    });
    $.ajax({
        url: userLoginUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        async: false,
        success: function(resp){
            console.log(resp);
            // showing response message
            token = resp.payload.token;
            console.log(token);
            // save token in local storage
//            window.localStorage.setItem("token", token);
            setCookie("token", token, 365)
            alert(resp.message);
            // redirect to login page
            window.location.href = "layout.html";
            return false;
        },
        error: function(xhr, status, error) {
          var err = eval("(" + xhr.responseText + ")");
          alert(err.message);
        }
    });
}

function get_all_products_for_user(){
    var token = getCookie("token");
    var headers = {
        'Authorization': 'Token ' + token
    };
    $.ajax({
        url: productUrl,
        type: 'GET',
        contentType: 'application/json',
        dataType: 'json',
        headers: headers,
        async: false,
        success: function(resp){
            console.log(resp);
            // showing response message
            payload = resp.payload;
            console.log(payload);
            for (var i = 0; i < payload.length; i++) {
                $('#news-slider').append('<div class="post-slide"> <div class="post-img"><img src="assets/images/reishi.webp" alt="Reishi Mushrooms" /> <a href="#" class="over-layer"><i class="fa fa-link"></i></a></div><div class="post-content"><h3 class="post-title"><a href="#">'+ payload[i].title +'</a></h3><p class="post-description">'+ payload[i].description +'</p><a id="reveal-click" class="read-more">Reviews</a></div></div>');
            }
        },
        error: function(resp){
            console.log(resp);
            return []
        }
    });
}
