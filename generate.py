import os
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import pandas as pd

class CertificateGenerator:
    def __init__(self, template_path, font_path, font_size= 180, font_color="#86529f", output_dir="certificates"):
        # Initialize the certificate generator with configuration
        self.template_path = Path(template_path)
        self.font_path = Path(font_path)
        self.font_size = font_size
        self.font_color = font_color
        self.output_dir = Path(output_dir)
        
        # Validate and load resources
        self._validate_paths()
        self.font = ImageFont.truetype(str(self.font_path), self.font_size)
        self.template = Image.open(self.template_path)
        self.width, self.height = self.template.size
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _validate_paths(self):
        """Validate that all required files exist"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
        if not self.font_path.exists():
            raise FileNotFoundError(f"Font file not found: {self.font_path}")

    def _calculate_text_position(self, draw, text):
        """Calculate the position to center the text"""
        # Get the bounding box of the text
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate center position
        x = (self.width - text_width) / 2
        y = (self.height - text_height) / 2 - 30  # Slight upward adjustment
        
        return x, y

    def generate_certificate(self, name):
        """Generate a single certificate for the given name"""
        try:
            # Create a fresh copy of the template
            image = self.template.copy()
            draw = ImageDraw.Draw(image)
            
            # Calculate text position
            x, y = self._calculate_text_position(draw, name)
            
            # Draw the name on the certificate
            draw.text((x, y), name, fill=self.font_color, font=self.font)
            
            # Save the certificate
            safe_filename = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            output_path = self.output_dir / f"{safe_filename}.png"
            image.save(output_path)
            print(f"✓ Certificate generated for: {name}")
            return output_path
            
        except Exception as e:
            print(f"✗ Error generating certificate for {name}: {str(e)}")
            return None

    def generate_batch(self, names):
        """Generate certificates for a list of names"""
        successful = 0
        failed = 0
        
        print(f"\nGenerating {len(names)} certificates...")
        print("-" * 40)
        
        for name in names:
            if self.generate_certificate(name):
                successful += 1
            else:
                failed += 1
        
        print("-" * 40)
        print(f"Generation complete!")
        print(f"✓ Successful: {successful}")
        print(f"✗ Failed: {failed}")
        print(f"📁 Output directory: {self.output_dir.absolute()}")

def read_names_from_csv(csv_path, name_column='name'):
    """Read names from a CSV file"""
    try:
        df = pd.read_csv(csv_path)
        if name_column not in df.columns:
            raise ValueError(f"Column '{name_column}' not found in CSV file. Available columns: {', '.join(df.columns)}")
        return df[name_column].tolist()
    except Exception as e:
        raise Exception(f"Error reading CSV file: {str(e)}")

def main():
    try:
        # Print current working directory
        print(f"Current directory: {Path.cwd()}")
        
        # Configuration with absolute paths
        config = {
            "template_path": "C:/Users/Admin/Desktop/certificates/template.png",
            "font_path": "C:/Users/Admin/Desktop/certificates/GreatVibes-Regular.ttf",
            "font_size": 180,
            "font_color": "#86529f",
            "output_dir": "C:/Users/Admin/Desktop/certificates/certi"
        }
        
        # CSV file path
        csv_path = "C:/Users/Admin/Desktop/certificates/Book1.csv"
        
        # Check if files exist
        print(f"\nChecking files:")
        print(f"Template exists: {Path(config['template_path']).exists()}")
        print(f"Font exists: {Path(config['font_path']).exists()}")
        print(f"CSV exists: {Path(csv_path).exists()}")
        
        # Try to read CSV file
        print(f"\nReading names from {csv_path}...")
        df = pd.read_csv(csv_path)
        print(f"CSV columns: {df.columns.tolist()}")
        names = read_names_from_csv(csv_path)
        
        if not names:
            print("No names found in the CSV file.")
            return
            
        print(f"Found {len(names)} names: {names[:5]}...")  # Print first 5 names
        
        # Create certificate generator
        print("\nCreating certificate generator...")
        generator = CertificateGenerator(**config)
        
        # Generate certificates
        generator.generate_batch(names)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()