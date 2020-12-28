from core.models import Curriculum



CURRICULUM_SHORT_NAME_DS_PRE_BOOT = "data sci prebootcamp"
CURRICULUM_SHORT_NAME_DS_BOOT = "data sci boot"
CURRICULUM_SHORT_NAME_WEB_PRE_BOOT = "web dev pre boot"
CURRICULUM_SHORT_NAME_WEB_BOOT = "web dev boot"

DEPT_WEB = "Web Development"
DEPT_DS = "Data Science"


def data_science_curriculums():
    return [
        Curriculum.objects.get(short_name=CURRICULUM_SHORT_NAME_DS_PRE_BOOT),
        Curriculum.objects.get(short_name=CURRICULUM_SHORT_NAME_DS_BOOT),
    ]


def web_dev_curriculums():
    return [
        Curriculum.objects.get(short_name=CURRICULUM_SHORT_NAME_WEB_PRE_BOOT),
        Curriculum.objects.get(short_name=CURRICULUM_SHORT_NAME_WEB_BOOT),
    ]


data_science_curriculums = data_science_curriculums()
web_dev_curriculums = web_dev_curriculums()
