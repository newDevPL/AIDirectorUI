
# AIDirectorUI

AIDirectorUI is a tool designed to facilitate the generation and merging of AI-created videos based on user-supplied prompts. 

## Prerequisites

- Python 3.7 or later
- Git
- pip (Python package installer)

## Installation and Usage

1. Clone the repository:
```
git clone https://github.com/newDevPL/AIDirectorUI.git
```

2. Navigate to the AIDirectorUI directory:
```
cd AIDirectorUI
```

3. Run the setup script according to your operating system:

- For Windows:
```
setup_env.bat
```

- For Linux/Mac:
```
bash setup_env.sh
```

4. Run the application:

- For Windows:
```
start.bat
```

- For Linux/Mac:
```
bash start.sh
```

## Files

- `run_model.py`: The main script that generates videos based on user prompts using the Zeroscope AI model.
- `mergevideo.py`: A script that merges multiple videos into one.
- `setup_env.bat/setup_env.sh`: A script to set up the Python virtual environment and install required dependencies.
- `start.bat/start.sh`: A script to start the Gradio interface.

## Notes

- When using the Gradio interface, you can enter multiple prompts, one per line. Press Shift+Enter to create a new line without submitting.
- Videos will be saved in the output directory as `video1.mp4`, `video2.mp4`, etc.
- You can use the following Google Colab if you don't have a GPU or prefer to use cloud computing: https://colab.research.google.com/drive/1tpcGri9uHT0-xxD9U2N_lDcZQwTODJt4#scrollTo=outvcWX55A2o
