# 🚀 VS CODE SETUP - QUICK START GUIDE

## 📥 STEP 1: GET THE PROJECT

### From Replit (Current Location):

1. Click the **3 dots menu** (⋮) in Replit
2. Select **"Export as ZIP"** or **"Download as ZIP"**
3. Extract the ZIP file to your desired location on your computer

Example location:
```
Windows: C:\Users\YourName\Documents\smart-resume-analyzer
Mac/Linux: ~/Documents/smart-resume-analyzer
```

---

## 💻 STEP 2: INSTALL PYTHON

### Check if Python is installed:
```bash
python --version
```

### If not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Mac**: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

**Required Version**: Python 3.10 or 3.11

---

## 📂 STEP 3: OPEN IN VS CODE

```bash
# Navigate to project folder
cd path/to/smart-resume-analyzer

# Open in VS Code
code .
```

---

## 🔧 STEP 4: SETUP VIRTUAL ENVIRONMENT

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal now.

---

## 📦 STEP 5: INSTALL DEPENDENCIES

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- scikit-learn (machine learning)
- PyPDF2 & pdfminer.six (PDF processing)
- python-docx (DOCX processing)
- SQLAlchemy (database)
- And 10+ other packages

**Wait 2-3 minutes** for installation to complete.

---

## 📚 STEP 6: DOWNLOAD NLTK DATA

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

## 📁 STEP 7: CREATE REQUIRED FOLDERS

```bash
# Windows
mkdir uploads
mkdir data\trained_models

# Mac/Linux
mkdir -p uploads
mkdir -p data/trained_models
```

---

## ▶️ STEP 8: RUN THE APPLICATION

### Option A: Development Mode (with debug)
```bash
python app.py
```

### Option B: Production Mode (faster)
```bash
python run.py
```

You should see:
```
🚀 Starting Smart Resume Analyzer...
📊 Dashboard: http://localhost:5000
 * Running on http://127.0.0.1:5000
```

---

## 🌐 STEP 9: OPEN IN BROWSER

Open your browser and go to:
```
http://localhost:5000
```

You should see the **Smart Resume Analyzer** homepage!

---

## ✅ STEP 10: TEST IT

1. **Click** "Choose File & Analyze"
2. **Select** a resume PDF or DOCX file
3. **Wait** 2-5 seconds
4. **View** the analysis results!

---

## 🛠️ VS CODE EXTENSIONS (RECOMMENDED)

Install these extensions for better development:

1. **Python** (by Microsoft) - Essential
2. **Pylance** (by Microsoft) - Better IntelliSense
3. **SQLite Viewer** (by qwtel) - View database
4. **Flask Snippets** - Flask helpers
5. **Prettier** - Code formatting

To install:
- Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac)
- Search for extension name
- Click "Install"

---

## 🐛 DEBUGGING IN VS CODE

### Create `.vscode/launch.json`:

1. Click **Run and Debug** icon (left sidebar)
2. Click **"create a launch.json file"**
3. Select **Python** → **Flask**
4. Paste this configuration:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask: Run",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--host=0.0.0.0",
                "--port=5000"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

Now you can:
- Press **F5** to start debugging
- Set breakpoints by clicking left of line numbers
- Inspect variables while code runs

---

## 🧪 TESTING

### Run the test suite:
```bash
python test_app.py
```

Expected output:
```
✅ PASS - Module Imports
✅ PASS - Custom Modules
✅ PASS - Database
✅ PASS - Resume Parser
✅ PASS - ML Classifier
✅ PASS - File Operations
Overall: 6/6 tests passed
```

### Test individual components:
```bash
python models/classifier.py
python utils/parser.py
python models/ranker.py
```

---

## 🔥 COMMON ERRORS & FIXES

### ❌ Error: "No module named 'flask'"
**Fix**:
```bash
# Make sure venv is activated
pip install -r requirements.txt
```

### ❌ Error: "Port 5000 is already in use"
**Fix**: Edit `run.py` line 15:
```python
port = int(os.environ.get('PORT', 5001))  # Change to 5001
```

### ❌ Error: "NLTK data not found"
**Fix**:
```bash
python -c "import nltk; nltk.download('all')"
```

### ❌ Error: "Permission denied" on uploads folder
**Fix**:
```bash
# Windows
icacls uploads /grant Everyone:(OI)(CI)F

# Mac/Linux
chmod 777 uploads
```

### ❌ Error: Import warnings in VS Code (red squiggles)
**Fix**: These are false positives. The code works fine!

Create `pyrightconfig.json`:
```json
{
  "reportMissingImports": false,
  "reportMissingModuleSource": false
}
```

---

## 📝 EDITING THE CODE

### Where to make changes:

#### Change acceptance logic:
- File: `models/classifier.py`
- Function: `determine_acceptance_status()` (line 121)

