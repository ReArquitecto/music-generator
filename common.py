from datetime import datetime

def get_filename(ext='xml', user_input=False, prefix=None):
    """
    Generate a filename with an optional user-defined name or a date-based name.

    Args:
        ext (str): File extension (default is 'xml').
        user_input (bool): Whether to allow user input for the file name (default is False).
        prefix (str): Optional prefix to add to the file name (default is None).

    Returns:
        str: Generated file name.
    """
    if user_input:
        name = input("Enter the file name (without extension): ").strip()
    else:
        now = datetime.now()
        name = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    if prefix:
        name = f"{prefix}_{name}"
    
    return f"{name}.{ext}"
