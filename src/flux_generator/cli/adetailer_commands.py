"""
CLI commands for Adetailer integration.
"""

import click
from pathlib import Path
from typing import Optional

from ..core.adetailer import AdetailerGenerator
from ..utils.logger import get_logger

logger = get_logger(__name__)


@click.group()
def adetailer():
    """Adetailer face enhancement commands."""
    pass


@adetailer.command()
@click.option('--api-key', envvar='FLUX_API_KEY', help='FLUX API key')
@click.option('--prompt', help='Custom prompt for generation')
@click.option('--seed', type=int, help='Random seed for generation')
@click.option('--aspect-ratio', default='2:3', help='Aspect ratio (default: 2:3)')
@click.option('--output-format', default='jpeg', help='Output format (default: jpeg)')
@click.option('--confidence', type=float, default=0.3, help='Face detection confidence (default: 0.3)')
@click.option('--denoising-strength', type=float, default=0.4, help='Denoising strength (default: 0.4)')
@click.option('--steps', type=int, default=20, help='Number of steps (default: 20)')
@click.option('--cfg-scale', type=float, default=7.0, help='CFG scale (default: 7.0)')
def generate(
    api_key: Optional[str],
    prompt: Optional[str],
    seed: Optional[int],
    aspect_ratio: str,
    output_format: str,
    confidence: float,
    denoising_strength: float,
    steps: int,
    cfg_scale: float
):
    """Generate a single image with Adetailer face enhancement."""
    try:
        # Initialize generator
        generator = AdetailerGenerator(api_key)
        
        # Test connection
        if not generator.test_connection():
            click.echo("❌ Failed to connect to FLUX API. Check your API key.")
            return
        
        click.echo("✅ Connected to FLUX API successfully!")
        
        # Update Adetailer settings
        adetailer_config = {
            'confidence': confidence,
            'denoising_strength': denoising_strength,
            'steps': steps,
            'cfg_scale': cfg_scale
        }
        
        # Generate image
        click.echo("🚀 Starting Adetailer generation...")
        output_path = generator.generate_with_adetailer(
            prompt=prompt,
            seed=seed,
            aspect_ratio=aspect_ratio,
            output_format=output_format,
            adetailer_config=adetailer_config
        )
        
        if output_path:
            click.echo(f"✅ Image generated successfully: {output_path}")
        else:
            click.echo("❌ Failed to generate image")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        logger.error(f"CLI error: {e}")


@adetailer.command()
@click.option('--api-key', envvar='FLUX_API_KEY', help='FLUX API key')
@click.option('--count', type=int, default=5, help='Number of images to generate (default: 5)')
@click.option('--start-seed', type=int, help='Starting seed for generation')
@click.option('--prompt', help='Custom prompt for generation')
@click.option('--aspect-ratio', default='2:3', help='Aspect ratio (default: 2:3)')
@click.option('--output-format', default='jpeg', help='Output format (default: jpeg)')
@click.option('--confidence', type=float, default=0.3, help='Face detection confidence (default: 0.3)')
@click.option('--denoising-strength', type=float, default=0.4, help='Denoising strength (default: 0.4)')
@click.option('--steps', type=int, default=20, help='Number of steps (default: 20)')
@click.option('--cfg-scale', type=float, default=7.0, help='CFG scale (default: 7.0)')
def batch(
    api_key: Optional[str],
    count: int,
    start_seed: Optional[int],
    prompt: Optional[str],
    aspect_ratio: str,
    output_format: str,
    confidence: float,
    denoising_strength: float,
    steps: int,
    cfg_scale: float
):
    """Generate multiple images with Adetailer face enhancement."""
    try:
        # Initialize generator
        generator = AdetailerGenerator(api_key)
        
        # Test connection
        if not generator.test_connection():
            click.echo("❌ Failed to connect to FLUX API. Check your API key.")
            return
        
        click.echo("✅ Connected to FLUX API successfully!")
        
        # Update Adetailer settings
        adetailer_config = {
            'confidence': confidence,
            'denoising_strength': denoising_strength,
            'steps': steps,
            'cfg_scale': cfg_scale
        }
        
        # Generate images
        click.echo(f"🚀 Starting batch Adetailer generation of {count} images...")
        output_paths = generator.generate_multiple_with_adetailer(
            count=count,
            start_seed=start_seed,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            output_format=output_format,
            adetailer_config=adetailer_config
        )
        
        if output_paths:
            click.echo(f"✅ Successfully generated {len(output_paths)} images:")
            for path in output_paths:
                click.echo(f"  📸 {path}")
        else:
            click.echo("❌ No images were generated")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        logger.error(f"CLI error: {e}")


