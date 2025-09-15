from mcp.types import EmbeddedResource, TextResourceContents
from enum import Enum

class MimeType(Enum):
    URL = "text/uri-list"
    HTML = "text/html"

class UiResource(EmbeddedResource):
    """Wrapper that constructs an MCP Embedded Resource folling the MCP-UI UIResource protocol.
    """

    def __init__(self, uri: str, mime_type: MimeType, text: str):

        if not uri.startswith("ui://"):
            raise ValueError(f"URI must start with 'ui://': {uri}")

        resource = TextResourceContents(uri=uri, mimeType=mime_type, text=text)
        super().__init__(type="resource", resource=resource, annotations=None, meta=None)

    @classmethod
    def from_url(cls, uri: str, url: str) -> "UiResource":
        mime_type = MimeType.URL
        return cls(uri=uri, mime_type=mime_type, text=url)

    @classmethod
    def from_html(cls, uri: str, html: str) -> "UiResource":
        mime_type = MimeType.HTML
        return cls(uri=uri, mime_type=mime_type, text=html)