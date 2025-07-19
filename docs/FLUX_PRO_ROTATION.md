# FLUX 1.1 [pro] Character Rotation Generator

This module provides a specialized character rotation generator using the FLUX 1.1 [pro] API with ultra and raw mode enabled for high-quality image generation.

## Features

- **FLUX 1.1 [pro] API Integration**: Uses the latest FLUX 1.1 [pro] API endpoint
- **Ultra and Raw Mode**: Enables ultra-realistic generation with raw mode for maximum quality
- **Fixed Seed Generation**: Ensures consistency across all rotation angles
- **Base64 Image Encoding**: Efficient image transmission to the API
- **Comprehensive Error Handling**: Robust error handling with retry mechanisms
- **Progress Monitoring**: Real-time progress updates during generation
- **Flexible Angle Configuration**: Support for custom rotation angles

## Requirements

- Python 3.7+
- FLUX API key with access to FLUX 1.1 [pro]
- Input character image (JPEG/PNG format)
- Internet connection for API access

## Installation

1. Ensure you have the required dependencies:
```bash
pip install requests
```

2. Set up your FLUX API key:
```bash
export FLUX_API_KEY="your_api_key_here"
```

## Usage

### Command Line Interface

The easiest way to use the generator is through the provided shell script:

```bash
# Basic usage with default angles
./scripts/run_flux_rotation.sh -k YOUR_API_KEY

# Custom angles
./scripts/run_flux_rotation.sh -k YOUR_API_KEY -a 45 90 135

# Custom input image and output directory
./scripts/run_flux_rotation.sh -k YOUR_API_KEY -i /path/to/character.jpg -o my_rotations

# Test API connection first
./scripts/run_flux_rotation.sh -k YOUR_API_KEY -t
```

### Python Script Direct Usage

```bash
# Basic usage
python bin/generate_flux_rotation.py --api-key YOUR_API_KEY

# With custom parameters
python bin/generate_flux_rotation.py \
    --api-key YOUR_API_KEY \
    --angles 10 20 30 45 60 90 135 180 \
    --input-image /path/to/character.jpg \
    --seed 123456 \
    --output-dir rotation_output \
    --test-connection
```

### Programmatic Usage

```python
from pathlib import Path
from bin.generate_flux_rotation import FluxProRotationGenerator

# Initialize generator
generator = FluxProRotationGenerator(
    api_key="your_api_key_here",
    output_dir="rotation_output"
)

# Test connection
if generator.test_connection():
    print("API connection successful!")
    
    # Generate rotations
    results = generator.generate_all_rotations(
        angles=[10, 20, 30, 45, 60, 90, 135, 180],
        input_image_path=Path("/path/to/character.jpg"),
        seed=123456
    )
    
    # Check results
    successful = sum(1 for r in results.values() if r is not None)
    print(f"Generated {successful}/{len(results)} images successfully!")
```

## API Configuration

### Endpoint
- **URL**: `https://api.flux.run/generate/flux-1.1-pro-ultra`
- **Method**: POST
- **Content-Type**: application/json

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Text prompt describing the desired rotation |
| `input_image` | string | Yes | Base64 encoded input image with MIME type |
| `seed` | integer | Yes | Random seed for consistent generation |
| `ultra` | boolean | Yes | Enable ultra mode (set to `true`) |
| `raw` | boolean | Yes | Enable raw mode (set to `true`) |
| `aspect_ratio` | string | No | Image aspect ratio (default: "2:3") |
| `output_format` | string | No | Output format (default: "jpeg") |

### Example Request

```json
{
    "prompt": "A realistic portrait of the same woman as in the input image, rotated 45 degrees to the right, keeping her facial features and body unchanged, consistent lighting and style, ultra realistic, high detail, studio lighting",
    "input_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...",
    "seed": 123456,
    "ultra": true,
    "raw": true,
    "aspect_ratio": "2:3",
    "output_format": "jpeg"
}
```

## Prompt Engineering

The generator automatically creates optimized prompts for each rotation angle:

- **0°**: "facing forward"
- **10-89°**: "rotated X degrees to the right"
- **90°**: "facing 90 degrees to the right"
- **91-179°**: "rotated X degrees to the right"
- **180°**: "facing away, back turned"

Each prompt includes:
- Character consistency instructions
- Lighting and style consistency
- Ultra-realistic quality specifications
- Studio lighting requirements

## Output

### File Naming Convention
Generated images are saved with the naming pattern:
```
rotation_{angle}.jpg
```

Example:
- `rotation_10.jpg`
- `rotation_45.jpg`
- `rotation_90.jpg`
- `rotation_180.jpg`

### Output Directory Structure
```
rotation_output/
├── rotation_10.jpg
├── rotation_20.jpg
├── rotation_30.jpg
├── rotation_45.jpg
├── rotation_60.jpg
├── rotation_90.jpg
├── rotation_135.jpg
└── rotation_180.jpg
```

## Error Handling

The generator includes comprehensive error handling:

- **API Connection Errors**: Automatic retry with exponential backoff
- **Generation Failures**: Individual angle failures don't stop the entire process
- **Network Timeouts**: Configurable timeout settings with retry logic
- **Invalid Input**: Validation of input image and parameters
- **API Rate Limits**: Built-in rate limiting and queuing

## Performance Considerations

- **API Rate Limits**: The FLUX API has rate limits; the generator respects these
- **Generation Time**: Each image typically takes 30-60 seconds to generate
- **Concurrent Requests**: The generator processes angles sequentially to avoid rate limiting
- **Image Size**: Input images are automatically encoded to base64; large images may increase request time

## Troubleshooting

### Common Issues

1. **API Key Invalid**
   ```
   Error: Access denied. Check API key.
   ```
   Solution: Verify your FLUX API key and ensure it has access to FLUX 1.1 [pro]

2. **Input Image Not Found**
   ```
   Error: Image file not found: /path/to/character.jpg
   ```
   Solution: Check the input image path and ensure the file exists

3. **Generation Timeout**
   ```
   Error: Generation timeout exceeded after 180 attempts
   ```
   Solution: Check your internet connection and API status

4. **Rate Limit Exceeded**
   ```
   Error: Too many requests
   ```
   Solution: Wait a few minutes before retrying

### Debug Mode

Enable verbose logging by setting the log level:
```bash
export LOG_LEVEL=DEBUG
```

## Examples

See the `examples/generate_flux_rotation_example.py` file for a complete working example.

## License

This module is part of the SenteticData project. See the main LICENSE file for details. 