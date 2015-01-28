$(function(){
        var OAUTHURL    =   'https://accounts.google.com/o/oauth2/auth?';
        var VALIDURL    =   'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=';
        var SCOPE       =   'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email';
        var CLIENTID    =   '895498739295-6umne92gah6gvkc3j3q1mmfo5ggabmpn.apps.googleusercontent.com';
        var REDIRECT    =   'http://localhost:5000/oauth2callback'
        var LOGOUT      =   'http://accounts.google.com/Logout';
        var TYPE        =   'token';
        var _url        =   OAUTHURL + 'scope=' + SCOPE + '&client_id=' + CLIENTID + '&redirect_uri=' + REDIRECT + '&response_type=' + TYPE;
        var acToken;
        var tokenType;
        var expiresIn;
        var user;
        var loggedIn    =   false;

        function login() {
            var win         =   window.open(_url, "windowname1", 'width=800, height=600'); 
            var pollTimer   =   window.setInterval(function() { 
                try {
                    console.log(win.document.URL);
                    if (win.document.URL.indexOf(REDIRECT) != -1) {
                        window.clearInterval(pollTimer);
                        var url =   win.document.URL;
                        acToken =   gup(url, 'access_token');
                        tokenType = gup(url, 'token_type');
                        expiresIn = gup(url, 'expires_in');
                        win.close();

                        validateToken(acToken);
                    }
                } catch(e) {
                }
            }, 500);
        }

        function validateToken(token) {
            $.ajax({
                url: VALIDURL + token,
                data: null,
                success: function(responseText){  
                    getUserInfo();
                    loggedIn = true;
                },  
                dataType: "jsonp"  
            });
        }

        function getUserInfo() {
            $.ajax({
                url: 'https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + acToken,
                data: null,
                success: function(resp) {
                    user = resp;
                    console.log(user);
                    redirectLogin(user)
                },
                dataType: "jsonp"
            });
        }

        function redirectLogin(user){
                parameters = {'id':user.id, 'name':user.name}
                $.getJSON("/login/", parameters,function(data){
                        location.href="/profile"
                })
        }

        //credits: http://www.netlobo.com/url_query_string_javascript.html
        function gup(url, name) {
            name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
            var regexS = "[\\#&]"+name+"=([^&#]*)";
            var regex = new RegExp( regexS );
            var results = regex.exec( url );
            if( results == null )
                return "";
            else
                return results[1];
        }

        function startLogoutPolling() {
            loggedIn = false;
            redirectLogout()
        }
        function redirectLogout(){
           $.getJSON("/logout", function(data){
                location.href = "/"
           })
        }
        $("a.login").click(function(){
            login()
        })
        $("a.logout").click(function(){
            location.href = 'http://accounts.google.com/Logout'
            startLogoutPolling()
        })
})