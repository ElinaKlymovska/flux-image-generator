# Enhanced Character Rotation

## Overview

The Enhanced Character Rotation system integrates Black Forest Labs best practices to provide superior character consistency and identity preservation across all rotation angles. This system uses specialized presets optimized for the FLUX.1 Kontext [pro] model.

## Key Features

### 🎯 Character Consistency
- **Identity Preservation**: Maintains facial features, hairstyle, and distinctive characteristics
- **Cross-Angle Consistency**: Ensures the same character appears across all rotation angles
- **Professional Quality**: 8K resolution with optimized lighting and composition

### 🎨 Preset System
- **Specialized Presets**: 8 rotation-specific presets optimized for FLUX.1 Kontext [pro]
- **Best Practices Integration**: Incorporates Black Forest Labs documentation recommendations
- **Flexible Configuration**: Support for custom prompts with preset optimization

### 🔧 Advanced Controls
- **Character-Consistent Generation**: New method for maintaining character identity
- **Preset-Based Generation**: Direct preset usage for optimal results
- **Custom Preset Integration**: Combine custom prompts with preset optimization

## Available Rotation Presets

| Preset | Description | Use Case |
|--------|-------------|----------|
| `rotation_front` | Front view with identity preservation | Professional headshots, character reference |
| `rotation_left` | Left view with character consistency | Dynamic portraits, character rotation |
| `rotation_right` | Right view with character consistency | Dynamic portraits, character rotation |
| `rotation_back` | Back view with distinctive features preservation | Artistic portraits, character rotation |
| `rotation_profile_left` | Left profile with facial profile preservation | Profile portraits, character rotation |
| `rotation_profile_right` | Right profile with facial profile preservation | Profile portraits, character rotation |
| `rotation_three_quarter_left` | Three-quarter left with identity preservation | Classic portraits, character rotation |
| `rotation_three_quarter_right` | Three-quarter right with identity preservation | Classic portraits, character rotation |

## Usage Examples

### Basic Character-Consistent Rotation

```python
from flux_generator.core.rotation import CharacterRotationGenerator

# Initialize generator
generator = CharacterRotationGenerator(output_subdir="enhanced_rotation")

# Generate character-consistent rotation
results = generator.generate_character_consistent_rotation(
    angles=["front", "left", "back", "right"],
    base_prompt="portrait of a woman with long brown hair and green eyes",
    seed=1001,
    use_presets=True
)

print(f"Generated {len(results)} character-consistent images")
```

### Using Specific Presets

```python
# Generate with specific preset
result = generator.generate_rotation_with_preset(
    angle="front",
    preset="rotation_front",
    custom_prompt="portrait of a woman wearing a red dress",
    seed=2001
)

if result:
    print(f"Generated image: {result}")
```

### Full Rotation with Presets

```python
# Generate full rotation sequence with presets
results = generator.generate_full_rotation(
    angles=["front", "left", "back", "right"],
    custom_prompt="portrait of a woman in professional attire",
    use_presets=True
)

successful = sum(1 for r in results.values() if r is not None)
print(f"Generated {successful}/{len(results)} images")
```

## Command Line Usage

### Basic Enhanced Rotation

```bash
# Character-consistent rotation with presets
python bin/generate_rotation.py --angles front left back right --use-presets

# With custom character description
python bin/generate_rotation.py --angles front left back right \
    --custom-prompt "portrait of a woman with long brown hair and green eyes" \
    --use-presets
```

### 360-Degree Sequence

```bash
# 8-step rotation with character consistency
python bin/generate_rotation.py --steps 8 \
    --custom-prompt "portrait of a woman in professional attire" \
    --use-presets
```

### Preset Information

```bash
# List available presets
python bin/generate_rotation.py --list-presets

# Show preset details
python bin/generate_rotation.py --preset-info rotation_front
```

### Enhanced Script Usage

