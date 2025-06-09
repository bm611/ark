Title: OpenRouter Images & PDFs - Complete Documentation

URL Source: http://openrouter.ai/docs/features/images-and-pdfs

Markdown Content:
OpenRouter supports sending images and PDFs via the API. This guide will show you how to work with both file types using our API.

Both images and PDFs also work in the chat room.

You can send both PDF and images in the same request.

## Image Inputs

Requests with images, to multimodel models, are available via the `/api/v1/chat/completions` API with a multi-part `messages` parameter. The `image_url` can either be a URL or a base64-encoded image. Note that multiple images can be sent in separate content array entries. The number of images you can send in a single request varies per provider and per model. Due to how the content is parsed, we recommend sending the text prompt first, then the images. If the images must come first, we recommend putting it in the system prompt.

### Using Image URLs

Here’s how to send an image using a URL:

`1import requests2import json34url = "https://openrouter.ai/api/v1/chat/completions"5headers = {6    "Authorization": f"Bearer {API_KEY_REF}",7    "Content-Type": "application/json"8}910messages = [11    {12        "role": "user",13        "content": [14            {15                "type": "text",16                "text": "What's in this image?"17            },18            {19                "type": "image_url",20                "image_url": {21                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"22                }23            }24        ]25    }26]2728payload = {29    "model": "google/gemini-2.0-flash-001",30    "messages": messages31}3233response = requests.post(url, headers=headers, json=payload)34print(response.json())`

### Using Base64 Encoded Images

For locally stored images, you can send them using base64 encoding. Here’s how to do it:

`1import requests2import json3import base644from pathlib import Path56def encode_image_to_base64(image_path):7    with open(image_path, "rb") as image_file:8        return base64.b64encode(image_file.read()).decode('utf-8')910url = "https://openrouter.ai/api/v1/chat/completions"11headers = {12    "Authorization": f"Bearer {API_KEY_REF}",13    "Content-Type": "application/json"14}1516# Read and encode the image17image_path = "path/to/your/image.jpg"18base64_image = encode_image_to_base64(image_path)19data_url = f"data:image/jpeg;base64,{base64_image}"2021messages = [22    {23        "role": "user",24        "content": [25            {26                "type": "text",27                "text": "What's in this image?"28            },29            {30                "type": "image_url",31                "image_url": {32                    "url": data_url33                }34            }35        ]36    }37]3839payload = {40    "model": "google/gemini-2.0-flash-001",41    "messages": messages42}4344response = requests.post(url, headers=headers, json=payload)45print(response.json())`

Supported image content types are:

- `image/png`
- `image/jpeg`
- `image/webp`

## PDF Support

OpenRouter supports PDF processing through the `/api/v1/chat/completions` API. PDFs can be sent as base64-encoded data URLs in the messages array, via the file content type. This feature works on **any** model on OpenRouter.

When a model supports file input natively, the PDF is passed directly to the model. When the model does not support file input natively, OpenRouter will parse the file and pass the parsed results to the requested model.

Note that multiple PDFs can be sent in separate content array entries. The number of PDFs you can send in a single request varies per provider and per model. Due to how the content is parsed, we recommend sending the text prompt first, then the PDF. If the PDF must come first, we recommend putting it in the system prompt.

### Processing PDFs

Here’s how to send and process a PDF:

`1import requests2import json3import base644from pathlib import Path56def encode_pdf_to_base64(pdf_path):7    with open(pdf_path, "rb") as pdf_file:8        return base64.b64encode(pdf_file.read()).decode('utf-8')910url = "https://openrouter.ai/api/v1/chat/completions"11headers = {12    "Authorization": f"Bearer {API_KEY_REF}",13    "Content-Type": "application/json"14}1516# Read and encode the PDF17pdf_path = "path/to/your/document.pdf"18base64_pdf = encode_pdf_to_base64(pdf_path)19data_url = f"data:application/pdf;base64,{base64_pdf}"2021messages = [22    {23        "role": "user",24        "content": [25            {26                "type": "text",27                "text": "What are the main points in this document?"28            },29            {30                "type": "file",31                "file": {32                    "filename": "document.pdf",33                    "file_data": data_url34                }35            },36        ]37    }38]3940# Optional: Configure PDF processing engine41# PDF parsing will still work even if the plugin is not explicitly set42plugins = [43    {44        "id": "file-parser",45        "pdf": {46            "engine": "pdf-text"  # defaults to "mistral-ocr". See Pricing below47        }48    }49]5051payload = {52    "model": "google/gemma-3-27b-it",53    "messages": messages,54    "plugins": plugins55}5657response = requests.post(url, headers=headers, json=payload)58print(response.json())`

