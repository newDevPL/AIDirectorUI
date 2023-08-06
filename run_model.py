
import os
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
from PIL import Image
import gradio as gr
from gradio.components import Textbox, Number, Checkbox, Slider, File

# Function to initialize the DiffusionPipeline
def initialize_diffusion_pipeline(model_name, dtype=torch.float16, chunk_size=1, dim=1):
    print(f"Initializing the pipeline with model: {model_name}")
    pipe = DiffusionPipeline.from_pretrained(model_name, torch_dtype=dtype)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.enable_model_cpu_offload()
    pipe.enable_vae_slicing()
    pipe.unet.enable_forward_chunking(chunk_size=chunk_size, dim=dim)
    return pipe

# Function to export frames to a video
def export_frames_to_video(frames, output_path):
    video_number = 1
    while os.path.exists(f"{output_path}video{video_number}.mp4"):
        video_number += 1
    video_path = export_to_video(frames, output_video_path=f"{output_path}video{video_number}.mp4")
    print(f"Video generated: {video_path}")
    return video_path

# Main function to generate videos
def generate_video(prompts=None, num_inference_steps=None, num_upscale_steps=None, height=None, width=None, upscale=None, upscaled_height=None, upscaled_width=None, num_frames=None, strength=None, output_path=None, negative_prompt=None, guidance_scale=None):
    prompts = prompts.split("\n") if prompts is not None else ["Space scenery"]
    num_inference_steps = int(num_inference_steps) if num_inference_steps is not None else 30
    num_upscale_steps = int(num_upscale_steps) if num_upscale_steps is not None else 30
    height = int(height) if height is not None else 576
    width = int(width) if width is not None else 1024
    upscale = upscale if upscale is not None else False
    upscaled_height = int(upscaled_height) if upscaled_height is not None else 576
    upscaled_width = int(upscaled_width) if upscaled_width is not None else 1024
    num_frames = int(num_frames) if num_frames is not None else 30
    strength = float(strength) if strength is not None else 0.6
    negative_prompt = negative_prompt.strip() if negative_prompt is not None else ""  # Convert to a single string
    guidance_scale = float(guidance_scale) if guidance_scale is not None else 1.0
    output_path = output_path or "./output/"

    video_paths = []

    # Create the pipeline once outside the loop
    pipe = initialize_diffusion_pipeline("cerspense/zeroscope_v2_576w")

    for i, prompt in enumerate(prompts):
        # Generate video frames
        video_frames = pipe(prompt.strip(), num_inference_steps=num_inference_steps, height=height, width=width, num_frames=num_frames, negative_prompt=negative_prompt, guidance_scale=guidance_scale).frames
        
        if upscale:
            # Clear memory before using the pipeline with larger model
            del pipe
            torch.cuda.empty_cache()

            pipe = initialize_diffusion_pipeline("cerspense/zeroscope_v2_XL")

            upscaled_size = (upscaled_width, upscaled_height)
            video = [Image.fromarray(frame).resize(upscaled_size) for frame in video_frames]

            video_frames = pipe(prompt.strip(), num_inference_steps=num_upscale_steps, video=video, strength=strength, negative_prompt=negative_prompt, guidance_scale=guidance_scale).frames
            
            video_path = export_frames_to_video(video_frames, output_path)
            video_paths.append(video_path)

            # Clear memory after using the pipeline with larger model
            del pipe
            torch.cuda.empty_cache()

            # Re-initialize the pipeline with the smaller model
            pipe = initialize_diffusion_pipeline("cerspense/zeroscope_v2_576w")
        else:
            video_path = export_frames_to_video(video_frames, output_path)
            video_paths.append(video_path)

    return ", ".join(video_paths)

inputs = [
    Textbox(lines=5, label="Prompts (one per line)", placeholder="Enter prompts here, one per line. Use Shift+Enter to create a new line without submitting."),
    Number(label="Number of Inference Steps"),
    Number(label="Number of Upscale Steps"),
    Number(label="Height"),
    Number(label="Width"),
    Checkbox(label="Upscale"),
    Number(label="Upscaled Height"),
    Number(label="Upscaled Width"),
    Number(label="Number of Frames"),
    Slider(minimum=0, maximum=1, step=0.1, label="Strength"),
    Textbox(label="Output Folder Path"),
    Textbox(label="Negative Prompt"),  # new input for negative_prompt
    Number(label="Guidance Scale"),  # new input for guidance_scale
]

iface = gr.Interface(fn=generate_video,
                     inputs=inputs,
                     outputs="text",
                     title="Video Generation",
                     description="Generate videos using zeroscope models.")
iface.launch(debug=True)
