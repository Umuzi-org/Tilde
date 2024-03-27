import copy
import taggit
from typing import List


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


class FlavourMixin:
    def flavours_match(self, flavour_strings: List[str]):
        return sorted(self.flavour_names) == sorted(flavour_strings)

    def flavour_ids_match(self, flavour_ids: List[int]):
        return sorted([flavour.id for flavour in self.flavours.all()]) == sorted(
            flavour_ids
        )

    @property
    def flavour_names(self):
        return [o.name for o in self.flavours.all()]

    def set_flavours(self, flavour_strings):
        flavour_tags = [
            taggit.models.Tag.objects.get_or_create(name=name)[0]
            for name in flavour_strings
        ]

        for flavour in self.flavours.all():
            if flavour not in flavour_tags:
                self.flavours.remove(flavour)
        for tag in flavour_tags:
            if tag not in self.flavours.all():
                self.flavours.add(tag)
