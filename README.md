# BMP-II Technical Training Simulator

A Python-based interactive 3D training simulator for the BMP-II Infantry Fighting Vehicle. This application provides virtual reality-style technical training for vehicle maintenance and operation.

## Features

### Training Modules
1. **Engine System** - Diesel engine, cooling system, fuel system
2. **Transmission System** - Gearbox, drive shaft, differential
3. **Turret & Weapons** - Turret rotation, 2A42 autocannon, ammunition feed
4. **Suspension System** - Torsion bars, track assembly, shock absorbers
5. **Electronics & Controls** - Fire control, communication systems
6. **Maintenance Procedures** - Routine maintenance and troubleshooting

### Capabilities
- Interactive 3D component visualization
- Step-by-step training procedures for each component
- Progress tracking and statistics
- Scoring system for completed modules
- Persistent progress saving
- Modern dark-themed UI

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)

## Installation

1. Ensure Python 3 is installed on your system:
```bash
python3 --version
```

2. tkinter should be included with most Python installations. If not installed:

**On Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**On macOS:**
```bash
brew install python-tk
```

**On Windows:**
tkinter is typically included with the Python installer.

## Usage

Run the simulator:
```bash
python3 bmp2_training_simulator.py
```

Or make it executable:
```bash
chmod +x bmp2_training_simulator.py
./bmp2_training_simulator.py
```

## How to Use

1. **Select a Module**: Click "Start" on any training module from the left panel
2. **View Components**: The 3D view shows all components in the selected module
3. **Interactive Training**: Click on any component to view detailed training procedures
4. **Complete Training**: Mark components as completed to track progress
5. **View Statistics**: Check your overall training progress and scores
6. **Reset Progress**: Clear all progress to start fresh

## Data Persistence

Training progress is automatically saved to `training_progress.json` in the same directory as the script. This allows you to continue your training across multiple sessions.

## Project Structure

```
bmp2_training_simulator.py    # Main application (single file)
training_progress.json         # Auto-generated progress file
README.md                      # This file
```

## Technical Details

### Architecture
- **GUI Framework**: tkinter (Python standard library)
- **Data Management**: JSON for persistence
- **Design Pattern**: Object-oriented with dataclasses

### Key Components
- `BMP2Simulator`: Main application class
- `TrainingModule`: Data structure for training modules
- `Component`: Data structure for vehicle components
- Interactive canvas for 3D visualization
- Progress tracking and statistics system

## BMP-II Vehicle Information

The BMP-II (Boyevaya Mashina Pekhoty) is a Soviet/Russian infantry fighting vehicle with the following specifications:

- **Engine**: UTD-20 6-cylinder diesel, 300 HP
- **Armament**: 2A42 30mm autocannon (500 rounds/min)
- **Crew**: 3 (commander, gunner, driver)
- **Passengers**: 7 infantry soldiers
- **Weight**: 14.3 tonnes
- **Top Speed**: 65 km/h (road), 7 km/h (water)

## Educational Use

This simulator is designed for:
- Military technical training
- Vehicle maintenance education
- Virtual reality training environments
- Educational institutions teaching vehicle mechanics
- Self-paced learning for military personnel

## License

This is an educational training tool. Use responsibly for training and educational purposes.

## Support

For issues or questions about using the simulator, please refer to the interactive help within the application or consult the training manual.

## Future Enhancements

Potential additions:
- VR headset support (Oculus/HTC Vive integration)
- Multiplayer training scenarios
- Quiz mode for knowledge testing
- Video tutorials for each component
- Export training reports
- Additional vehicle systems