```bash
# Use the enhanced rotation script
./scripts/run_enhanced_rotation.sh --angles front,left,back,right \
    --custom-prompt "portrait of a woman with brown hair"

# 360-degree sequence
./scripts/run_enhanced_rotation.sh --steps 8 \
    --custom-prompt "portrait of a woman in professional attire"

# List presets
./scripts/run_enhanced_rotation.sh --list-presets
```

## Black Forest Labs Best Practices

### Character Consistency Framework

The enhanced rotation system implements the character consistency framework from Black Forest Labs documentation:

1. **Establish Reference**: Begin with clear character identification
2. **Specify Transformation**: Clearly state what aspects are changing
3. **Preserve Identity Markers**: Explicitly mention what should remain consistent
4. **Use Specific Language**: Avoid vague references like "her" or "it"

### Prompt Optimization

- **Identity Preservation**: "maintain exact facial features, eye color, and distinctive characteristics"
- **Character Consistency**: "while preserving identity and personality"
- **Specific Descriptions**: "the woman with long brown hair" instead of "her"

### Technical Specifications

- **Resolution**: 8K for professional quality
- **Lighting**: Optimized for each rotation angle
- **Composition**: Professional portrait angles
- **Quality Settings**: High-quality generation parameters

## API Integration

### FLUX.1 Kontext [pro] Model

The enhanced rotation system is specifically optimized for the FLUX.1 Kontext [pro] model:

- **Endpoint**: `/flux-kontext-pro`
- **Image-to-Image**: Uses input image as reference
- **Character Consistency**: Leverages model's iterative editing capabilities
- **Quality Parameters**: Optimized safety tolerance and prompt upsampling

### Request Parameters

```python
# Example request structure
request = GenerationRequest.from_image_file(
    prompt="Front-facing portrait of a woman, maintain exact facial features...",
    image_path=input_image,
    seed=1001,
    aspect_ratio="2:3",
    output_format="jpeg",
    prompt_upsampling=True,
    safety_tolerance=1
)
```

## Performance Considerations

### API Stability
- **Request Delays**: 3-second delays between requests for better stability
- **Error Handling**: Comprehensive error handling and retry logic
- **Connection Testing**: Built-in API connection testing

### Quality vs Speed
- **Preset Usage**: Faster generation with optimized presets
- **Character Consistency**: Slightly longer generation time for better results
- **Batch Processing**: Efficient handling of multiple rotation angles

## Troubleshooting

### Common Issues

1. **Character Identity Changes Too Much**
   - Use more specific identity markers in prompts
   - Enable presets for better consistency
   - Use character-consistent rotation method

2. **Inconsistent Results**
   - Ensure consistent base prompts across angles
   - Use the same seed for related generations
   - Enable preset usage for optimized results

3. **API Connection Issues**
   - Test connection before generation
   - Check API key configuration
   - Verify network connectivity

### Best Practices

1. **Start Simple**: Begin with basic character descriptions
2. **Iterate Gradually**: Build complexity step by step
3. **Use Presets**: Leverage optimized preset configurations
4. **Test Connection**: Always test API connection first
5. **Monitor Results**: Check generated images for consistency

## Migration from Legacy Rotation

### Backward Compatibility

The enhanced rotation system maintains full backward compatibility:

```python
# Legacy method still works
results = generator.generate_full_rotation(
    angles=["front", "left", "back", "right"],
    style="ultra_realistic",
    use_presets=False  # Disable presets for legacy behavior
)
```

### Migration Steps

1. **Enable Presets**: Set `use_presets=True` for better results
2. **Update Prompts**: Use character-specific descriptions
3. **Test Consistency**: Verify character consistency across angles
4. **Optimize Parameters**: Adjust quality settings as needed

## Future Enhancements

### Planned Features

- **Advanced Presets**: More specialized rotation presets
- **Style Transfer**: Rotation with style preservation
- **Batch Optimization**: Improved batch processing
- **Quality Metrics**: Automated quality assessment

### Integration Opportunities

- **Web Interface**: GUI for rotation generation
- **API Endpoints**: REST API for rotation services
- **Cloud Integration**: Cloud-based rotation processing
- **Real-time Generation**: Live rotation preview 