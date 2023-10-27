import warnings


class AVDeprecationWarning(DeprecationWarning):
    pass


# DeprecationWarning is not printed by default (unless in __main__). We
# really want these to be seen, but also to use the "correct" base classes.
# So we're putting a filter in place to show our warnings. The users can
# turn them back off if they want.
warnings.filterwarnings("default", "", AVDeprecationWarning)
