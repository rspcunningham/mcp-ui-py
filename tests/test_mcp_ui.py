import pytest
from src.mcp_ui import UiResource


def test_from_external_url():
    """Test UiResource.from_external_url creates correct structure."""
    result = UiResource.from_external_url(uri="ui://external-url", url="https://example.com")
    
    # Test the structure directly
    assert result.meta is None
    assert result.annotations is None
    assert result.type == "resource"
    assert str(result.resource.uri) == "ui://external-url"
    assert result.resource.mimeType == "text/uri-list"
    assert result.resource.text == "https://example.com"
    assert result.resource.meta is None


def test_from_html():
    """Test UiResource.from_html creates correct structure."""
    result = UiResource.from_html(uri="ui://html-demo", html="<h1>Hello World</h1>")
    
    # Test the structure directly
    assert result.meta is None
    assert result.annotations is None
    assert result.type == "resource"
    assert str(result.resource.uri) == "ui://html-demo"
    assert result.resource.mimeType == "text/html"
    assert result.resource.text == "<h1>Hello World</h1>"
    assert result.resource.meta is None


def test_uri_validation():
    """Test that URI must start with 'ui://'."""
    with pytest.raises(ValueError, match="URI must start with 'ui://'"):
        UiResource.from_external_url(uri="http://invalid", url="https://example.com")
    
    with pytest.raises(ValueError, match="URI must start with 'ui://'"):
        UiResource.from_html(uri="invalid://test", html="<p>test</p>")


def test_direct_constructor():
    """Test direct UiResource constructor."""
    result = UiResource(uri="ui://test", mimeType="text/plain", text="test content")
    
    # Test the structure directly
    assert result.meta is None
    assert result.annotations is None
    assert result.type == "resource"
    assert str(result.resource.uri) == "ui://test"
    assert result.resource.mimeType == "text/plain"
    assert result.resource.text == "test content"
    assert result.resource.meta is None
