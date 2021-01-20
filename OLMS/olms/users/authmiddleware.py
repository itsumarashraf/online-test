from django.shortcuts import redirect
def userlogin_auth(get_response):
    # One-time configuration and initialization.

    def middleware(request):
         # Code to be executed for each request before the view (and later middleware) are called.
        
        if  not request.session.get('userlogged'):
            return redirect('userlogin')

        response = get_response(request)

        # Code to be executed for each request/response after the view is called.

        return response

    return middleware