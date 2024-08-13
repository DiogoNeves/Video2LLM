# Video2Image

> **Transform video content into a format that LLMs can understand.**

Video2Image converts video frames into a single, comprehensive image, enabling you to ask questions about the video to a Visual LLM.  
Since LLMs can process images as inputs, this tool packages your video as a sequence of frames in one image, allowing the model to analyze and respond to your questions about the video.

The intention of this project is to make it simple to use video content in any LLM by exporting the image. However, there's also a way to directly ask questions using the `video_gpt.py` script.

This project is experimental, and I’m actively researching and refining the approach.

Feedback and suggestions are highly encouraged as I continue to improve this tool.  
I'll also be preparing a YouTube video on this, which you can find on [my YouTube channel](https://youtube.com/@diogoneves?si=C7FD8V1ElaBiTxrp).

## 🎥 Sample

Here's a video of a book with pages being turned by the wind:

![sample](https://github.com/user-attachments/assets/adfd8d9f-4966-4f63-905b-8d009bdaa6b9)  
_[Source video on Pixabay](https://pixabay.com/videos/book-wind-literature-education-185092/)_  


Let's ask a Visual LLM **"What direction the wind is blowing?"**:  
![LLM Output](https://github.com/user-attachments/assets/5e6c186d-529b-4b22-a7e1-c68256b28d8b)

### 💬 Why This Question?

This question requires understanding the flow of the video, which can only be correctly interpreted by analyzing the sequence of events.

### 📼 How is the Video Processed?

Video2Image processes the video by sampling frames at a specified rate, resizing them, and concatenating them into a single image. This image represents the flow of the video, making it possible for the LLM to analyze and respond accurately.  

![output](https://github.com/user-attachments/assets/50a4836d-a930-45f7-bc45-f991750c2c8c)

This image can also be used in any other visual LLM.  

### 💬 The Prompt Used

The generated image was then sent to a Visual Large Language Model (LLM) with the following prompt:  
**Prompt:**
```
You are observing a video. First, provide a brief sentence that explains what you observe in relation to the question. Then, answer the question directly. The input should be treated as a video.

Question: What direction is the wind blowing?
```
_See [video_gpt.py](video_gpt.py)_

## ⚙️ Setup

### 📋 Requirements

- Python 3.x
- Required Python packages: `typer`, `opencv-python-headless`, `Pillow`, `openai`

### 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DiogoNeves/Video2Image.git
   cd Video2Image
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set the OpenAI API Key**:
   Make sure you have your OpenAI API key set as an environment variable:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```

## 🚀 Usage

### Basic Usage

1. **Ask a Question About the Video**  
   Use the `video_gpt.py` script to ask a Visual LLM a question about your video. The script converts the video into an image and sends it to the LLM, which responds based on the video content.

   ```bash
   python video_gpt.py /path/to/video.mp4 "What is happening in this video?"
   ```

2. **Create Images to Use in Other Models**  
   Use the `convert_video.py` script to generate an image representing the video frames. This image can then be used with any other Visual LLM.

   ```bash
   python convert_video.py /path/to/video.mp4 --output output_image.jpg
   ```

### Advanced Usage

- **`video_gpt.py`**  
  Convert a video to an image and ask a question about the content:
  
  ```bash
  python video_gpt.py /path/to/video.mp4 "Describe the actions in this video." --max-frames 30 --fps-sampling 5
  ```

- **`convert_video.py`**  
  Generate an image from a video:
  
  ```bash
  python convert_video.py /path/to/video.mp4 --output output_image.jpg --max-frames 30 --fps-sampling 5
  ```

**Arguments:**
  - `--max-frames`: Maximum number of frames to extract from the video. Increasing this value allows processing a longer segment of the video.
  - `--fps-sampling`: Frames per second to sample from the video. Lowering this value captures a longer segment of the video with fewer frames.

### ⚠️ Important Considerations

- **Video Duration**: The duration of the video that can be processed depends on the `max_frames` and `fps_sampling` settings. The default configuration processes 2 seconds of video (20 frames at 10 fps).
  
- **Model Context Size**: Not all videos will fit within the context size of the model. Longer videos or higher frame rates may produce images too large to be fully processed by some LLMs. Adjust the parameters accordingly to ensure the output image is suitable for your model's context window.

## 🤝 Contribution

I welcome suggestions and prompt improvements! If you have ideas for how to enhance the tool or ways to make the prompts more effective, feel free to share them. Your feedback is valuable to the ongoing development of Video2Image.

## 📬 How to Reach Me

- **YouTube**: [DiogoNeves](http://www.youtube.com/@DiogoNeves)
- **Twitch**: [diogosnows](https://www.twitch.tv/diogosnows)
- **Threads**: [@diogosnows](https://www.threads.net/@diogosnows)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
