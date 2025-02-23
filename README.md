<div align="center">
<pre>
 ████  ██████ ██   ██         ████  ██  ██ 
██     ██  ██ ███ ███        ██  ██ ██  ██ 
██     ██████ ██ █ ██ ██████ ██  ██ ██  ██ 
██     ██     ██   ██        ██  ██  ████  
 ████  ██     ██   ██         ████    ██   
</pre>
</div>
<p align="center">
	<em>Generate Text with Style: MiniCPM-o</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/mamorett/cpm-ov?style=flat-square&logo=opensourceinitiative&logoColor=white&color=8a2be2" alt="license">
	<img src="https://img.shields.io/github/last-commit/mamorett/cpm-ov?style=flat-square&logo=git&logoColor=white&color=8a2be2" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/mamorett/cpm-ov?style=flat-square&color=8a2be2" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/mamorett/cpm-ov?style=flat-square&color=8a2be2" alt="repo-language-count">
</p>
<p align="center">Built with the tools and technologies:</p>
<p align="center">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">
</p>
<br>

##  Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
  - [Project Index](#project-index)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration to use prompt Type](#configuration-to-use-prompt-type)
- [Usage](#usage)
  - [Single Image Processing](#single-image-processing)
  - [Directory Processing](#directory-processing)
  - [Force Processing](#force-processing)
- [Output](#output)
- [Command Line Arguments](#command-line-arguments)
- [Usage](#usage-1)
  - [Single Image Processing](#single-image-processing-1)
  - [Directory Processing](#directory-processing-1)
  - [Force Processing](#force-processing-1)
- [Output](#output-1)
- [Command Line Arguments](#command-line-arguments-1)
- [Usage](#usage-2)
  - [Single Image Processing](#single-image-processing-2)
  - [Directory Processing](#directory-processing-2)
  - [Force Processing](#force-processing-2)
  - [Print Response to Terminal](#print-response-to-terminal)
- [Output](#output-2)
- [Command Line Arguments](#command-line-arguments-2)
- [Error Handling](#error-handling)
- [Notes](#notes)
- [Example Workflow](#example-workflow)
- [Project Roadmap](#project-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

##  Overview

The cpm-ov project is an open-source AI-powered image-to-text generation tool that leverages the int4 quantized version of [**MiniCPM-o 2.6**](https://huggingface.co/openbmb/MiniCPM-o-2_6) model to generate text based on input images.   
Running with int4 version would use lower GPU memory (about 9GB). MiniCPM-o is the latest series of end-side multimodal LLMs (MLLMs) ungraded from MiniCPM-V. The models can now take images, video, text, and audio as inputs and provide high-quality text and speech outputs in an end-to-end fashion. This script processes images using the [MiniCPM-o-2_6-int4](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4) model to generate text descriptions based on customizable prompts. It can handle both single images and directories, supporting various image formats including JPG, JPEG, PNG, BMP, and WebP.

---

##  Features

- Process single images or entire directories
- Customizable prompts via environment variables
- Support for multiple image formats (JPG, JPEG, PNG, BMP, WebP)
- Skip existing processed files with option to force reprocessing
- Progress bar for directory processing
- Detailed output logging

---

##  Project Structure

```sh
└── cpm-ov/
    ├── LICENSE
    ├── README.md
    ├── minicpm-o.py
    └── requirements.txt
```


###  Project Index
<details open>
	<summary><b><code>CPM-OV/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/mamorett/cpm-ov/blob/master/requirements.txt'>requirements.txt</a></b></td>
				<td>- The provided `requirements.txt` file specifies the dependencies required to run the codebase, including Pillow, torch, torchaudio, torchvision, transformers, sentencepiece, vector-quantize-pytorch, vocos, accelerate, timm, soundfile, librosa, decord, and moviepy<br>- These dependencies are necessary for the code to function properly and ensure that all necessary packages are installed before running the code.</td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/mamorett/cpm-ov/blob/master/minicpm-o.py'>minicpm-o.py</a></b></td>
				<td>- This file is a Python script that uses the MiniCPM-o model to generate text based on an input image<br>- It takes an image path as an argument and generates a text file with the same name but a .txt extension in the same directory<br>- The generated text is based on the prompts defined in the .env file, which are loaded using the load_dotenv() function<br>- The script uses the AutoGPTQForCausalLM model to generate the text<br>- It also includes an argument parser to allow for customization of the input image path and the type of prompt used.</td>
			</tr>
			</table>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with cpm-ov, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python version 3.11
- **Package Manager:** Pip

###  Installation

Install cpm-ov using one of the following methods:

**Build from source:**

1. Clone the cpm-ov repository:
```sh
❯ git clone https://github.com/mamorett/cpm-ov
```

2. Navigate to the project directory:
```sh
❯ cd cpm-ov
```

3. Prepare code and install AutoGPTQ
   
```python
git clone https://github.com/OpenBMB/AutoGPTQ.git && cd AutoGPTQ
git checkout minicpmo

# install AutoGPTQ
pip install -vvv --no-build-isolation -e .
```

4. Install the project dependencies:


**Using `pip`** &nbsp; [<img align="center" src="" />]()

```sh
❯ echo 'pip install -r requirements.txt'
```

## Configuration to use prompt Type

If you plan to use Prompt Type then:

1. Create a `.env` file in the script directory
2. Add your prompts with the `_PROMPT` suffix:

```env
DESCRIBE_IMAGE_PROMPT="Describe what you see in this image"
TECHNICAL_ANALYSIS_PROMPT="Provide a technical analysis of this image"
ARTISTIC_REVIEW_PROMPT="Review this image from an artistic perspective"
# Add as many prompts as needed
```

The prompt names will be automatically converted to command-line arguments:
- `DESCRIBE_IMAGE_PROMPT` becomes `--prompt-type describe-image`
- `TECHNICAL_ANALYSIS_PROMPT` becomes `--prompt-type technical-analysis`

Here's the updated README section:

## Usage

### Single Image Processing

```bash
python minicpm-o.py path/to/image.jpg -t describe-image
```

Alternatively, you can use a custom prompt:

```bash
python minicpm-o.py path/to/image.jpg -p "Custom prompt to describe the image"
```

### Directory Processing

```bash
python minicpm-o.py path/to/image/directory -t technical-analysis
```

Alternatively, you can use a custom prompt:

```bash
python minicpm-o.py path/to/image/directory -p "Custom prompt for technical analysis"
```

### Force Processing

To process files even if output already exists:

```bash
python minicpm-o.py path/to/images -t describe-image -f
```

Or with a custom prompt:

```bash
python minicpm-o.py path/to/images -p "Custom prompt" -f
```

## Output

- For each processed image, a corresponding `.txt` file is created in the same directory
- The script shows progress and results during processing
- Existing output files are skipped unless force flag (-f) is used

## Command Line Arguments

- `path`: Path to image file or directory (required)
- `-t, --prompt-type`: Type of prompt to use (defined in .env file) (mutually exclusive with `-p, --prompt`)
- `-p, --prompt`: Custom prompt to use (mutually exclusive with `-t, --prompt-type`)
- `-f, --force`: Force processing even if output file exists

From other sources:

Claude 3.5 Sonnet, GPT-4o



Here's the updated README section:

## Usage

### Single Image Processing

Using a prompt type from .env file:
```bash
python minicpm-o.py path/to/image.jpg -t describe-image
# or
python minicpm-o.py path/to/image.jpg --prompt-type describe-image
```

Using a custom prompt:
```bash
python minicpm-o.py path/to/image.jpg -p "Describe this image in detail"
# or
python minicpm-o.py path/to/image.jpg --prompt "Describe this image in detail"
```

### Directory Processing

Using a prompt type from .env file:
```bash
python minicpm-o.py path/to/image/directory -t technical-analysis
```

Using a custom prompt:
```bash
python minicpm-o.py path/to/image/directory -p "Analyze the technical aspects of this image"
```

### Force Processing

To process files even if output already exists:

```bash
python minicpm-o.py path/to/images -t describe-image -f
# or
python minicpm-o.py path/to/images -p "Describe this image" -f
```

## Output

- For each processed image, a corresponding `.txt` file is created in the same directory
- The script shows progress and results during processing
- Existing output files are skipped unless force flag (-f) is used

## Command Line Arguments

- `path`: Path to image file or directory (required)
- `-t, --prompt-type`: Type of prompt to use from .env file
- `-p, --prompt`: Custom prompt to use
- `-f, --force`: Force processing even if output file exists

Note: Either `-t/--prompt-type` or `-p/--prompt` must be specified, but not both simultaneously.

## Usage

### Single Image Processing

You can process a single image by specifying the path to the image and using either a prompt type from the `.env` file or a custom prompt directly.

Using a prompt type from the `.env` file:
```bash
python minicpm-o.py path/to/image.jpg -t describe-image
```

Using a custom prompt directly:
```bash
python minicpm-o.py path/to/image.jpg -p "Describe the main features of this image"
```

### Directory Processing

You can process all images in a directory by specifying the path to the directory and using either a prompt type from the `.env` file or a custom prompt directly.

Using a prompt type from the `.env` file:
```bash
python minicpm-o.py path/to/image/directory -t technical-analysis
```

Using a custom prompt directly:
```bash
python minicpm-o.py path/to/image/directory -p "Provide a technical analysis of these images"
```

### Force Processing

To process files even if the output already exists, use the `-f` or `--force` flag:

Using a prompt type from the `.env` file:
```bash
python minicpm-o.py path/to/images -t describe-image -f
```

Using a custom prompt directly:
```bash
python minicpm-o.py path/to/images -p "Describe the main features of these images" -f
```

### Print Response to Terminal

To print the response directly to the terminal instead of saving to a file:

```bash
python minicpm-o.py path/to/image.jpg -t describe-image --no-save
```

## Output

- For each processed image, a corresponding `.txt` file is created in the same directory unless `--no-save` is used
- The script shows progress and results during processing
- Existing output files are skipped unless force flag (-f) is used

## Command Line Arguments

- `path`: Path to image file or directory (required)
- `-t, --prompt-type`: Type of prompt to use (defined in .env file) (mutually exclusive with `-p, --prompt`)
- `-p, --prompt`: Custom prompt to use (mutually exclusive with `-t, --prompt-type`)
- `-f, --force`: Force processing even if output file exists
- `-n, --no-save`: Print response to terminal instead of saving to file
- `-q, --quiet`: Suppress model response output when saving to files.

## Error Handling

- Invalid paths or unsupported file types are caught and reported
- Processing errors for individual images are logged without stopping the entire process
- Detailed error messages are provided for troubleshooting

## Notes

- The script suppresses model loading messages for cleaner output
- Progress bar shows real-time processing status for directory operations
- Skipped files (due to existing output) are reported in the summary

## Example Workflow

1. Set up your prompts in `.env`:
```env
DESCRIBE_IMAGE_PROMPT="Provide a detailed description of this image"
```

2. Run the script:
```bash
python minicpm-o.py ~/images/vacation --prompt-type describe-image
```

3. Check the output:
```bash
Found 50 images, skipping 10 with existing output files
Processing 40 images
[========================================] 40/40
Processing complete. Successfully processed 40 out of 40 images.
```

4. Find the results in `.txt` files next to your images


---
##  Project Roadmap

- [X] **`Task 1`**: <strike>Directory process.</strike>
- [ ] **`Task 2`**: GPTQModel support, once [PR](https://github.com/ModelCloud/GPTQModel/pull/1116) will be approved and merged.
- [ ] **`Task 3`**: API integration with text2img services.

---

##  Contributing

- **💬 [Join the Discussions](https://github.com/mamorett/cpm-ov/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/mamorett/cpm-ov/issues)**: Submit bugs found or log feature requests for the `cpm-ov` project.
- **💡 [Submit Pull Requests](https://github.com/mamorett/cpm-ov/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/mamorett/cpm-ov
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/mamorett/cpm-ov/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=mamorett/cpm-ov">
   </a>
</p>
</details>

---

##  License

This project is protected under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/) License. For more details, refer to the [LICENSE](./LICENSE) file.

---

##  Acknowledgments

- [MiniCPM-o-2_6#usage](https://huggingface.co/openbmb/MiniCPM-o-2_6#usage)

---
