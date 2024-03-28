def guess_os(ip_address):
    try:
        # Run p0f and capture its output
        result = subprocess.run(['p0f', '-r', '-', '-s', '-f', '/path/to/p0f.fp', ip_address], capture_output=True, text=True)

        # Check if p0f command succeeded
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Failed to guess OS. Error: {result.stderr.strip()}"

    except Exception as e:
        return f"An error occurred: {e}"
