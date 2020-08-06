ifndef MK_VARS_APP
MK_VARS_APP=1

include make/env.Makefile
include make/vars.app.*.Makefile

ifdef INSIDE_CI
# This overrides the previous value
APP_ENV=test
endif

endif
