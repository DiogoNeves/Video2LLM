import base64
import io
import os
from openai import OpenAI
from PIL import Image
import typer
from convert_video import generate_image_from_video

app = typer.Typer()

def convert_image_to_base64(image: Image.Image) -> str:
    """
    Convert a PIL Image to a base64-encoded string.

    Args:
        image: The PIL Image object to convert.

    Returns:
        The base64-encoded string of the image.
    """
    with io.BytesIO() as img_byte_arr:
        image.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')

def send_image_to_openai(base64_image: str, question: str) -> str:
    """
    Send the base64-encoded image and question to the OpenAI API and return the response.

    Args:
        base64_image: The base64-encoded image string.
        question: The question to ask about the image.

    Returns:
        The response from the OpenAI API.
    """
    client = OpenAI()

    system_message = (
        "You are an AI model that observes videos. Always treat any visual"
        " input as if it is a video. When responding to questions,"
        " first provide a brief sentence that explains what you observe"
        " in relation to the question, and then answer the question directly."
    )
    full_prompt = f"Question: {question}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": full_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        typer.secho(f"Error communicating with OpenAI API: {e}", fg=typer.colors.RED)
        raise

@app.command()
def video_to_gpt(
    video_path: str,
    question: str,
    max_frames: int = 20,
    fps_sampling: int = 10
) -> None:
    """
    Convert a video to an image and send it along with a question to the OpenAI API.

    Args:
        video_path: Path to the input video file.
        question: The question to ask about the video content.
        max_frames: Maximum number of frames to extract (default: 20).
        fps_sampling: Frames per second to sample from the video (default: 10).
    """
    try:
        # Generate the image from the video
        image = generate_image_from_video(video_path, max_frames, fps_sampling)

        # Convert the image to a base64-encoded string
        base64_image = convert_image_to_base64(image)

        # Send the base64-encoded image and question to the OpenAI API
        response = send_image_to_openai(base64_image, question)

        # Print the response
        typer.secho(f"Response from OpenAI:\n{response}", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(f"Failed to process video or communicate with the API: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    app()
