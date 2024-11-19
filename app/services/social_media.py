import requests

def post_to_instagram(account_id: str, access_token: str, image_url: str, caption: str):
    media_url = f"https://graph.facebook.com/v12.0/{account_id}/media"
    payload = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }

    response = requests.post(media_url, data=payload)
    response_json = response.json()

    if 'id' in response_json:
        container_id = response_json['id']
        publish_url = f"https://graph.facebook.com/v12.0/{account_id}/media_publish"
        publish_payload = {
            'creation_id': container_id,
            'access_token': access_token
        }

        publish_response = requests.post(publish_url, data=publish_payload)
        
        if publish_response.status_code == 200:
            print("Posted on Instagram")
        else:
            raise Exception(f"Error publishing media: {publish_response.json()}")
    else:
        raise Exception(f"Error creating media container: {response_json}")

def post_to_facebook(page_id: str, access_token: str, image_path: str, caption: str):
    photo_url = f"https://graph.facebook.com/{page_id}/photos"
    payload = {
        "message": caption,
        "access_token": access_token,
    }

    with open(image_path, "rb") as image_file:
        files = {"source": image_file}
        response = requests.post(photo_url, data=payload, files=files)

    if response.status_code == 200:
        print("Posted on Facebook")
    else:
        raise Exception(f"Error posting image: {response.json()}")
