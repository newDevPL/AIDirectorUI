
#!/bin/bash
python3 -m venv myenv
source myenv/bin/activate
pip install git+https://github.com/huggingface/diffusers.git
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers accelerate gradio
pip install opencv-python
