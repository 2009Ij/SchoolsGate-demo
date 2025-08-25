import qrcode
from PIL import Image
import io

def test_qr_generation():
    """Test the QR code generation functionality"""
    print("Testing QR code generation...")
    
    # Test data
    test_data = {"student_id": 123}
    
    # Generate QR code
    qr_data = f"student:{test_data.get('student_id', 'unknown')}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    print(f"QR code generated successfully!")
    print(f"QR data: {qr_data}")
    print(f"Image size: {img.size}")
    print(f"Buffer size: {len(img_buffer.getvalue())} bytes")
    
    # Test if it can be read back
    try:
        test_img = Image.open(img_buffer)
        print(f"Image can be opened successfully: {test_img.format}, {test_img.size}")
        return True
    except Exception as e:
        print(f"Error opening image: {e}")
        return False

if __name__ == "__main__":
    success = test_qr_generation()
    if success:
        print("✅ QR code test passed!")
    else:
        print("❌ QR code test failed!")
