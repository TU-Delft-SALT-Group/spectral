try:
    from beartype.claw import beartype_this_package

    beartype_this_package()
except ImportError:
    # in case beartype is not installed: running in production
    pass
