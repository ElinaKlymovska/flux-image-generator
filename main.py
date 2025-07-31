"""
Main CLI for FLUX Image Generator.

This script provides a command-line interface to interact with the various
image generation modules.
"""

import sys
from pathlib import Path

# Add src to path if running from root
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.flux_generator import (
        FluxImageGenerator,
        EnhancedFluxGenerator,
        CharacterRotationGenerator,
        AdetailerGenerator
    )
    from src.flux_generator.utils.logger import get_logger
except ImportError:
    print("❌ Error: Could not import generator modules.")
    print("   Please ensure you are running this script from the project root directory,")
    print("   or that the 'src' directory is in your PYTHONPATH.")
    sys.exit(1)

logger = get_logger("main_cli")


class CLI:
    """Command-Line Interface for the SenteticData Generator."""

    def __init__(self):
        """Initialize the CLI and load the generators."""
        self.flux_generator = None
        self.enhanced_generator = None
        self.rotation_generator = None
        self.adetailer_generator = None
        self._initialize_generators()

    def _initialize_generators(self):
        """Safely initialize all image generators."""
        try:
            print("🚀 Initializing generators...")
            self.flux_generator = FluxImageGenerator()
            self.enhanced_generator = EnhancedFluxGenerator()
            self.rotation_generator = CharacterRotationGenerator()
            self.adetailer_generator = AdetailerGenerator()
            print("✅ All generators initialized successfully!")
        except FileNotFoundError as e:
            logger.error(f"❌ Initialization failed: {e}")
            print(f"❌ Critical Error: {e}")
            print("   Please make sure the 'data/input/character.jpg' file exists.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"❌ An unexpected error occurred during initialization: {e}")
            print(f"❌ An unexpected error occurred: {e}")
            sys.exit(1)

    def run(self):
        """Start the main CLI loop."""
        while True:
            self._show_main_menu()
            choice = input("👉 Enter your choice: ").strip()
            
            if choice == '1':
                self._handle_flux_generator_menu()
            elif choice == '2':
                self._handle_enhanced_generator_menu()
            elif choice == '3':
                self._handle_rotation_generator_menu()
            elif choice == '4':
                self._handle_adetailer_generator_menu()
            elif choice == '5':
                self._test_connection()
            elif choice.lower() in ['q', 'quit', 'exit']:
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice, please try again.")

    def _show_main_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("🖼️  SenteticData FLUX Image Generator")
        print("="*50)
        print("1. Basic Generator")
        print("2. Enhanced Generator (Styles, Quality, etc.)")
        print("3. Character Rotation Generator")
        print("4. Adetailer (Face Enhancement)")
        print("5. Test API Connection")
        print("q. Quit")
        print("-"*50)

    def _handle_flux_generator_menu(self):
        """Handle the menu for the basic FluxImageGenerator."""
        while True:
            print("\n--- Basic Generator Menu ---")
            print("1. Generate a single image")
            print("2. Generate multiple images")
            print("b. Back to main menu")
            choice = input("👉 Enter your choice: ").strip()

            if choice == '1':
                prompt = input("   Enter prompt (or press Enter for default): ") or None
                self.flux_generator.generate_single_image(prompt=prompt)
            elif choice == '2':
                try:
                    count = int(input("   Enter number of images to generate (e.g., 5): "))
                    prompt = input("   Enter prompt (or press Enter for default): ") or None
                    self.flux_generator.generate_images(count=count, prompt=prompt)
                except ValueError:
                    print("❌ Invalid number.")
            elif choice.lower() == 'b':
                break
            else:
                print("❌ Invalid choice.")

    def _handle_enhanced_generator_menu(self):
        """Handle the menu for the EnhancedFluxGenerator."""
        while True:
            print("\n--- Enhanced Generator Menu ---")
            print(f"(Current Style: {self.enhanced_generator.current_style}, "
                  f"Aspect: {self.enhanced_generator.current_aspect}, "
                  f"Quality: {self.enhanced_generator.current_quality})")
            print("1. Generate a single image with current settings")
            print("2. Generate multiple images with current settings")
            print("3. Change Style")
            print("4. Change Aspect Ratio")
            print("5. Change Quality")
            print("6. List available styles")
            print("b. Back to main menu")
            choice = input("👉 Enter your choice: ").strip()

            if choice == '1':
                self.enhanced_generator.generate_single_image()
            elif choice == '2':
                try:
                    count = int(input("   Enter number of images: "))
                    self.enhanced_generator.generate_images(count=count)
                except ValueError:
                    print("❌ Invalid number.")
            elif choice == '3':
                style = input("   Enter new style: ").strip()
                try:
                    self.enhanced_generator.set_style(style)
                except ValueError as e:
                    print(f"❌ {e}")
            elif choice == '4':
                aspect = input("   Enter new aspect ratio: ").strip()
                try:
                    self.enhanced_generator.set_aspect_ratio(aspect)
                except ValueError as e:
                    print(f"❌ {e}")
            elif choice == '5':
                quality = input("   Enter new quality: ").strip()
                try:
                    self.enhanced_generator.set_quality(quality)
                except ValueError as e:
                    print(f"❌ {e}")
            elif choice == '6':
                styles = self.enhanced_generator.list_available_styles()
                print("   Available Styles:")
                for s in styles:
                    print(f"   - {s['key']}: {s['name']}")
            elif choice.lower() == 'b':
                break
            else:
                print("❌ Invalid choice.")

    def _handle_rotation_generator_menu(self):
        """Handle the menu for the CharacterRotationGenerator."""
        while True:
            print("\n--- Character Rotation Menu ---")
            print("1. Generate a single rotation angle")
            print("2. Generate a 360-degree sequence (8 steps)")
            print("3. List available angles")
            print("b. Back to main menu")
            choice = input("👉 Enter your choice: ").strip()

            if choice == '1':
                angle = input("   Enter angle (e.g., front_left): ").strip()
                try:
                    self.rotation_generator.generate_single_rotation(angle=angle)
                except ValueError as e:
                    print(f"❌ {e}")
            elif choice == '2':
                self.rotation_generator.generate_360_degree_sequence(steps=8)
            elif choice == '3':
                angles = self.rotation_generator.get_rotation_angles()
                print("   Available Angles:")
                for a in angles:
                    print(f"   - {a}")
            elif choice.lower() == 'b':
                break
            else:
                print("❌ Invalid choice.")

    def _handle_adetailer_generator_menu(self):
        """Handle the menu for the AdetailerGenerator."""
        print("\n--- Adetailer (Face Enhancement) Menu ---")
        print("This tool processes existing images to improve face details.")
        input_dir = self.enhanced_generator.output_dir # Common case is processing enhanced images
        print(f"Default input directory is: {input_dir}")
        
        while True:
            print("1. Process all images in the default directory")
            print("2. Process images in a custom directory")
            print("b. Back to main menu")
            choice = input("👉 Enter your choice: ").strip()

            if choice == '1':
                self.adetailer_generator.process_directory_images(input_dir=input_dir)
                print(f"✅ Processing complete. Check the 'data/adetailer_processed' directory.")
            elif choice == '2':
                custom_path = input("   Enter the full path to the directory: ").strip()
                try:
                    path = Path(custom_path)
                    if not path.is_dir():
                        print("❌ Path is not a valid directory.")
                        continue
                    self.adetailer_generator.process_directory_images(input_dir=path)
                    print(f"✅ Processing complete. Check the 'data/adetailer_processed' directory.")
                except Exception as e:
                    print(f"❌ An error occurred: {e}")
            elif choice.lower() == 'b':
                break
            else:
                print("❌ Invalid choice.")

    def _test_connection(self):
        """Test the connection to the API."""
        print("\n🧪 Testing API connection...")
        # Any generator can be used to test the connection
        if self.flux_generator and self.flux_generator.test_connection():
            print("✅ API Connection successful!")
        else:
            print("❌ API Connection failed. Check your API key and network.")


if __name__ == "__main__":
    cli = CLI()
    cli.run() 