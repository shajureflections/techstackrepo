from app_constants import AppConstants
from string_table import AppMessages
from structlogconfig import log_config

logdata = log_config()


class AppResponse(dict):
    def __init__(
        self,
        code_param=AppConstants.CODE_INTERNAL_SERVER_ERROR,
        data_param={},
        message_param=AppMessages.FAILED,
        status_param=AppMessages.FALSE,
    ):
        dict.__init__(
            self,
            code=code_param,
            data=data_param,
            message=message_param,
            status=status_param,
        )

    def set_response(self, code_param, data_param, message_param, status_param):
        self["code"] = code_param
        self["data"] = data_param
        self["message"] = message_param
        self["status"] = status_param
        if code_param == 200:
            try:
                if "User is created with given name" in data_param.get("Success"):
                    data_param = data_param.get("Success").split("Generated")[0]
                elif "User is loggedinn" in data_param.get("Success"):
                    data_param = data_param.get("Success").split("and token")[0]
            except:
                pass
            logdata.info(data_param, message=message_param, status_code=status_param)
        else:
            logdata.error(data_param, message=message_param, status_code=status_param)
