import sysconfig
free_threaded_build = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))
assert isinstance(free_threaded_build, bool)
