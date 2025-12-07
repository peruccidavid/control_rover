# Control Rover Project

## Overview
The Control Rover project is designed to control a rover using motor drivers and keyboard inputs. The project allows the rover to move forward, reverse, and turn based on keyboard commands.

## Project Structure
```
control_rover
├── src
│   ├── control_motores.py      # Main logic for controlling the motors
│   ├── keyboard_control.py      # Keyboard control commands for the rover
│   ├── __init__.py              # Package initialization
│   └── utils
│       └── __init__.py          # Utility functions
├── tests
│   └── test_keyboard_control.py  # Unit tests for keyboard control
├── requirements.txt              # Project dependencies
├── pyproject.toml                # Project configuration
├── .gitignore                    # Files to ignore in version control
└── README.md                     # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd control_rover
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the motor control script:
   ```
   python src/control_motores.py
   ```

2. Use the keyboard control script to move the rover:
   - **Up Arrow**: Move forward at full speed
   - **Down Arrow**: Reverse
   - **Left Arrow**: Turn 45 degrees to the left
   - **Right Arrow**: Turn 45 degrees to the right
   - **Space**: Stop

## Testing
To run the unit tests for keyboard control, execute:
```
python -m unittest discover -s tests
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.