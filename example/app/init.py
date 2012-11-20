# -*- coding: utf-8 -*-
"""
Web app initial data, usage from main project directory::

    $> python -m apps.init
"""

def load_users():
    from django.contrib.auth.models import User

    admin, created = User.objects.get_or_create(
        username = "admin",
        email = "admin@admin.com",
        is_superuser = True,
    )
    admin.is_staff = True
    admin.set_password("admin")
    admin.save()

    return dict(
        admin = admin,
    )


def load():
    load_users()


if __name__ == '__main__':
    import manage; manage.setup()
    load()
