"""
Integration test to verify that our UiResource format matches what @mcp-ui/client expects.
This test simulates the client-side parsing and validates the JSON structure.
"""
import json
import pytest
from src.mcp_ui import UiResource


def test_client_integration_external_url():
    """Test that our UiResource matches the expected client format for external URLs."""
    # Create a UiResource like our server would
    result = UiResource.from_external_url(uri="ui://external-url", url="https://example.com")
    
    # Simulate what the MCP server would send to the client
    if hasattr(result.resource, 'model_dump'):
        resource_dict = result.resource.model_dump(mode='json')
        client_payload = {
            'meta': result.meta,
            'annotations': result.annotations,
            'type': result.type,
            'resource': resource_dict
        }
    else:
        pytest.skip("TextResourceContents doesn't have model_dump method")
    
    # Convert to JSON (what the client would receive)
    json_payload = json.dumps(client_payload)
    parsed_payload = json.loads(json_payload)
    
    # Verify the structure matches what UIResourceRenderer expects
    assert parsed_payload['type'] == 'resource'
    assert parsed_payload['resource']['uri'].startswith('ui://')
    assert parsed_payload['resource']['mimeType'] == 'text/uri-list'
    assert parsed_payload['resource']['text'] == 'https://example.com'
    
    # Test the client-side condition from the example
    mcpResource = parsed_payload
    client_condition = (
        mcpResource['type'] == 'resource' and
        mcpResource['resource']['uri'].startswith('ui://')
    )
    assert client_condition, "Client-side condition should pass"
    
    print("✅ Client integration test passed!")
    print(f"JSON payload: {json.dumps(parsed_payload, indent=2)}")


def test_client_integration_html():
    """Test that our UiResource matches the expected client format for HTML."""
    # Create an HTML UiResource
    result = UiResource.from_html(uri="ui://html-demo", html="<h1>Hello World</h1>")
    
    # Simulate what the MCP server would send to the client
    if hasattr(result.resource, 'model_dump'):
        resource_dict = result.resource.model_dump(mode='json')
        client_payload = {
            'meta': result.meta,
            'annotations': result.annotations,
            'type': result.type,
            'resource': resource_dict
        }
    else:
        pytest.skip("TextResourceContents doesn't have model_dump method")
    
    # Convert to JSON (what the client would receive)
    json_payload = json.dumps(client_payload)
    parsed_payload = json.loads(json_payload)
    
    # Verify the structure
    assert parsed_payload['type'] == 'resource'
    assert parsed_payload['resource']['uri'].startswith('ui://')
    assert parsed_payload['resource']['mimeType'] == 'text/html'
    assert parsed_payload['resource']['text'] == '<h1>Hello World</h1>'
    
    # Test the client-side condition
    mcpResource = parsed_payload
    client_condition = (
        mcpResource['type'] == 'resource' and
        mcpResource['resource']['uri'].startswith('ui://')
    )
    assert client_condition, "Client-side condition should pass"
    
    print("✅ HTML client integration test passed!")


def test_client_payload_structure():
    """Test that our payload structure exactly matches the expected client format."""
    result = UiResource.from_external_url(uri="ui://test", url="https://test.com")
    
    # Get the JSON structure
    if hasattr(result.resource, 'model_dump'):
        resource_dict = result.resource.model_dump(mode='json')
        payload = {
            'meta': result.meta,
            'annotations': result.annotations,
            'type': result.type,
            'resource': resource_dict
        }
    else:
        pytest.skip("TextResourceContents doesn't have model_dump method")
    
    # Verify all expected fields are present
    expected_top_level_fields = {'meta', 'annotations', 'type', 'resource'}
    assert set(payload.keys()) == expected_top_level_fields
    
    # Verify resource structure
    resource = payload['resource']
    expected_resource_fields = {'uri', 'mimeType', 'meta', 'text'}
    assert set(resource.keys()) == expected_resource_fields
    
    # Verify types
    assert payload['meta'] is None
    assert payload['annotations'] is None
    assert isinstance(payload['type'], str)
    assert isinstance(resource, dict)
    assert isinstance(resource['uri'], str)
    assert isinstance(resource['mimeType'], str)
    assert isinstance(resource['text'], str)
    
    print("✅ Payload structure validation passed!")


if __name__ == "__main__":
    # Run the tests directly
    test_client_integration_external_url()
    test_client_integration_html() 
    test_client_payload_structure()
    print("\n🎉 All client integration tests passed!")
