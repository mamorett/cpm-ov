import warnings
import logging
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
from contextlib import contextmanager
import io
from ctransformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path
import os
from tqdm import tqdm
import argparse
from dotenv import load_dotenv
import sys
from contextlib import contextmanager
import io

# Suppress all warnings
warnings.filterwarnings('ignore')

# Configure logging to be as quiet as possible
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("safetensors").setLevel(logging.ERROR)

# Context manager to suppress stdout and stderr
@contextmanager
def suppress_output():
    # Save the original stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    # Create string buffers to catch output
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    try:
        # Redirect stdout and stderr
        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer
        yield
    finally:
        # Restore stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr


def load_model_and_tokenizer():
    """Initialize the model and tokenizer."""
    # with suppress_output():
    model = AutoModelForCausalLM.from_pretrained(
        '/gorgon/ia/MiniCPM-o-2_6-Q6_K.gguf',
        model_type='llama',  # or whatever model type you're using
        gpu_layers=99  # adjust based on your GPU memory
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model)
    
    return model, tokenizer

def get_prompts_from_env():
    """Get all prompts from .env file that end with _PROMPT."""
    load_dotenv()
    prompts = {}
    for key, value in os.environ.items():
        if key.endswith('_PROMPT'):
            prompt_name = key.replace('_PROMPT', '').lower().replace('_', '-')
            prompts[prompt_name] = value
    return prompts

def process_single_image(image_path, prompt, model, tokenizer, force=False):
    """Process a single image and save the result."""
    try:
        output_path = image_path.with_suffix('.txt')
        
        # Check if output file exists and skip if not forced
        if output_path.exists() and not force:
            print(f"\nSkipping {image_path} - output file already exists")
            return True
            
        # Load and convert image
        image = Image.open(image_path).convert('RGB')
        
        # Create chat message
        msgs = [{'role': 'user', 'content': [image, prompt]}]
        
        # Get model response
        with suppress_output():
            answer = model.chat(msgs=msgs, tokenizer=tokenizer)
        
        # Save response to text file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(answer)
        
        print(f"\nCreated output file: {output_path}")
        print(f"Content written:\n{answer}\n")
            
        return True
    except Exception as e:
        print(f"\nError processing {image_path}: {str(e)}")
        return False

def main():
    # Get prompts from .env
    prompts = get_prompts_from_env()
    
    if not prompts:
        print("No prompts found in .env file. Please add prompts with _PROMPT suffix.")
        return
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process images with GPT model')
    parser.add_argument('path', help='Path to image file or directory')
    parser.add_argument('--prompt-type', choices=list(prompts.keys()),
                       required=True, help='Type of prompt to use')
    parser.add_argument('-f', '--force', action='store_true',
                       help='Force processing even if output file exists')
    args = parser.parse_args()
    
    selected_prompt = prompts[args.prompt_type]
    
    # Initialize model and tokenizer
    print("Initializing model and tokenizer...")
    model, tokenizer = load_model_and_tokenizer()
    print("Initialization complete!")
    
    # Process path
    path = Path(args.path)
    if path.is_file():
        # Single file processing
        if path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
            print(f"Processing single image: {path}")
            process_single_image(path, selected_prompt, model, tokenizer, args.force)
    elif path.is_dir():
        # Directory processing
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.webp']:
            image_files.extend(path.glob(ext))
            image_files.extend(path.glob(ext.upper()))  # Also match uppercase extensions
        
        if not image_files:
            print("No image files found in directory")
            return
            
        # Count files that need processing
        if not args.force:
            to_process = [f for f in image_files if not f.with_suffix('.txt').exists()]
            skipped = len(image_files) - len(to_process)
            if skipped > 0:
                print(f"Found {len(image_files)} images, skipping {skipped} with existing output files")
            image_files = to_process
            
        if not image_files:
            print("No images require processing (all have existing output files)")
            return
            
        print(f"Processing {len(image_files)} images")
        successful = 0
        
        # Process all images with progress bar
        for image_path in tqdm(image_files, desc="Processing images"):
            if process_single_image(image_path, selected_prompt, model, tokenizer, args.force):
                successful += 1
                
        print(f"\nProcessing complete. Successfully processed {successful} out of {len(image_files)} images.")
    else:
        print("Invalid path. Please provide a valid image file or directory path.")

if __name__ == "__main__":
    main()