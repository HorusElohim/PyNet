from setuptools import setup

if __name__ == "__main__":
    try:
        setup()
    except Exception as e:
        print(
            f"Exception occurred:  {e}"
            "please ensure you have the most updated version of setuptools, "
            "wheel with:\n"
            "   pip install -U setuptools wheel\n\n"
        )
        raise
