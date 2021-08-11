import copy


class Mixins:
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    @classmethod
    def get_or_create_or_update(cls, defaults=None, overrides=None, **getkwargs):
        assert "default" not in getkwargs, "did you mean 'defaults'"
        assert "override" not in getkwargs, "did you mean 'overrides'"
        default_copy = copy.copy(defaults or {})
        default_copy.update(overrides or {})
        o, created = cls.objects.get_or_create(**getkwargs, defaults=default_copy or {})
        if (not created) and overrides:
            o.update(**overrides)
            o.save()
        return o, created
