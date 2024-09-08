import keyboard
from PIL import Image, ImageChops, ImageDraw, ImageGrab
import os

def take_screenshot():
    screenshot = ImageGrab.grab()
    return screenshot

def save_screenshot(image, filename):
    image.save(filename)

def highlight_differences(original_image, new_image, output_path):
    # Resize images to match dimensions if necessary
    if original_image.size != new_image.size:
        original_image = original_image.resize(new_image.size)
    
    # Ensure both images have the same mode
    if original_image.mode != new_image.mode:
        original_image = original_image.convert(new_image.mode)

    # Perform difference operation
    diff = ImageChops.difference(original_image, new_image)
    diff = diff.convert('RGB')
    
    # Highlight differences
    draw = ImageDraw.Draw(diff)
    draw.rectangle((0, 0, diff.size[0], diff.size[1]), outline="red")
    
    # Save output image
    output_path = os.path.join(output_path, 'diff.png')
    diff.save(output_path)
    
    return output_path

def select_base_image(directory):
    print("Press 0-9 to select which BaseImage to use (0 for BaseImage.png, 1 for BaseImage1.png, ..., 9 for BaseImage9.png)")
    while True:
        key = keyboard.read_event(suppress=True).name.lower()
        base_image_filename = f"BaseImage{key}.png"
        base_image_path = os.path.join(directory, base_image_filename)
        print(f"Selected base image: {base_image_path}")

        if os.path.exists(base_image_path):
            return base_image_path
        else:
            print(f"Error: {base_image_filename} not found. Please try again.")

def main():
    directory = os.path.join(os.getcwd(), "ImageChecker")
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

    while True:
        print("Press 1 for screenshot mode, 2 for existing image comparison mode, or C to compare screenshot to BaseImage")
        mode = keyboard.read_event(suppress=True).name.lower()

        if mode == "1":
            # Screenshot mode
            print("Screenshot mode activated.")
            print("Press T to take a screenshot")
            keyboard.wait("t")
            original_screenshot = take_screenshot()
            original_screenshot_path = os.path.join(directory, "original_screenshot.png")
            save_screenshot(original_screenshot, original_screenshot_path)
            print(f"Screenshot saved: {original_screenshot_path}")

            print("Press Y to take another screenshot for comparison")
            keyboard.wait("y")
            new_screenshot = take_screenshot()
            new_screenshot_path = os.path.join(directory, "new_screenshot.png")
            save_screenshot(new_screenshot, new_screenshot_path)
            print(f"Screenshot saved: {new_screenshot_path}")

            diff_output_path = directory
            diff_output_path = highlight_differences(original_screenshot, new_screenshot, diff_output_path)
            print(f"Differences highlighted and saved: {diff_output_path}")

        elif mode == "2":
            # Existing image comparison mode
            print("Existing image comparison mode activated.")
            image1_path = os.path.join(directory, "image1.png")
            image2_path = os.path.join(directory, "image2.png")

            if not (os.path.exists(image1_path) and os.path.exists(image2_path)):
                print("Error: Image files not found.")
                return

            original_image = Image.open(image1_path)
            new_image = Image.open(image2_path)

            diff_output_path = directory
            diff_output_path = highlight_differences(original_image, new_image, diff_output_path)
            print(f"Differences highlighted and saved: {diff_output_path}")

        elif mode == "c":
            # Compare screenshot to BaseImage
            print("Comparing screenshot to BaseImage.")
            base_image_path = select_base_image(directory)
            print("Press J to take a screenshot to compare to BaseImage")
            keyboard.wait("j")
            new_screenshot = take_screenshot()
            new_screenshot_path = os.path.join(directory, "new_screenshot.png")
            save_screenshot(new_screenshot, new_screenshot_path)
            print(f"Screenshot saved: {new_screenshot_path}")

            base_image = Image.open(base_image_path)
            diff_output_path = directory
            diff_output_path = highlight_differences(base_image, new_screenshot, diff_output_path)
            print(f"Differences highlighted and saved: {diff_output_path}")

        else:
            print("Invalid mode selection. Please press either 1, 2, or C.")

if __name__ == "__main__":
    main()
