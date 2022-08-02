var apiBaseUrl = "https://8000-cgauci87-dropit-tikws9w3u3u.ws-eu54.gitpod.io";
var userRegistrationUrl = apiBaseUrl + "/users/registration/";
var userLoginUrl = apiBaseUrl + "/users/sign-in/";
var productUrl = apiBaseUrl + "/products/";
var writeAreviewUrl = apiBaseUrl + "/products/user-review";

// COOKIES

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
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
    $inputs.each(function () {
        data[this.name] = $(this).val();
    });
    $.ajax({
        url: userRegistrationUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        async: false,
        success: function (resp) {
            console.log(resp);
            // showing response message
            alert(resp.message);
            // redirect to login page

            window.location.href = "login.html";
            return false;
        },
        error: function (resp) {
            console.log(resp);
            alert(resp.message);
        }
    });
}

function loginUser() {
    var $inputs = $('#user-login-form :input');
    var data = {};
    $inputs.each(function () {
        data[this.name] = $(this).val();
    });
    $.ajax({
        url: userLoginUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        async: false,
        success: function (resp) {
            console.log(resp);
            // showing response message
            token = resp.payload.token;
            console.log(token);
            // save token in local storage
            setCookie("token", token, 365) // The token will be stored in the cookies
            alert(resp.message);
            // redirect to login page
            window.location.href = "layout.html";
            return false;
        },
        error: function (xhr, status, error) {
            var err = eval("(" + xhr.responseText + ")");
            alert(err.message);
        }
    });
}
// To pull data related to products , all mushroom types.
function get_all_products_for_user() {
    var token = getCookie("token");
    var headers = {
        'Authorization': 'Token ' + token //Authentication - to verify the user login using token from cookies and provide security for the API
    };
    $.ajax({ //using AJAX
        url: productUrl,
        type: 'GET',
        // contentType, dataType & headers are used to call the API , js
        contentType: 'application/json',
        dataType: 'json',
        headers: headers,
        async: false,
        success: function (resp) {
            console.log(resp);
            // showing response message
            payload = resp.payload;
            console.log(payload);
            for (var i = 0; i < payload.length; i++) {
                $('#news-slider').append('<div class="post-slide"> <div class="post-img"><img src="assets/images/reishi.webp" alt="Reishi Mushrooms" /> <a href="#" class="over-layer"><i class="fa fa-link"></i></a></div><div class="post-content"><h3 class="post-title"><a href="#">' + payload[i].title + '</a></h3><p class="post-description">' + payload[i].description + '</p><a id="reveal-click" class="read-more">Reviews</a></div></div>');
                $('#write_review_product_dropdown').append('<option value="' + payload[i].id + '">' + payload[i].title + '</option>');
            }
        },
        error: function (resp) {
            console.log(resp);
            return []
        }
    });
}

function write_a_review() {
    var token = getCookie("token");
    var headers = {
        'Authorization': 'Token ' + token
    };
    var $inputs = $('#write-a-review-form:input');
    var data = {};
    $inputs.each(function () {
        data[this.name] = $(this).val();
    });
    data.rating = getCookie("rating"); // Get the rating from the cookie data
    console.log(data);
     $.ajax({
        url: writeAreviewUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        headers: headers,
        async: false,
        success: function (resp) {
            console.log(resp);
            // showing response message
            alert(resp.message);
            // redirect to login page
            return false;
        },
        error: function (resp) {
            console.log(resp);
            alert(resp.message);
        }
    });
}


function save_rating(value){
    setCookie("rating", value, 365);
}