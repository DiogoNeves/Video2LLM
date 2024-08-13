import cv2
from PIL import Image, ImageDraw
from typing import List
import typer

# Constants
TARGET_SIZE = (400, 400)  # Size to downscale each frame
LINE_COLOR = "red"  # Color of the vertical line between frames
LINE_WIDTH = 5  # Width of the vertical line

app = typer.Typer()

def extract_frames(video_path: str, fps_sampling: int, max_frames: int) -> List[Image.Image]:
    """Extract frames from a video at a specified FPS and return them as PIL images."""
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(video_fps / fps_sampling)

    frames = []
    for count in range(total_frames):
        ret, frame = cap.read()
        if not ret or len(frames) >= max_frames:
            break
        if count % frame_interval == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb).resize(TARGET_SIZE)
            frames.append(frame_pil)

    cap.release()
    return frames

def concatenate_frames_with_lines(frames: List[Image.Image], line_width: int, line_color: str) -> Image.Image:
    """Concatenate frames horizontally with a vertical line between them."""
    if not frames:
        raise ValueError("No frames to concatenate.")

    total_width = sum(frame.width for frame in frames) + line_width * (len(frames) - 1)
    max_height = max(frame.height for frame in frames)

    concatenated_image = Image.new('RGB', (total_width, max_height))
    draw = ImageDraw.Draw(concatenated_image)

    x_offset = 0
    for i, frame in enumerate(frames):
        concatenated_image.paste(frame, (x_offset, 0))
        x_offset += frame.width
        if i < len(frames) - 1:
            draw.rectangle([x_offset, 0, x_offset + line_width - 1, max_height], fill=line_color)
            x_offset += line_width

    return concatenated_image

def generate_image_from_video(
    video_path: str,
    max_frames: int = 20,
    fps_sampling: int = 10
) -> Image.Image:
    """
    Generate a concatenated image from video frames.

    Args:
        video_path: Path to the input video file.
        max_frames: Maximum number of frames to extract (default: 20).
        fps_sampling: Frames per second to sample from the video (default: 10).

    Returns:
        A PIL Image object representing the concatenated frames.
    """
    frames = extract_frames(video_path, fps_sampling, max_frames)
    return concatenate_frames_with_lines(frames, LINE_WIDTH, LINE_COLOR)

def save_image(image: Image.Image, output_path: str) -> None:
    """Save the image to the specified output path."""
    image.save(output_path)
    print(f"Image saved to {output_path}")

@app.command()
def process_video_to_image(
    video_path: str,
    output_path: str = "output.jpg",
    max_frames: int = 20,
    fps_sampling: int = 10
) -> None:
    """
    Process a video into an image with concatenated frames.

    Args:
        video_path: Path to the input video file.
        output_path: Path to save the output image (default: output.jpg).
        max_frames: Maximum number of frames to extract (default: 20).
        fps_sampling: Frames per second to sample from the video (default: 10).
    """
    image = generate_image_from_video(video_path, max_frames, fps_sampling)
    save_image(image, output_path)

if __name__ == "__main__":
    app()
