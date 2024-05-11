from pydantic import BaseModel
from router.usecase.shared import htmlname


class SelectOption(BaseModel):
    id: int
    selected: str = ""
    text: str = ""


class SelectForm(BaseModel):
    form_method: str = htmlname.FORMMETHOD.GET.value
    from_action: str = ""
    title: str
    input_name: str
    menu_list: list[SelectOption] = []
