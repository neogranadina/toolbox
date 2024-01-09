class LegacyDbRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'hello':
            return 'legacy_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'hello':
            return 'legacy_db'
        return 'default'

    # ... (other methods)
