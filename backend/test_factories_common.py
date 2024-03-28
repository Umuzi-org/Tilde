class FlavourMixin:
    @staticmethod
    def flavours(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.set_flavours(extracted)
        else:
            pass
