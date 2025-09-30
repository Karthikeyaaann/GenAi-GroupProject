import threading
import time
import cv2
import base64
import json
import sys

# Try to import ollama; if not available, we'll use REST via requests
try:
    import ollama
    _HAS_OLLAMA = True
except Exception:
    _HAS_OLLAMA = False
    import requests

class FrameGrabber(threading.Thread):
    def __init__(self, src=0, target_fps=24, max_width=1024):
        super().__init__(daemon=True)
        self.cap = cv2.VideoCapture(src)
        self.running = True
        self.lock = threading.Lock()
        self.latest_frame = None
        self.target_fps = target_fps
        self.max_width = max_width

    def run(self):
        interval = 1.0 / float(self.target_fps)
        while self.running:
            t0 = time.time()
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            with self.lock:
                self.latest_frame = frame.copy()
            elapsed = time.time() - t0
            to_sleep = max(0, interval - elapsed)
            time.sleep(to_sleep)

    def stop(self):
        self.running = False
        try:
            self.cap.release()
        except Exception:
            pass

    def get_latest_frame_b64(self, jpeg_quality=80):
        with self.lock:
            f = None if self.latest_frame is None else self.latest_frame.copy()
        if f is None:
            return None
        h, w = f.shape[:2]
        if self.max_width and w > self.max_width:
            scale = self.max_width / float(w)
            f = cv2.resize(f, (int(w*scale), int(h*scale)))
        ok, buf = cv2.imencode('.jpg', f, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        if not ok:
            return None
        b64 = base64.b64encode(buf.tobytes()).decode('ascii')
        return b64


class ModelClient:
    def __init__(self, model='llama3.2-vision', host='http://localhost:11434'):
        self.model = model
        self.host = host
        self.use_ollama_pkg = _HAS_OLLAMA

    def query(self, prompt: str, image_b64_list=None, timeout=60):
        messages = []
        if image_b64_list:
            messages.append({'role': 'user', 'content': prompt, 'images': image_b64_list})
        else:
            messages.append({'role': 'user', 'content': prompt})

        if self.use_ollama_pkg:
            # Using the ollama python package
            resp = ollama.chat(model=self.model, messages=messages, stream=False)
            try:
                return resp.message.content
            except Exception:
                try:
                    return resp['message']['content']
                except Exception:
                    return str(resp)
        else:
            payload = {'model': self.model, 'messages': messages}
            r = requests.post(f'{self.host}/api/chat', json=payload, timeout=timeout)
            r.raise_for_status()
            j = r.json()
            if isinstance(j, dict) and 'message' in j and isinstance(j['message'], dict) and 'content' in j['message']:
                return j['message']['content']
            return json.dumps(j)


def interactive_loop(frame_grabber: FrameGrabber, client: ModelClient):
    print("Interactive mode. Type a question and press Enter. Type 'exit' to quit.")
    while True:
        try:
            prompt = input("USER> ").strip()
        except (EOFError, KeyboardInterrupt):
            print('\nShutting down...')
            break
        if not prompt:
            continue
        if prompt.lower() in ('exit', 'quit'):
            break

        # Grab one (or a few) latest frames. Adjust number if you need temporal reasoning.
        b64 = frame_grabber.get_latest_frame_b64(jpeg_quality=75)
        if b64 is None:
            print("No frame available yet. Try again in a moment.")
            continue

        print("Sending image to model... (this can be slow depending on model/hardware)")
        try:
            answer = client.query(prompt, image_b64_list=[b64])
            print("MODEL>", answer)
        except Exception as e:
            print("Error calling model:", e)


if __name__ == '__main__':
    src = 0  # change to RTSP URL or video file as needed
    fg = FrameGrabber(src=src, target_fps=24, max_width=1024)
    fg.start()
    client = ModelClient(model='llama3.2-vision')
    try:
        interactive_loop(fg, client)
    finally:
        fg.stop()
        time.sleep(0.2)
        print('Stopped')
