def test_admin_login(user):
    if not user.is_authenticated():
        return False
    if not user.is_superuser:
        return False
    return True
