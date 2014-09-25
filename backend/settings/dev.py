from .common import Common


class Dev(Common):
    DEBUG = True

    PIPELINE_ENABLED = False
    PIPELINE_DISABLE_WRAPPER = True
