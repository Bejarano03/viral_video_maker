from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem
from twelvelabs.tasks import TasksRetrieveResponse

import os
import boto3
from dotenv import load_dotenv

from glob import glob


load_dotenv()


# S3 config from environment
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def upload_video_to_s3(local_file_path, s3_key):
    """
    Upload a local video file to S3 and return the public URL
    """
    try:
        # Upload the file to S3
        s3_client.upload_file(local_file_path, S3_BUCKET, s3_key)
        
        # Generate the public URL
        s3_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        
        print(f"Successfully uploaded {local_file_path} to S3")
        print(f"S3 URL: {s3_url}")
        
        return s3_url
        
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        raise e



client = TwelveLabs(api_key=os.getenv("TWELVE_LABS_API_KEY"))

index = client.indexes.create(
    index_name="ddddyur",
    models=[
        IndexesCreateRequestModelsItem(
            model_name="marengo2.7",
            model_options=["visual", "audio"]
        )
    ]
)
if index.id is None:
    raise RuntimeError("Failed to create an index.")
print(f"Created index: id={index.id}")


video_path = os.path.join(os.path.dirname(__file__), "videos_twelve/test.MP4")
with open(video_path, "rb") as video_file:
    task = client.tasks.create(index_id=index.id, video_file=video_file)



def on_task_update(task: TasksRetrieveResponse):
    print(f"  Status={task.status}")
task = client.tasks.wait_for_done(task_id=task.id, callback=on_task_update)
if task.status != "ready":
    raise RuntimeError(f"Indexing failed with status {task.status}")
print(
    f"Upload complete. The unique identifier of your video is {task.video_id}.")

search_pager = client.search.query(
    index_id=index.id, query_text="look for black screens", search_options=["visual", "audio"],)
print("Search results:")
for clip in search_pager:
    print(
        f" video_id {clip.video_id} score={clip.score} start={clip.start} end={clip.end} confidence={clip.confidence}"
    )





"""
curl -X GET "https://api.twelvelabs.io/v1.3/indexes" \
  -H "x-api-key: tlk_0FH0KA318Q2K4E2K19T172AF4VS2"



{"data":[],"page_info":{"page":1,"limit_per_page":10,"total_page":0,"total_results":0}}
(base) hamzabenaggoun@Hamzas-MacBook-Pro ~ % 
"""








