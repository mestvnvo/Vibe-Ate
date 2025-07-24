from gradio_client import Client, handle_file
import tempfile
import os

from app.core.config import settings

def call_gradio_client_api(
    space_name: str,
    input_data: str | bytes,
    input_type: str = "text",
    api_name: str = "/predict"
) -> any:

    client = Client(space_name, hf_token=settings.HF_API_TOKEN)

    if input_type == "image":
        # Write image bytes to a temp file, then delete it after use
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(input_data)
            temp.flush()
            temp_path = temp.name

        try:
            return client.predict(image=handle_file(temp_path), api_name=api_name)
        finally:
            os.remove(temp_path)

    elif input_type == "text":
        return client.predict(input_data, api_name=api_name)

    else:
        raise ValueError("Unsupported input_type: must be 'text' or 'image'")
