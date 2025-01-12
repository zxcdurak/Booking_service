from app.tasks.celery import celery
from PIL import Image
from pathlib import Path


@celery.task
def process_pic(
   path: str
):
   img_path = Path(path)
   img = Image.open(img_path)
   resized_img_1000_500 = img.resize((1000, 500))
   resized_img_200_100 = img.resize((200, 100))
   resized_img_1000_500.save(f"app/static/images/resize_1000_500_{img_path.name}")
   resized_img_200_100.save(f"app/static/images/resize_200_100_{img_path.name}")

