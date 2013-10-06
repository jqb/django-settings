# -*- coding: utf-8 -*-
from .. import DBTestCase


BUILTIN_TYPE_NAMES = ['Integer', 'Email', 'PositiveInteger', 'String']


class DjangoSettingsAdminTest(DBTestCase):
    def create_user(self, username, password=None, is_staff=False, is_admin=False):
        from django.contrib.auth.models import User

        user, created = User.objects.get_or_create(
            username=username,
            email="%s@example.com" % username,
            is_superuser=is_admin,
        )
        user.is_staff = is_staff
        user.set_password(password)
        user.save()

        return user

    def login(self, user, password):
        self.client.login(username=user.username, password=password)

    def setup(self):
        from django.test import Client
        self.admin = self.create_user("admin", "admin", is_staff=True, is_admin=True)
        self.client = Client()
        self.login(self.admin, "admin")

    def test_admin_settings_list(self):
        from django_settings import admin as django_settings_admin
        import django_settings
        import django

        # set some data
        data = [
            ("Integer", "test-int", 1),
            ("String", "test-str", "Value"),
            ("Email", "test-email", "admin@admin.com"),
        ]

        def set_all_data():
            for type_name, name, value in data:
                django_settings.set(type_name, name, value)

        self.assert_queries_count(len(data) * 4, set_all_data)
        # end

        # run request and check number of quesries
        def run_request():
            return self.client.get('/admin/django_settings/setting/')

        expected_queries = sum([
            1 if django.get_version() == '1.3' else 0,  # auth_messages (gone for ver > 1.3)
            1,  # auth_user
            1,  # session
            1,  # number of settings
            1,  # names of settings
        ])

        response = self.assert_queries_count(expected_queries, run_request)
        # end

        ctx = response.context
        self.assert_true('cl' in ctx)

        change_list = ctx['cl']
        self.assert_true(isinstance(change_list, django_settings_admin.ChangeList))
        self.assert_items_equal(
            change_list.available_settings_models,
            BUILTIN_TYPE_NAMES,
        )

    def test_create_settings_get(self):
        # First check if 404 is raise when there's no 'typename'
        response = self.client.get('/admin/django_settings/setting/add/', follow=True)
        self.assert_equal(response.status_code, 404)

        for btype in BUILTIN_TYPE_NAMES:
            response = self.client.get('/admin/django_settings/setting/add/?typename=%s' % btype)
            self.assert_equal(response.status_code, 200)

    def test_create_settings_post_should_contain_errors(self):
        for btype in BUILTIN_TYPE_NAMES:
            response = self.client.post('/admin/django_settings/setting/add/?typename=%s' % btype)
            adminform = response.context['adminform']

            self.assert_equal(response.status_code, 200)
            self.assert_equal(adminform.form.errors, {
                'name': [u'This field is required.'],
                'value': [u'This field is required.'],
            })

    def test_create_settings_post_should_work_just_fine(self):
        def create_setting(btype, name, value, params=None):
            data = dict(params or {})
            data.update(
                name=name,
                value=value,
            )
            return self.client.post('/admin/django_settings/setting/add/?typename=%s' % btype,
                                    data, follow=True)

        def test_all_save_button_cases(btype, value):
            resp = create_setting(btype, 'test-%s-1' % btype, value, {'_continue': True})
            self.assert_equal(resp.status_code, 200)
            self.assert_equal(resp.context['adminform'].form.errors, {})

            resp = create_setting(btype, 'test-%s-2' % btype, value, {'_addanother': True})
            self.assert_equal(resp.status_code, 200)
            self.assert_equal(resp.context['adminform'].form.errors, {})

            resp = create_setting(btype, 'test-%s-3' % btype, value, {'_save': True})
            self.assert_equal(resp.status_code, 200)
            self.assert_equal(resp.redirect_chain, [
                ('http://testserver/admin/django_settings/setting/', 302),
            ])

        test_all_save_button_cases('Integer', '123')
        test_all_save_button_cases('String', 'test string value')
        test_all_save_button_cases('Email', 'admin@admin.com')
        test_all_save_button_cases('PositiveInteger', '123123')
