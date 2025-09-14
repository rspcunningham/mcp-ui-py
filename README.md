## MCP‑UI Resource helper

`src/mcp_ui.py` provides a tiny helper class `UiResource` to build MCP‑UI compliant UI resources that your host/client can render. It follows the Interactive UI Resource Protocol described in the MCP‑UI docs: [Introduction](https://mcpui.dev/guide/introduction).

### What it produces (maps to MCP‑UI UIResource)

- Top-level shape: `{ meta, annotations, type, resource }` (the first two are convenience fields on this helper)
- `type` is always `"resource"`
- `resource` is an MCP `TextResourceContents` with fields `{ uri, mimeType, text, meta }`
- URIs must start with `ui://`
- `mimeType` controls rendering per MCP‑UI:
  - `text/html` → inline HTML (rendered via iframe srcdoc)
  - `text/uri-list` → external URL (rendered via iframe src)
  - (Future) `application/vnd.mcp-ui.remote-dom` → remote DOM JavaScript channel from the MCP‑UI spec

Example serialized JSON sent to a client/host:

```json
{
  "meta": null,
  "annotations": null,
  "type": "resource",
  "resource": {
    "uri": "ui://external-url",
    "mimeType": "text/uri-list",
    "meta": null,
    "text": "https://example.com"
  }
}
```

### API

```python
from mcp_ui import UiResource

# Constructors
UiResource.from_external_url(uri: str, url: str)
UiResource.from_html(uri: str, html: str)
```

Validation: raises `ValueError` if `uri` does not start with `"ui://"`.

### Using in an MCP server (FastMCP)

```python
from fastmcp import FastMCP
from mcp_ui import UiResource

mcp = FastMCP()

@mcp.tool(name="show_external_url")
def show_external_url() -> UiResource:
    return UiResource.from_external_url(
        uri="ui://external-url",
        url="https://example.com",
    )

@mcp.tool(name="show_html")
def show_html() -> UiResource:
    return UiResource.from_html(
        uri="ui://html-demo",
        html="<h1>Hello</h1>",
    )
```

### Serializing for transport

`TextResourceContents.uri` is an `AnyUrl` (pydantic). Use `model_dump(mode="json")` so URLs become strings:

```python
res = UiResource.from_external_url("ui://external-url", "https://example.com")
payload = {
    "meta": res.meta,
    "annotations": res.annotations,
    "type": res.type,
    "resource": res.resource.model_dump(mode="json"),
}
```

### Rendering on the client

With the client SDK `@mcp-ui/client` you can render UI resources:

```tsx
import { UIResourceRenderer } from '@mcp-ui/client';

function App({ mcpResource }) {
  if (
    mcpResource.type === 'resource' &&
    mcpResource.resource.uri?.startsWith('ui://')
  ) {
    return (
      <UIResourceRenderer
        resource={mcpResource.resource}
        onUIAction={(result) => console.log('Action:', result)}
      />
    );
  }
  return <p>Unsupported resource</p>;
}
```

Client library reference:

- Docs site: [MCP‑UI Guide](https://mcpui.dev/guide/introduction)
- TypeScript SDK: [`@mcp-ui/client`](https://github.com/idosal/mcp-ui/tree/main/sdks/typescript/client)

### Tests

Run all tests:

```bash
uv run pytest
```


