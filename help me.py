import json
import requests


def create_request_body(text_data, inline_data, binary_data_encoded):
    """
    Construct the request body with inline data and other content parts.
    """
    request_body = {
        "content": {
            "parts": [
                {"text": text_data},
                {"inline_data": inline_data, "mime_type": "text/plain"},
                {"blob": binary_data_encoded, "mime_type": "application/octet-stream"}
            ]
        }
    }
    return json.dumps(request_body)


def send_api_request(request_body):
    """
    Send the constructed request body to the API endpoint.
    """
    url = "https://example.com/api/endpoint"
    headers = {'Content-Type': 'application/json'}

    # Send the request
    response = requests.post(url, data=request_body, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Success:", response.text)
    else:
        print("Failed:", response.status_code, response.text)


def main():
    text_data = "Hello, this is a text part of the request."
    inline_data = json.dumps({"key1": "value1", "key2": "value2"})
    binary_data = b'Example binary data here'
    binary_data_encoded = json.dumps(binary_data.decode('utf-8'))  # Encode binary data to base64 if needed

    request_body = create_request_body(text_data, inline_data, binary_data_encoded)
    send_api_request(request_body)


if __name__ == "__main__":
    main()
