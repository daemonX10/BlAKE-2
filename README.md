

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd ultimate-cipher
```

2. Create a virtual environment:

For Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# If you encounter execution policy error, run PowerShell as Administrator and execute:
Set-ExecutionPolicy RemoteSigned
```

For macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Terminal Interface

1. Activate the virtual environment (if not already activated):
   - Windows: `.\venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

2. Run the terminal interface:
```bash
python menu_cli.py
```

3. Follow the interactive menu:
   - Choose operation (Encrypt/Decrypt)
   - Enter text to process
   - Provide encryption/decryption keys:
     - Affine key 'a' (must be coprime with 26)
     - Affine key 'b' (0-25)
     - Vigenere key (alphabetic characters only)
     - XOR key (any text)

### Web Interface

1. Activate the virtual environment (if not already activated)

2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

4. Use the web form to:
   - Enter text to process
   - Select operation (Encrypt/Decrypt)
   - Provide required keys
   - View results with original and processed text


### Web Interface Example:
1. Start the web server:
```bash
python app.py
```
2. Fill in the web form with the same example values as above
3. Click "Process" to see the results

## Security Considerations

- This is a demonstration tool and should not be used for sensitive data
- The web interface uses a default secret key - change it in production
- Keys should be kept secure and not shared
- Longer keys generally provide better security

## Troubleshooting

1. If you see "Permission denied" when activating venv:
   - Run PowerShell as Administrator
   - Execute: `Set-ExecutionPolicy RemoteSigned`

2. If Flask shows "No module named 'flask'":
   - Ensure virtual environment is activated
   - Run: `pip install -r requirements.txt`

3. If web interface shows CSRF error:
   - Clear browser cache
   - Restart Flask application

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 