import os
import sys

from tech_stack_app_init import manageApp

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common")
)
app = manageApp()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
