__author__ = 'Dell'

class Ewallet_Router(object):
    """A router to control all database operations on models in
    the myapp application"""

    def db_for_read(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'ewallet':
            return 'ewallet'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'ewallet':
            return 'ewallet'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        if obj1._meta.app_label == 'ewallet' or obj2._meta.app_label == 'ewallet':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the myapp app only appears on the 'other' db"
        if db == 'ewallet':
            return model._meta.app_label == 'ewallet'
        elif model._meta.app_label == 'ewallet':
            return False
        return None




class Bank_1_Router(object):
    """A router to control all database operations on models in
    the myapp application"""

    def db_for_read(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'bank_1':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'bank_1':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        if obj1._meta.app_label == 'bank_1' or obj2._meta.app_label == 'bank_1':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the myapp app only appears on the 'other' db"
        if db == 'default':
            return model._meta.app_label == 'bank_1'
        elif model._meta.app_label == 'bank_1':
            return False
        return None


class Bank_2_Router(object):
    """A router to control all database operations on models in
    the myapp application"""

#    def db_for_read(self, model, **hints):
#        "Point all operations on myapp models to 'other'"
#        if model._meta.app_label == 'bank_2':
#            return 'bank_2'
#        return None
#
#    def db_for_write(self, model, **hints):
#        "Point all operations on myapp models to 'other'"
#        if model._meta.app_label == 'bank_2':
#            return 'bank_2'
#        return None

    def db_for_read(self, model, **hints):
        "Point all operations on app1 models to 'app1'"
        from django.conf import settings
        if not settings.DATABASES.has_key('bank_2'):
            return None
        if model._meta.app_label == 'bank_2':
            return 'bank_2'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on app1 models to 'app1'"
        from django.conf import settings
        if not settings.DATABASES.has_key('bank_2'):
            return None
        if model._meta.app_label == 'bank_2':
            return 'bank_2'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        if obj1._meta.app_label == 'bank_2' or obj2._meta.app_label == 'bank_2':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the myapp app only appears on the 'other' db"
        if db == 'bank_2':
            return model._meta.app_label == 'bank_2'
        elif model._meta.app_label == 'bank_2':
            return False
        return None
