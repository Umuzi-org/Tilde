# from logging import StringTemplateStyle
# from typing import NamedTuple
from django.db import models
from model_mixins import Mixins
from collections import namedtuple


class NameSpace(
    models.Model,
    Mixins,
):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_value(self, name):
        instance = Value.objects.get(name=name, namespace=self)
        return instance.get()

    @classmethod
    def get_config(Klass, namespace: str):
        """all the configuration in this namespace as a namedtuple"""
        try:
            instance = Klass.objects.get(name=namespace)
        except Klass.DoesNotExist:
            print(f"namespace = {namespace}")
            raise
        values = Value.objects.filter(namespace=instance)
        name_value_pairs = [(value.name, value.get()) for value in values]

        ConfigOptions = namedtuple(
            f"ConfigOptions",
            " ".join([name for name, _ in name_value_pairs]),
        )
        args = [value for _, value in name_value_pairs]
        return ConfigOptions(*args)


class Value(
    models.Model,
    Mixins,
):
    INTEGER = "i"
    STRING = "s"
    BOOLEAN = "b"

    DATATYPE_CHOICES = [(INTEGER, "integer"), (STRING, "string"), (BOOLEAN, "boolean")]

    namespace = models.ForeignKey(NameSpace, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    value = models.TextField()
    datatype = models.CharField(max_length=1, choices=DATATYPE_CHOICES)
    repeated = models.BooleanField()

    def __str__(self):
        return f"{self.namespace}: {self.name} = {self.get()}"

    def get(self):
        value = self.value.strip()
        if self.repeated:
            values = [s.strip() for s in value.split("\n")]
            return [self.parse(value) for value in values]
        else:
            return self.parse(value)

    def parse(self, x):
        """convert the string x into the correct type"""
        if self.datatype == self.INTEGER:
            return int(x)
        if self.datatype == self.STRING:
            return x
        if self.datatype == self.BOOLEAN:
            x = x.lower()
            if x in ["true", "1"]:
                return True
            if x in ["false", "0"]:
                return False
            raise ValueError(f"invalid boolean value: {x}")

        raise ValueError(f"unhandled datatype: {self.datatype}")