### Pricing

OpenRouter provides several PDF processing engines:

1.  `"mistral-ocr"`: Best for scanned documents or PDFs with images ($2 per 1,000 pages).
2.  `"pdf-text"`: Best for well-structured PDFs with clear text content (Free).
3.  `"native"`: Only available for models that support file input natively (charged as input tokens).

If you don’t explicitly specify an engine, OpenRouter will default first to the model’s native file processing capabilities, and if that’s not available, we will use the `"mistral-ocr"` engine.

To select an engine, use the plugin configuration:

`1plugins = [2    {3        "id": "file-parser",4        "pdf": {5            "engine": "mistral-ocr"6        }7    }8]`

### Skip Parsing Costs

When you send a PDF to the API, the response may include file annotations in the assistant’s message. These annotations contain structured information about the PDF document that was parsed. By sending these annotations back in subsequent requests, you can avoid re-parsing the same PDF document multiple times, which saves both processing time and costs.

Here’s how to reuse file annotations:

`1import requests2import json3import base644from pathlib import Path56# First, encode and send the PDF7def encode_pdf_to_base64(pdf_path):8    with open(pdf_path, "rb") as pdf_file:9        return base64.b64encode(pdf_file.read()).decode('utf-8')1011url = "https://openrouter.ai/api/v1/chat/completions"12headers = {13    "Authorization": f"Bearer {API_KEY_REF}",14    "Content-Type": "application/json"15}1617# Read and encode the PDF18pdf_path = "path/to/your/document.pdf"19base64_pdf = encode_pdf_to_base64(pdf_path)20data_url = f"data:application/pdf;base64,{base64_pdf}"2122# Initial request with the PDF23messages = [24    {25        "role": "user",26        "content": [27            {28                "type": "text",29                "text": "What are the main points in this document?"30            },31            {32                "type": "file",33                "file": {34                    "filename": "document.pdf",35                    "file_data": data_url36                }37            },38        ]39    }40]4142payload = {43    "model": "google/gemma-3-27b-it",44    "messages": messages45}4647response = requests.post(url, headers=headers, json=payload)48response_data = response.json()4950# Store the annotations from the response51file_annotations = None52if response_data.get("choices") and len(response_data["choices"]) > 0:53    if "annotations" in response_data["choices"][0]["message"]:54        file_annotations = response_data["choices"][0]["message"]["annotations"]5556# Follow-up request using the annotations (without sending the PDF again)57if file_annotations:58    follow_up_messages = [59        {60            "role": "user",61            "content": [62                {63                    "type": "text",64                    "text": "What are the main points in this document?"65                },66                {67                    "type": "file",68                    "file": {69                        "filename": "document.pdf",70                        "file_data": data_url71                    }72                }73            ]74        },75        {76            "role": "assistant",77            "content": "The document contains information about...",78            "annotations": file_annotations79        },80        {81            "role": "user",82            "content": "Can you elaborate on the second point?"83        }84    ]8586    follow_up_payload = {87        "model": "google/gemma-3-27b-it",88        "messages": follow_up_messages89    }9091    follow_up_response = requests.post(url, headers=headers, json=follow_up_payload)92    print(follow_up_response.json())`

When you include the file annotations from a previous response in your subsequent requests, OpenRouter will use this pre-parsed information instead of re-parsing the PDF, which saves processing time and costs. This is especially beneficial for large documents or when using the `mistral-ocr` engine which incurs additional costs.

### Response Format

The API will return a response in the following format:

`1{2  "id": "gen-1234567890",3  "provider": "DeepInfra",4  "model": "google/gemma-3-27b-it",5  "object": "chat.completion",6  "created": 1234567890,7  "choices": [8    {9      "message": {10        "role": "assistant",11        "content": "The document discusses..."12      }13    }14  ],15  "usage": {16    "prompt_tokens": 1000,17    "completion_tokens": 100,18    "total_tokens": 110019  }20}`
