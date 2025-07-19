"""
CLI commands for FLUX Image Generator.
"""

import click
from pathlib import Path
from typing import Optional

from ..core.generator import FluxImageGenerator
from ..core.enhanced import EnhancedFluxGenerator
from ..core.tester import PromptTester
from ..config.settings import settings
from ..config.prompts import PromptConfig
from ..utils.logger import setup_logger
from ..utils.image import ImageUtils


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--quiet', '-q', is_flag=True, help='Suppress output')
def cli(verbose: bool, quiet: bool):
    """FLUX Image Generator CLI."""
    # Setup logging
    log_level = 'DEBUG' if verbose else 'INFO'
    if quiet:
        log_level = 'ERROR'
    
    setup_logger(level=log_level)


@cli.command()
@click.option('--count', '-c', default=None, type=int, help='Number of images to generate')
@click.option('--seed', '-s', default=None, type=int, help='Starting seed value')
@click.option('--prompt', '-p', help='Custom prompt for generation')
@click.option('--aspect-ratio', '-a', help='Aspect ratio (portrait, square, landscape, wide)')
@click.option('--format', '-f', help='Output format (jpeg, png)')
def generate(count: Optional[int], seed: Optional[int], prompt: Optional[str], 
             aspect_ratio: Optional[str], format: Optional[str]):
    """Generate images using basic generator."""
    try:
        generator = FluxImageGenerator()
        
        # Test connection first
        click.echo("Testing API connection...")
        if not generator.test_connection():
            click.echo("❌ API connection failed. Check your API key.")
            return
        
        click.echo("✅ API connection successful")
        
        # Generate images
        images = generator.generate_images(
            count=count,
            start_seed=seed,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            output_format=format
        )
        
        click.echo(f"✅ Generated {len(images)} images")
        for image_path in images:
            click.echo(f"  📁 {image_path}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.option('--style', '-s', help='Style to use for generation')
@click.option('--count', '-c', default=5, type=int, help='Number of images per style')
@click.option('--compare', is_flag=True, help='Generate comparison across styles')
@click.option('--list-styles', is_flag=True, help='List available styles')
@click.option('--use-case', help='Find styles suitable for specific use case')
@click.option('--technical-spec', help='Find styles by technical specification (format: type:value)')
@click.option('--style-info', help='Show detailed information about specific style')
def enhanced(style: Optional[str], count: int, compare: bool, list_styles: bool, 
             use_case: Optional[str], technical_spec: Optional[str], style_info: Optional[str]):
    """Generate images using enhanced generator with precision-focused prompts."""
    try:
        if list_styles:
            styles = PromptConfig.list_available_styles()
            click.echo("Available styles with use cases:")
            for style_info in styles:
                click.echo(f"  {style_info['key']}: {style_info['name']}")
                click.echo(f"    Description: {style_info['description']}")
                click.echo(f"    Use Case: {style_info['use_case']}")
                click.echo()
            return
        
        if use_case:
            generator = EnhancedFluxGenerator()
            matching_styles = generator.find_styles_by_use_case(use_case)
            click.echo(f"Styles suitable for '{use_case}':")
            for style_data in matching_styles:
                click.echo(f"  {style_data['style']}: {style_data['name']} - {style_data['description']}")
                click.echo(f"    Use Case: {style_data['use_case']}")
                click.echo()
            return
        
        if technical_spec:
            if ':' not in technical_spec:
                click.echo("❌ Technical spec must be in format 'type:value' (e.g., 'lighting:dramatic')")
                return
            
            spec_type, spec_value = technical_spec.split(':', 1)
            generator = EnhancedFluxGenerator()
            matching_styles = generator.find_styles_by_technical_spec(spec_type, spec_value)
            click.echo(f"Styles with {spec_type} = '{spec_value}':")
            for style_data in matching_styles:
                click.echo(f"  {style_data['style']}: {style_data['name']} - {style_data['description']}")
                click.echo(f"    Technical Specs: {style_data['technical_specs']}")
                click.echo()
            return
        
        if style_info:
            try:
                info = PromptConfig.get_style_info(style_info)
                click.echo(f"Style Information: {info['name']}")
                click.echo(f"Description: {info['description']}")
                click.echo(f"Use Case: {info['use_case']}")
                click.echo(f"Technical Specs: {info['technical_specs']}")
                click.echo(f"Prompt: {info['prompt']}")
            except ValueError as e:
                click.echo(f"❌ {e}")
            return
        
        generator = EnhancedFluxGenerator()
        
        if compare:
            # Generate comparison with new styles
            styles_to_compare = ["ultra_realistic", "cinematic", "artistic"]
            click.echo(f"Generating comparison across {len(styles_to_compare)} styles...")
            
            for style_name in styles_to_compare:
                click.echo(f"Generating {count} images in {style_name} style...")
                generator.set_style(style_name)
                images = generator.generate_images(count)
                click.echo(f"  ✅ Generated {len(images)} {style_name} images")
        else:
            # Single style generation
            if style:
                generator.set_style(style)
            
            # Show current style info
            current_info = generator.get_style_info()
            click.echo(f"Generating {count} images in {current_info['name']} style...")
            click.echo(f"Use Case: {current_info['use_case']}")
            
            images = generator.generate_images(count)
            click.echo(f"✅ Generated {len(images)} images")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.option('--prompt', '-p', help='Specific prompt to test')
@click.option('--all', is_flag=True, help='Test all prompts')
@click.option('--count', '-c', default=1, type=int, help='Images per prompt')
def test(prompt: Optional[str], all: bool, count: int):
    """Test prompts with different rotations."""
    try:
        tester = PromptTester()
        
        if all:
            click.echo("Testing all prompts...")
            results = tester.test_all_prompts(images_per_prompt=count)
            click.echo(f"✅ Tested {len(results)} prompts")
        elif prompt:
            click.echo(f"Testing prompt: {prompt}")
            results = tester.test_prompt(prompt, count=count)
            click.echo(f"✅ Generated {len(results)} images for prompt")
        else:
            click.echo("Available test prompts:")
            for i, test_prompt in enumerate(tester.test_prompts, 1):
                click.echo(f"  {i}. {test_prompt}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.option('--show', is_flag=True, help='Show current configuration')
@click.option('--set', 'set_key', help='Set configuration key')
@click.option('--value', help='Value for configuration key')
@click.option('--reset', is_flag=True, help='Reset to default configuration')
def config(show: bool, set_key: Optional[str], value: Optional[str], reset: bool):
    """Manage configuration."""
    try:
        if show:
            click.echo("Current configuration:")
            click.echo(f"  API Key: {'*' * 10 if settings.api_key else 'Not set'}")
            click.echo(f"  Base URL: {settings.api.base_url}")
            click.echo(f"  Default Count: {settings.generation.default_count}")
            click.echo(f"  Default Seed: {settings.generation.default_seed}")
            click.echo(f"  Default Aspect Ratio: {settings.generation.default_aspect_ratio}")
            click.echo(f"  Input Directory: {settings.paths.input_dir}")
            click.echo(f"  Output Directory: {settings.paths.output_dir}")
            
        elif set_key and value:
            # This would require implementing configuration setters
            click.echo(f"Setting {set_key} = {value}")
            click.echo("Configuration setting not yet implemented")
            
        elif reset:
            # Reset to defaults
            settings.save_to_file()
            click.echo("Configuration reset to defaults")
            
        else:
            click.echo("Use --show to view configuration")
            click.echo("Use --set KEY --value VALUE to set configuration")
            click.echo("Use --reset to reset to defaults")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
def info():
    """Show system information."""
    try:
        click.echo("FLUX Image Generator - System Information")
        click.echo("=" * 50)
        
        # Check input image
        input_image = ImageUtils.find_input_image(settings.paths.input_dir)
        if input_image:
            info = ImageUtils.get_image_info(input_image)
            click.echo(f"✅ Input Image: {info['path']}")
            click.echo(f"   Size: {info['size_mb']} MB")
            click.echo(f"   Format: {info['extension']}")
        else:
            click.echo("❌ Input image not found")
        
        # Check API connection
        try:
            generator = FluxImageGenerator()
            if generator.test_connection():
                click.echo("✅ API Connection: Working")
            else:
                click.echo("❌ API Connection: Failed")
        except Exception as e:
            click.echo(f"❌ API Connection: Error - {e}")
        
        # Check directories
        click.echo(f"📁 Input Directory: {settings.paths.input_dir}")
        click.echo(f"📁 Output Directory: {settings.paths.output_dir}")
        click.echo(f"📁 Config Directory: {settings.paths.config_dir}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")


def main():
    """Main CLI entry point."""
    cli()


if __name__ == "__main__":
    main() 