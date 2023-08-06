@echo off
python -m venv myenv
call myenv\Scripts\activate.bat
pip install git+https://github.com/huggingface/diffusers.git
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers accelerate gradio
pip install opencv-python

