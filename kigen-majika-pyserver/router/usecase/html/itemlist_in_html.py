import json
import httpx

from datetime import tzinfo

from model.domain import Item, ItemSort, ItemStockFilter
from router.usecase.shared import htmlcontext, util as sutil
from router.usecase.shared import htmlname, htmlform
from router.param import ItemListGetForm


class InventoryFilterFactory:

    @classmethod
    def create(
        cls,
        form_method: str = htmlname.FORMMETHOD.GET.value,
        form_action: str = "",
        title: str = "在庫状況",
        input_name: str = htmlname.GETNAME.STOCK.value,
        select_id: int = 0,
    ) -> htmlform.SelectForm:
        menu_list: list[htmlform.SelectOption] = []
        for s in ItemStockFilter:
            selectopt = htmlform.SelectOption(id=s.id, text=s.jname, selected="")
            if select_id == s.id:
                selectopt.selected = htmlname.HTMLTemplateValue.SELECTED
            menu_list.append(selectopt)
        return htmlform.SelectForm(
            form_method=form_method,
            form_action=form_action,
            title=title,
            input_name=input_name,
            menu_list=menu_list,
        )


class ItemSortFormFactory:

    @classmethod
    def create(
        cls,
        form_method: str = htmlname.FORMMETHOD.GET.value,
        form_action: str = "",
        title: str = "並び替え",
        input_name: str = htmlname.GETNAME.ISORT.value,
        select_id: int = 0,
    ) -> htmlform.SelectForm:
        menu_list: list[htmlform.SelectOption] = []
        for i in ItemSort:
            selectopt = htmlform.SelectOption(id=i.id, text=i.jname, selected="")
            if select_id == i.id:
                selectopt.selected = htmlname.HTMLTemplateValue.SELECTED
            menu_list.append(selectopt)
        return htmlform.SelectForm(
            form_method=form_method,
            form_action=form_action,
            title=title,
            input_name=input_name,
            menu_list=menu_list,
        )


class ItemListInHTMLResult(htmlcontext.HtmlContext):
    inventory_filter: htmlform.SelectForm
    sort_order: htmlform.SelectForm
    hidden_input_dict: dict
    items: list[Item] = []
    items_length: int = 0
    error_msg: str = ""
    PARAM_ID: str = htmlname.POSTNAME.ID.value


class ItemListInHTMLResultFactory:
    @classmethod
    def create(
        cls, itemlistgetform: ItemListGetForm, items: list[Item], error_msg: str = ""
    ) -> ItemListInHTMLResult:
        items_length = len(items)
        hidden_input_dict = {}
        if itemlistgetform.isort:
            hidden_input_dict["isort"] = itemlistgetform.isort
        if itemlistgetform.stock:
            hidden_input_dict["stock"] = itemlistgetform.stock
        return ItemListInHTMLResult(
            inventory_filter=InventoryFilterFactory.create(
                select_id=itemlistgetform.stock or 0
            ),
            sort_order=ItemSortFormFactory.create(select_id=itemlistgetform.isort or 0),
            hidden_input_dict=hidden_input_dict,
            items=items,
            items_length=items_length,
            error_msg=error_msg,
        )


class ItemListInHTML:
    itemlistgetform: ItemListGetForm
    api_url: str
    local_timezone: tzinfo

    def __init__(
        self, api_url: str, local_timezone: tzinfo, itemlistgetform: ItemListGetForm
    ):
        self.api_url = api_url
        self.local_timezone = local_timezone
        self.itemlistgetform = itemlistgetform

    async def execute(self) -> ItemListInHTMLResult:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                self.api_url, json=json.loads(self.itemlistgetform.model_dump_json())
            )
        if not res.json():
            return ItemListInHTMLResultFactory.create(
                itemlistgetform=self.itemlistgetform,
                items=[],
                error_msg=htmlname.HTMLViewError.NOT_RESULT_API.jname,
            )
        result = ItemListInHTMLResultFactory.create(
            **res.json(),
            itemlistgetform=self.itemlistgetform,
        )
        if result.items:
            result.items_length = len(result.items)
            for i in result.items:
                self.toLocaltimezone(item=i, tz=self.local_timezone)
        return result

    def toLocaltimezone(self, item: Item, tz: tzinfo) -> None:
        if item.expiry_date:
            item.expiry_date = sutil.utcTolocaltime(input_date=item.expiry_date, tz=tz)
        item.created_at = sutil.utcTolocaltime(input_date=item.created_at, tz=tz)
        item.updated_at = sutil.utcTolocaltime(input_date=item.updated_at, tz=tz)
