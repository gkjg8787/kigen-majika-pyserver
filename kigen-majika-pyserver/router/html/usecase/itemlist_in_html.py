import json
import httpx

from datetime import datetime, timezone, tzinfo

from domain.models import Item, ItemSort, ItemStockFilter, ItemSearchType
from .shared import htmlcontext, htmlname, htmlelement, util as sutil
from router.html.param import ItemListGetForm


class InventoryFilterFactory:

    @classmethod
    def create(
        cls,
        form_method: str = htmlname.FORMMETHOD.GET.value,
        form_action: str = "",
        title: str = "在庫状況",
        input_name: str = htmlname.GETNAME.STOCK.value,
        select_id: int = 0,
    ) -> htmlelement.SelectForm:
        menu_list: list[htmlelement.SelectOption] = []
        for s in ItemStockFilter:
            selectopt = htmlelement.SelectOption(id=s.id, text=s.jname, selected="")
            if select_id == s.id:
                selectopt.selected = htmlname.HTMLTemplateValue.SELECTED
            menu_list.append(selectopt)
        return htmlelement.SelectForm(
            form=htmlelement.Form(method=form_method, action=form_action),
            select=htmlelement.Select(
                title=title, input_name=input_name, menu_list=menu_list
            ),
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
    ) -> htmlelement.SelectForm:
        menu_list: list[htmlelement.SelectOption] = []
        for i in ItemSort:
            selectopt = htmlelement.SelectOption(id=i.id, text=i.jname, selected="")
            if select_id == i.id:
                selectopt.selected = htmlname.HTMLTemplateValue.SELECTED
            menu_list.append(selectopt)
        return htmlelement.SelectForm(
            form=htmlelement.Form(method=form_method, action=form_action),
            select=htmlelement.Select(
                title=title, input_name=input_name, menu_list=menu_list
            ),
        )


class ItemSearchTypeSelectSearchFactory:
    @classmethod
    def create(
        cls,
        form_method: str = htmlname.FORMMETHOD.GET.value,
        form_action: str = "",
        title: str = "検索対象",
        input_name: str = htmlname.GETNAME.STYPE.value,
        selected_id: int = 0,
        word: str = "",
    ) -> htmlelement.SelectSearch:
        menu_list: list[htmlelement.SelectOption] = []
        for i in ItemSearchType:
            selectopt = htmlelement.SelectOption(id=i.id, text=i.jname, selected="")
            if selected_id == i.id:
                selectopt.selected = htmlname.HTMLTemplateValue.SELECTED
            menu_list.append(selectopt)
        return htmlelement.SelectSearch(
            form=htmlelement.Form(method=form_method, action=form_action),
            select=htmlelement.Select(
                title=title, input_name=input_name, menu_list=menu_list
            ),
            inputtext=htmlelement.InputText(
                name=htmlname.GETNAME.WORD.value, value=word
            ),
        )


class ViewItem(Item):
    days_to_deadline: int | None = None


class ItemListInHTMLResult(htmlcontext.HtmlContext):
    inventory_filter: htmlelement.SelectForm
    sort_order: htmlelement.SelectForm
    search_filter: htmlelement.SelectSearch
    hidden_input_dict: dict
    items: list[ViewItem] = []
    items_length: int = 0
    error_msg: str = ""
    PARAM_ID: str = htmlname.POSTNAME.ID.value


class ItemListInHTMLResultFactory:
    @classmethod
    def create(
        cls,
        itemlistgetform: ItemListGetForm,
        items: list[dict],
        error_msg: str = "",
        local_timezone: tzinfo | None = None,
    ) -> ItemListInHTMLResult:
        items_length = len(items)
        hidden_input_dict = {}
        if itemlistgetform.isort:
            hidden_input_dict["isort"] = itemlistgetform.isort
        if itemlistgetform.stock:
            hidden_input_dict["stock"] = itemlistgetform.stock
        if itemlistgetform.stype:
            hidden_input_dict["stype"] = itemlistgetform.stype
        if itemlistgetform.word:
            hidden_input_dict["word"] = itemlistgetform.word
        viewitems: list[ViewItem] = []
        if items:
            viewitems = cls.create_viewitems(items=items, tz=local_timezone)
        return ItemListInHTMLResult(
            inventory_filter=InventoryFilterFactory.create(
                select_id=itemlistgetform.stock or 0
            ),
            sort_order=ItemSortFormFactory.create(select_id=itemlistgetform.isort or 0),
            search_filter=ItemSearchTypeSelectSearchFactory.create(
                selected_id=itemlistgetform.stype or 0, word=itemlistgetform.word
            ),
            hidden_input_dict=hidden_input_dict,
            items=viewitems,
            items_length=items_length,
            error_msg=error_msg,
        )

    @classmethod
    def create_viewitems(cls, items: list[dict], tz: tzinfo) -> list[ViewItem]:
        results: list[ViewItem] = []
        now = datetime.now(timezone.utc)
        for i in items:
            viewitem = ViewItem(**i)
            results.append(viewitem)
            cls.toLocaltimezone(item=viewitem, tz=tz)
            if viewitem.expiry_date:
                viewitem.days_to_deadline = (viewitem.expiry_date - now).days
        return results

    @classmethod
    def toLocaltimezone(cls, item: ViewItem, tz: tzinfo) -> None:
        if item.expiry_date:
            item.expiry_date = sutil.utcTolocaltime(input_date=item.expiry_date, tz=tz)
        item.created_at = sutil.utcTolocaltime(input_date=item.created_at, tz=tz)
        item.updated_at = sutil.utcTolocaltime(input_date=item.updated_at, tz=tz)


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
                local_timezone=self.local_timezone,
            )
        result = ItemListInHTMLResultFactory.create(
            **res.json(),
            itemlistgetform=self.itemlistgetform,
            local_timezone=self.local_timezone
        )
        return result
