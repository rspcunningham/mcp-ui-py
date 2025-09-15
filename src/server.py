#from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP
from mcp_ui import UiResource

mcp = FastMCP()

url = "https://www.google.com"

@mcp.tool(name="show_external_url", description="Creates a UI resource displaying an external URL")
def show_external_url() -> UiResource:
    return UiResource.from_url(uri="ui://external-url", url=url)

@mcp.tool(name="show_html", description="Creates a UI resource displaying an HTML string")
def show_html() -> UiResource:
    return UiResource.from_html(uri="ui://html-demo", html="<h1>Hello from HTML</h1>")

app = mcp.http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('server:app', host="0.0.0.0", port=8000)