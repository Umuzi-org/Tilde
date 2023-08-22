class _BaseException(Exception):
    def __init__(self, message, project_uri, clone_dir_path, self_test, config) -> None:
        full_message = f"{message}\nproject_uri: {project_uri}\nclone_dir_path: {clone_dir_path}\nself_test: {self_test}\nconfig: {config}"
        super().__init__(full_message)


class SystemError(_BaseException):
    """There is an error in the marker system, it's not something wrong with the code being marked"""


# class ProjectError(_BaseException):
#     """There is an error with the project being marked"""
#     def __init__(self, message, project_uri, clone_dir_path, self_test, config, fail_fast) -> None:
#         full_message = f"{message}\nproject_uri: {project_uri}\nclone_dir_path: {clone_dir_path}\nself_test: {self_test}\nconfig: {config}\nfail_fast: {fail_fast}"
#         super().__init__(full_message)


# class NotYetCompetentError(_BaseException):
#     """The project is not yet competent"""


# class RedFlagError(_BaseException):
#     """The project is not yet competent"""
