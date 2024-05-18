from pydantic import BaseModel
from . import htmlname


class SelectOption(BaseModel):
    id: int
    selected: str = ""
    text: str = ""


class Select(BaseModel):
    title: str
    input_name: str
    menu_list: list[SelectOption] = []


class Form(BaseModel):
    method: str = htmlname.FORMMETHOD.GET.value
    action: str = ""


class InputText(BaseModel):
    name: str
    value: str


class SelectSearch(BaseModel):
    form: Form
    select: Select
    inputtext: InputText


class SelectForm(BaseModel):
    form: Form
    select: Select
