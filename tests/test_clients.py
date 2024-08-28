    # create_client raises ValueError for unsupported provider names
def test_create_client_invalid_provider(self):
    from src.nbswitch.core import create_client
    with pytest.raises(ValueError, match="is not a package"):
        create_client(provider="InvalidProvider")


# create_client returns an Instructor instance for valid provider names
def test_create_client_valid_providers(self, mocker):
    from src.nbswitch.core import create_client
    from instructor import Instructor

    valid_providers = ["OpenAI", "Cohere", "Groq", "Ollama", "Anthropic"]
    for provider in valid_providers:
        mock_instructor = mocker.patch('instructor.from_' + provider.lower(), return_value=Instructor())
        client = create_client(provider=provider)
        assert isinstance(client, Instructor)
        mock_instructor.assert_called_once()