@adetailer.command()
@click.option('--api-key', envvar='FLUX_API_KEY', help='FLUX API key')
@click.option('--input-dir', type=click.Path(exists=True), help='Input directory with images (default: data/output)')
@click.option('--file-pattern', default='*.jpg', help='File pattern to match (default: *.jpg)')
@click.option('--output-suffix', default='_adetailer', help='Suffix for enhanced images (default: _adetailer)')
@click.option('--confidence', type=float, default=0.3, help='Face detection confidence (default: 0.3)')
@click.option('--denoising-strength', type=float, default=0.4, help='Denoising strength (default: 0.4)')
@click.option('--steps', type=int, default=20, help='Number of steps (default: 20)')
@click.option('--cfg-scale', type=float, default=7.0, help='CFG scale (default: 7.0)')
def process(
    api_key: Optional[str],
    input_dir: Optional[str],
    file_pattern: str,
    output_suffix: str,
    confidence: float,
    denoising_strength: float,
    steps: int,
    cfg_scale: float
):
    """Process existing images in output directory with Adetailer enhancement."""
    try:
        # Initialize generator
        generator = AdetailerGenerator(api_key)
        
        # Test connection
        if not generator.test_connection():
            click.echo("❌ Failed to connect to FLUX API. Check your API key.")
            return
        
        click.echo("✅ Connected to FLUX API successfully!")
        
        # Update Adetailer settings
        adetailer_config = {
            'confidence': confidence,
            'denoising_strength': denoising_strength,
            'steps': steps,
            'cfg_scale': cfg_scale
        }
        
        # Process images
        input_path = Path(input_dir) if input_dir else None
        click.echo(f"🚀 Starting Adetailer processing of existing images...")
        click.echo(f"📁 Input directory: {input_path or 'data/output'}")
        click.echo(f"🔍 File pattern: {file_pattern}")
        click.echo(f"🏷️ Output suffix: {output_suffix}")
        
        output_paths = generator.process_existing_images(
            input_dir=input_path,
            file_pattern=file_pattern,
            adetailer_config=adetailer_config,
            output_suffix=output_suffix
        )
        
        if output_paths:
            click.echo(f"✅ Successfully processed {len(output_paths)} images:")
            for path in output_paths:
                click.echo(f"  📸 {path}")
        else:
            click.echo("❌ No images were processed")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        logger.error(f"CLI error: {e}")


@adetailer.command()
@click.option('--api-key', envvar='FLUX_API_KEY', help='FLUX API key')
@click.option('--files', required=True, help='Comma-separated list of image files to process')
@click.option('--output-suffix', default='_adetailer', help='Suffix for enhanced images (default: _adetailer)')
@click.option('--confidence', type=float, default=0.3, help='Face detection confidence (default: 0.3)')
@click.option('--denoising-strength', type=float, default=0.4, help='Denoising strength (default: 0.4)')
@click.option('--steps', type=int, default=20, help='Number of steps (default: 20)')
@click.option('--cfg-scale', type=float, default=7.0, help='CFG scale (default: 7.0)')
def process_files(
    api_key: Optional[str],
    files: str,
    output_suffix: str,
    confidence: float,
    denoising_strength: float,
    steps: int,
    cfg_scale: float
):
    """Process specific image files with Adetailer enhancement."""
    try:
        # Initialize generator
        generator = AdetailerGenerator(api_key)
        
        # Test connection
        if not generator.test_connection():
            click.echo("❌ Failed to connect to FLUX API. Check your API key.")
            return
        
        click.echo("✅ Connected to FLUX API successfully!")
        
        # Parse file list
        file_list = [Path(f.strip()) for f in files.split(',')]
        
        # Validate files exist
        for file_path in file_list:
            if not file_path.exists():
                click.echo(f"❌ File not found: {file_path}")
                return
        
        # Update Adetailer settings
        adetailer_config = {
            'confidence': confidence,
            'denoising_strength': denoising_strength,
            'steps': steps,
            'cfg_scale': cfg_scale
        }
        
        # Process specific files
        click.echo(f"🚀 Starting Adetailer processing of {len(file_list)} specific files...")
        click.echo(f"📁 Files to process:")
        for file_path in file_list:
            click.echo(f"  📸 {file_path}")
        click.echo(f"🏷️ Output suffix: {output_suffix}")
        
        output_paths = generator.process_specific_images(
            image_paths=file_list,
            adetailer_config=adetailer_config,
            output_suffix=output_suffix
        )
        
        if output_paths:
            click.echo(f"✅ Successfully processed {len(output_paths)} images:")
            for path in output_paths:
                click.echo(f"  📸 {path}")
        else:
            click.echo("❌ No images were processed")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        logger.error(f"CLI error: {e}")


