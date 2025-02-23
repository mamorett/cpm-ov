import warnings
import logging
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM
from pathlib import Path
import os
from tqdm import tqdm
import argparse
from dotenv import load_dotenv
from contextlib import contextmanager

# Suppress all warnings
warnings.filterwarnings('ignore')

# Configure logging to be as quiet as possible
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("auto_gptq").setLevel(logging.ERROR)
logging.getLogger("safetensors").setLevel(logging.ERROR)


def load_model_and_tokenizer():
    """Initialize the model and tokenizer."""
    model = AutoGPTQForCausalLM.from_quantized(
        'openbmb/MiniCPM-o-2_6-int4',
        torch_dtype=torch.bfloat16,
        device="cuda:0",
        trust_remote_code=True,
        disable_exllama=True,
        disable_exllamav2=True,
        use_safetensors=True
    )
    
    tokenizer = AutoTokenizer.from_pretrained(
        'openbmb/MiniCPM-o-2_6-int4',
        trust_remote_code=True
    )
    
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

def process_single_image(image_path, prompt, model, tokenizer, force=False, no_save=False):
    """Process a single image and save the result."""
    try:
        output_path = image_path.with_suffix('.txt')
        
        # Check if output file exists and skip if not forced
        if not no_save and output_path.exists() and not force:
            print(f"\nSkipping {image_path} - output file already exists")
            return True
            
        # Load and convert image
        image = Image.open(image_path).convert('RGB')
        
        # Create chat message
        msgs = [{'role': 'user', 'content': [image, prompt]}]
        
        # Get model response
        answer = model.chat(msgs=msgs, tokenizer=tokenizer)
        
        # Save response to text file if no_save is False
        if not no_save:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(answer)
            print(f"\nCreated output file: {output_path}")
        
        print(f"\nResponse for {image_path}:\n{answer}\n")
            
        return True
    except Exception as e:
        print(f"\nError processing {image_path}: {str(e)}")
        return False
    
def get_prompts():
    """Get prompts from .env file and command line arguments."""
    # Get prompts from .env
    load_dotenv()
    prompts = {}
    for key, value in os.environ.items():
        if key.endswith('_PROMPT'):
            prompt_name = key.replace('_PROMPT', '').lower().replace('_', '-')
            prompts[prompt_name] = value
    return prompts    

def main():
    # Get prompts from .env
    prompts = get_prompts_from_env()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process images with GPT model')
    parser.add_argument('path', help='Path to image file or directory')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--prompt-type', choices=list(prompts.keys()),
                       help='Type of prompt to use (defined in .env file)')
    group.add_argument('-p', '--prompt', help='Custom prompt to use')
    parser.add_argument('-f', '--force', action='store_true',
                       help='Force processing even if output file exists')
    parser.add_argument('-n', '--no-save', action='store_true',
                       help='Do not save output to text files, print to terminal only')    
    args = parser.parse_args()

        # Determine which prompt to use
    if args.prompt_type:
        selected_prompt = prompts[args.prompt_type]
    else:
        selected_prompt = args.prompt
    
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
            process_single_image(path, selected_prompt, model, tokenizer, args.force, args.no_save)
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
            if process_single_image(image_path, selected_prompt, model, tokenizer, args.force, args.no_save):
                successful += 1
                
        print(f"\nProcessing complete. Successfully processed {successful} out of {len(image_files)} images.")
    else:
        print("Invalid path. Please provide a valid image file or directory path.")

if __name__ == "__main__":
    main()