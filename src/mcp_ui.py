
from mcp.types import EmbeddedResource, TextResourceContents


class UiResource(EmbeddedResource):
    """Wrapper that constructs an MCP EmbeddedResource with TextResourceContents.

    Returning this object from a FastMCP tool ensures the server emits a
    `{"type": "resource", ...}` content rather than wrapping JSON into a text content.
    """

    def __init__(self, uri: str, mimeType: str, text: str):

        if not uri.startswith("ui://"):
            raise ValueError(f"URI must start with 'ui://': {uri}")

        resource = TextResourceContents(uri=uri, mimeType=mimeType, text=text)
        # Pydantic BaseModel init for EmbeddedResource
        super().__init__(type="resource", resource=resource, annotations=None, meta=None)

    @classmethod
    def from_external_url(cls, uri: str, url: str) -> "UiResource":
        mime_type = "text/uri-list"
        return cls(uri=uri, mimeType=mime_type, text=url)

    @classmethod
    def from_html(cls, uri: str, html: str) -> "UiResource":
        mime_type = "text/html"
        return cls(uri=uri, mimeType=mime_type, text=html)