from pydantic import BaseModel


class HtmlContext(BaseModel):

    def get_context(self):
        return dict(self)
