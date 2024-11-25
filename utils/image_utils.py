import base64

# Function to convert an image URL to a Base64-encoded string
def image_url_to_base64(image_url):
    with open(image_url, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

    return ""