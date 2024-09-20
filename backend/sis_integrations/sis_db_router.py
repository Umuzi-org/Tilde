class SISDBRouter:
    """
    A router to control all database operations on models in the
    sis_integrations application.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "sis_integrations":
            return "sis_db"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "sis_integrations":
            return "sis_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == "sis_integrations"
            or obj2._meta.app_label == "sis_integrations"
        ):
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "sis_integrations":
            return db == "sis_db"
        return False