@adetailer.command()
@click.option('--api-key', envvar='FLUX_API_KEY', help='FLUX API key')
def test(api_key: Optional[str]):
    """Test Adetailer generator connection and setup."""
    try:
        # Initialize generator
        generator = AdetailerGenerator(api_key)
        
        # Test connection
        if generator.test_connection():
            click.echo("✅ FLUX API connection successful")
        else:
            click.echo("❌ FLUX API connection failed")
            return
        
        # Get input image info
        image_info = generator.get_input_image_info()
        click.echo(f"📸 Input image: {image_info['path']}")
        click.echo(f"📏 Size: {image_info['width']}x{image_info['height']}")
        click.echo(f"💾 Format: {image_info['format']}")
        
        # Show Adetailer settings
        click.echo("\n🔧 Adetailer Settings:")
        click.echo(f"  Model: {generator.adetailer_settings.model}")
        click.echo(f"  Confidence: {generator.adetailer_settings.confidence}")
        click.echo(f"  Denoising Strength: {generator.adetailer_settings.denoising_strength}")
        click.echo(f"  Steps: {generator.adetailer_settings.steps}")
        click.echo(f"  CFG Scale: {generator.adetailer_settings.cfg_scale}")
        click.echo(f"  Sampler: {generator.adetailer_settings.sampler}")
        
        click.echo("\n✅ Adetailer generator is ready!")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        logger.error(f"CLI error: {e}")


@adetailer.command()
@click.option('--api-key', envvar='FLUX_API_KEY', help='FLUX API key')
@click.option('--confidence', type=float, help='Face detection confidence')
@click.option('--denoising-strength', type=float, help='Denoising strength')
@click.option('--steps', type=int, help='Number of steps')
@click.option('--cfg-scale', type=float, help='CFG scale')
@click.option('--sampler', help='Sampler name')
@click.option('--prompt', help='Face enhancement prompt')
@click.option('--negative-prompt', help='Negative prompt')
def configure(
    api_key: Optional[str],
    confidence: Optional[float],
    denoising_strength: Optional[float],
    steps: Optional[int],
    cfg_scale: Optional[float],
    sampler: Optional[str],
    prompt: Optional[str],
    negative_prompt: Optional[str]
):
    """Configure Adetailer settings."""
    try:
        # Initialize generator
        generator = AdetailerGenerator(api_key)
        
        # Update settings
        settings_to_update = {}
        if confidence is not None:
            settings_to_update['confidence'] = confidence
        if denoising_strength is not None:
            settings_to_update['denoising_strength'] = denoising_strength
        if steps is not None:
            settings_to_update['steps'] = steps
        if cfg_scale is not None:
            settings_to_update['cfg_scale'] = cfg_scale
        if sampler is not None:
            settings_to_update['sampler'] = sampler
        if prompt is not None:
            settings_to_update['prompt'] = prompt
        if negative_prompt is not None:
            settings_to_update['negative_prompt'] = negative_prompt
        
        if settings_to_update:
            generator.update_adetailer_settings(**settings_to_update)
            click.echo("✅ Adetailer settings updated successfully!")
        else:
            click.echo("ℹ️ No settings to update. Use --help to see available options.")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        logger.error(f"CLI error: {e}")


if __name__ == '__main__':
    adetailer() 