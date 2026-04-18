# Biology Slideshow Project

This project creates a PowerPoint slideshow on the interaction between the immune and integumentary systems in fighting germs and pathogens, using Python.

## Files
- `create_slideshow.py`: Python script that generates the slideshow using python-pptx and matplotlib.
- `biology_slideshow.pptx`: The generated PowerPoint presentation.
- `model_diagram.png`: Diagram image used in the slideshow.

## How to Run
1. Ensure Python is installed.
2. Configure virtual environment: The script uses a virtual environment at `.venv`.
3. Install dependencies: `python-pptx`, `matplotlib`, `pillow`.
4. Run the script: `python create_slideshow.py`

## Troubleshooting

### Issue 1: Configuring Python Environment
- **Problem**: Needed to set up a virtual environment for dependency management.
- **Solution**: Used the `configure_python_environment` tool to create a virtual environment in the workspace. This ensures isolated package installation and avoids conflicts with system Python.

### Issue 2: Installing Packages
- **Problem**: Required packages (python-pptx for PowerPoint creation, matplotlib for diagrams, pillow for image handling) were not installed.
- **Solution**: Used `install_python_packages` to install them in the virtual environment. Verified installation by checking the output.

### Issue 3: Running the Script in Terminal
- **Problem**: Initial attempt to run the script failed with "Unexpected token" error due to spaces in the path and improper quoting in PowerShell.
- **Command tried**: `"c:/Users/Hari/Desktop/Personal projects/Biology slides/.venv/Scripts/python.exe" create_slideshow.py`
- **Error**: ParserError because PowerShell didn't recognize the unquoted script name.
- **Solution**: Used PowerShell call operator `&` and quoted both the executable path and the script file: `& "c:/Users/Hari/Desktop/Personal projects/Biology slides/.venv/Scripts/python.exe" "create_slideshow.py"`. This properly handles paths with spaces.

### Issue 4: Generating the Diagram
- **Problem**: Needed to create a visual model of how the systems fight pathogens.
- **Solution**: Used matplotlib to draw a simple flowchart with boxes and arrows, saved as PNG, and embedded in the PowerPoint slide.

### Issue 5: Content Accuracy
- **Problem**: Ensured biological content is correct.
- **Solution**: Based on standard biology knowledge: integumentary system as barrier, immune system as response. Included key points on interaction and defense mechanisms.

The project was completed successfully after resolving the terminal execution issue.