#### Change fraud detection:
- File: `models/classifier.py`
- Function: `detect_fraud()` (line 182)

#### Change skills database:
- File: `utils/parser.py`
- Variable: `skills_db` (line 118)

#### Change UI:
- File: `templates/index.html`
- File: `static/css/style.css`

#### Change departments:
- File: `models/classifier.py`
- Variable: `self.departments` (line 11)

---

## 🎨 CUSTOMIZING

### Add new skill category:
1. Open `utils/parser.py`
2. Find `skills_db` dictionary (line 118)
3. Add new category:
```python
'Your Category': [
    'skill1', 'skill2', 'skill3'
]
```

### Change department names:
1. Open `models/classifier.py`
2. Find `self.departments` (line 11)
3. Modify list:
```python
self.departments = ['Tech', 'People', 'Money', 'Marketing', 'Engineering', 'Ops', 'Sales']
```

### Adjust acceptance threshold:
1. Open `models/classifier.py`
2. Find `determine_acceptance_status()` (line 121)
3. Change numbers:
```python
if total_skills >= 5:  # Was 4, now 5 (stricter)
    return "Accepted"
```

---

## 📊 PROJECT STRUCTURE EXPLAINED

```
smart-resume-analyzer/
│
├── 📄 app.py                    ← Main application (start here)
├── 📄 run.py                    ← Production runner
├── 📄 test_app.py               ← Test suite
├── 📄 requirements.txt          ← Dependencies list
│
├── 📁 models/
│   ├── classifier.py            ← ML classification + fraud detection
│   └── ranker.py                ← Candidate ranking logic
│
├── 📁 utils/
│   ├── parser.py                ← Resume parsing (PDF/DOCX)
│   ├── preprocessor.py          ← Text cleaning
│   └── feature_extractor.py     ← Feature engineering
│
├── 📁 templates/
│   ├── index.html               ← Home page (upload)
│   ├── history.html             ← Analysis history page
│   └── dashboard.html           ← Analytics dashboard
│
├── 📁 static/
│   ├── css/style.css            ← Custom styles
│   └── favicon.svg              ← Website icon
│
├── 📁 data/
│   └── trained_models/
│       ├── classifier.pkl       ← ML model (auto-generated)
│       └── vectorizer.pkl       ← TF-IDF vectorizer (auto-generated)
│
├── 📁 uploads/                  ← Temporary resume storage
└── 📄 app.db                    ← SQLite database (auto-generated)
```

---

## 🚦 WHAT HAPPENS WHEN YOU RUN

```
1. Flask starts web server on port 5000
2. Database (SQLite) initializes
3. ML models load (or train if first time)
4. NLTK data loads
5. Web interface becomes available
6. Ready to accept resume uploads!
```

---

## 🎓 LEARNING THE CODE

### Beginner Path:
1. Read `app.py` - understand Flask routes
2. Read `utils/parser.py` - see how resumes are parsed
3. Play with `templates/index.html` - modify the UI
4. Run `test_app.py` - understand testing

### Intermediate Path:
5. Study `models/classifier.py` - learn ML classification
6. Study `models/ranker.py` - understand ranking logic
7. Modify acceptance criteria and test
8. Add new features (e.g., export to Excel)

### Advanced Path:
9. Improve ML model accuracy
10. Add new fraud detection methods
11. Implement user authentication
12. Deploy to cloud (Heroku, AWS, Azure)

---

## 📖 ADDITIONAL RESOURCES

### Documentation Files:
- `PROJECT_DOCUMENTATION.md` - Complete technical guide
- `replit.md` - Project overview
- This file - VS Code setup

### Code Comments:
Every function has docstrings explaining what it does!

### Online Resources:
- Flask: https://flask.palletsprojects.com/
- scikit-learn: https://scikit-learn.org/
- SQLAlchemy: https://www.sqlalchemy.org/

---

## 💡 TIPS FOR VS CODE

1. **Use Split Editor**
   - `Ctrl+\` to split editor
   - View code and documentation side-by-side

2. **Terminal Shortcuts**
   - `Ctrl+` \` to toggle terminal
   - Multiple terminals: Click "+" in terminal panel

3. **Search Across Files**
   - `Ctrl+Shift+F` to search entire project
   - Useful for finding where a function is used

4. **Go to Definition**
   - `Ctrl+Click` on function name
   - Jumps to where it's defined

5. **Format Code**
   - `Shift+Alt+F` to auto-format
   - Install "Black" formatter for Python

---

## 🎉 YOU'RE READY!

Now you can:
✅ Run the application in VS Code
✅ Debug with breakpoints
✅ Modify the code
✅ Test your changes
✅ Understand the entire codebase

**Happy coding!** 🚀

For detailed explanations, check `PROJECT_DOCUMENTATION.md`
