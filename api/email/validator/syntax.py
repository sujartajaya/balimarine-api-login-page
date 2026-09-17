from email_validator import validate_email, EmailNotValidError

def check(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False