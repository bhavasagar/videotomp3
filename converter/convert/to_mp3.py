import pika, json, os, tempfile
from bson.objectid import ObjectId
import moviepy.editor

def start(body, fs_videos, fs_mp3s, ch):
    message = json.loads(body)
    
    temporary_file = tempfile.NamedTemporaryFile()
    out = fs_videos.get(ObjectId(message["video_fid"]))
    temporary_file.write(out.read())
    
    audio = moviepy.editor.VideoFileClip(temporary_file.name).audio
    audio_file_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(audio_file_path)
    
    with open(audio_file_path) as af:
        data = af.read()
        audio_fid = fs_mp3s.put(data)
    
    os.remove(audio_file_path)
    message["mp3_fid"] = str(audio_fid)
    
    try:
        ch.basic_publish(
            exchange="",
            routing_key = os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )    
    except Exception as e:
        print("Error in putting auido file id in queue, ", e)
        fs_mp3s.delete(audio_fid)
        return "Failed to add message"    