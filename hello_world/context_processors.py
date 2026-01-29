"""
Custom context processors for Neudebri HMIS
"""


def auth_pages(request):
    """Add show_content_always flag for auth pages"""
    show_content_always = False
    
    # Check if current page is a login or signup page
    path = request.path
    if 'accounts/login' in path or 'accounts/signup' in path or 'accounts/password' in path:
        show_content_always = True
    
    return {
        'show_content_always': show_content_always
    }
