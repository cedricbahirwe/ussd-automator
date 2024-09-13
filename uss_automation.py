import subprocess
import uiautomator2 as u2

# Connect to the device
# Use the device's IP or leave blank for USB
d = u2.connect("192.168.1.66")

# Check if the device is connected
print(f"Device Info {d.info}")


def print_text():
    for element in d.xpath("//*").all():
        text = element.text
        if text:
            print(text)


def perform_ussd(ussd_code: str):
    # Press home
    d.press("home")

    # Launch an app by its package name (for example, launching the Settings app)
    d.app_start("com.automate.myapp")

    # Take a screenshot
    d.screenshot("home_screen.png")

    # Locate the ussd input field by resourceId, className, or any other property
    ussd_input_field = d(className="android.widget.EditText")

    ussd_input_field.set_text(ussd_code)

    # Click an object by its text
    d(text="Dial").click()

    targetText = "fee of"

    # Wait for the USSD response
    if d(textContains=targetText).wait(timeout=5):
        # If the element appears, fetch the element and print its text
        ussd_response = d(textContains=targetText)
        print("USSD response received:", ussd_response.get_text())
        print_text()

        # Locate the USSD Dialog Field
        input_field = d(className="android.widget.EditText")

        # Check if the input field exists
        if input_field.exists:
            # Input the digits (e.g., "1234") into the field
            input_field.set_text("22001")

            # Find and click the "Send" or "OK" button
            # You might need to adjust this if it's "OK" or a different text
            send_button = d(text="SEND")
            if send_button.exists:
                send_button.click()
                print_text()
            else:
                print("Send button not found")
        else:
            print("Input field not found")
    else:
        print("USSD response not detected.")
        print_text()


def print_package_for(version_name: str):
    # Get the list of all packages
    packages_output = subprocess.check_output(
        ["adb", "shell", "pm", "list", "packages"], encoding='utf-8')
    packages = [line.split(":")[1].strip()
                for line in packages_output.splitlines()]

    # Check each package for the versionName
    print(f"Getting here {len(packages)}")
    for package in packages:
        try:
            version_info = subprocess.check_output(
                ["adb", "shell", "dumpsys", "package", package], encoding='utf-8')
            if f"versionName={version_name}" in version_info:
                print(f"Package: {package}, VersionName: {
                      version_name}")
        except subprocess.CalledProcessError:
            print("Passing here")
            pass
