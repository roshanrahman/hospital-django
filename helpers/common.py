
def redirect_to_correct_account(request, intended_account):
    try:
        if request.user.user_type == intended_account:
            return False
    except Exception:
        pass
    return True
