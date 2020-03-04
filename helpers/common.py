
def redirect_to_correct_account(request, intended_account):
    try:
        if request.user.user_type == intended_account:
            return False
    except Exception:
        pass
    return True


def resolve_integrity_error_string(error_inst):
    ERRORS = (
        ('email', 'The email address is already in use by another account. Please provide another email address'),
        ('registration_number', 'The registration number is already in use by another account. Please provide your registration number correctly'),
        ('mobile', 'The mobile number is already in use by another account. Please provide your mobile number correctly')
    )
    for error in ERRORS:
        if error[0] in str(error_inst):
            return error[1]
    print(error_inst)
    return 'Something went wrong'
