class CustomMeta(type):

    def __new__(cls, name, bases, classdict):
        new_classdict = {}
        for key, value in classdict.items():
            if not (key.startswith("__") and key.endswith("__")):
                new_key = f"custom_{key}"
                new_classdict[new_key] = value
            else:
                new_classdict[key] = value

        adjusted_custom_class = super().__new__(cls, name, bases, new_classdict)

        original_setattr = adjusted_custom_class.__setattr__
        original_getattribute = adjusted_custom_class.__getattribute__

        def __setattr__(self, title, argument):
            if title.startswith("__") and title.endswith("__"):
                original_setattr(self, title, argument)
            elif title.startswith("custom_"):
                original_setattr(self, title, argument)
            else:
                custom_name = f"custom_{title}"
                original_setattr(self, custom_name, argument)

        def __getattribute__(self, title):
            if title.startswith("__") and title.endswith("__"):
                return original_getattribute(self, title)
            if title.startswith("custom_"):
                return original_getattribute(self, title)
            raise AttributeError(
                f"'{type(self).__name__}' не содержит "
                f"атрибута "
                f"'{title}'"
            )

        adjusted_custom_class.__setattr__ = __setattr__
        adjusted_custom_class.__getattribute__ = __getattribute__

        return adjusted_custom_class
