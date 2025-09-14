
from dataclasses import dataclass
from mcp.types import TextResourceContents

@dataclass
class UiResource:
    meta: None
    annotations: None
    type: str
    resource: TextResourceContents

    def __init__(self, uri: str, mimeType: str, text: str):

        if not uri.startswith("ui://"):
            raise ValueError(f"URI must start with 'ui://': {uri}")
        
        self.meta = None
        self.annotations = None
        self.type = "resource"
        self.resource = TextResourceContents(uri=uri, mimeType=mimeType, text=text)

    @classmethod
    def from_external_url(cls, uri: str, url: str) -> "UiResource":
        
        mime_type = "text/uri-list"
        return cls(uri=uri, mimeType=mime_type, text=url)

    @classmethod
    def from_html(cls, uri: str, html: str) -> "UiResource":
        
        mime_type = "text/html"
        return cls(uri=uri, mimeType=mime_type, text=html)
    
    def __post_init__(self):
        # This ensures the dataclass is properly initialized
        pass