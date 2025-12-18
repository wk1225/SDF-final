# 🏋️ Anytime Fitness Mobile App

## 1. Introduction
The **Anytime Fitness Mobile App** is a Python-based management system designed to help users architect workout plans, log real-time exercise performance, and track progress via caloric burn analysis. Built with a modern light-themed GUI, it simplifies the transition from paper-based logging to a digital fitness dashboard.

---

## 2. Objectives
The objectives of this project are:
- To implement scientifically grounded progress tracking using **MET (Metabolic Equivalent of Task)** values.
- To practice modular programming by separating page logic into specialized Python files.
- To handle local data persistence using Tab-Separated Values (TSV) in `.txt` files.
- To enhance User Experience (UX) through interactive sound feedback using `pygame`.

---

## 3. Technologies Used
- **Python 3.13+**
- **CustomTkinter** – Modernized Graphical User Interface (GUI).
- **pygame (mixer)** – Specialized audio engine for feedback and "Easter Eggs."
- **Pillow (PIL)** – Image processing for application icons and assets.
- **TSV (Flat-File Storage)** – Lightweight local data management.

---

## 4. System Features
- **User Authentication**: Secure Sign-up/Login with user-specific session data.
- **Workout Planning**: Schedule specific body-part exercises for any date.
- **Dynamic Logging**: Record duration and intensity for various activities.
- **Intelligent Reporting**: 
    - Automatic calorie calculation based on intensity multipliers.
    - Comparison popups to visualize progress trends.
- **Profile Customization**: Manage personal descriptions and user metadata.

---

## 5. Use of pygame
The `pygame` library is used exclusively for the **Audio Feedback System**, including:
- **Navigation Sounds**: Feedback when switching between Plan, Log, and Report tabs.
- **Success Cues**: `miaumiau.MP3` or `gayyyy.MP3` for successful entries.
- **Warning/Error Cues**: `omg.MP3` or `bruh.MP3` for invalid inputs.
- **Easter Eggs**: `rickroll.MP3` integrated into specific logging interactions.

---

## 6. Project Structure
```text
AnytimeFitness/
│
├─ image/               # PNG icons and Splash screens
├─ audio/               # Sound effects (.MP3)
│
├─ Main.py              # Application entry, Auth, and Navigation
├─ PlanPage.py          # Workout scheduling logic
├─ LogPage.py           # Exercise logging and audio triggers
├─ ReportPage.py        # Calorie calculations and data analysis
├─ ProfilePage.py       # User settings and system restart
│
├─ user_info.txt        # Local database for account credentials
├─ workout_records.txt  # Local database for fitness history
│
└─ README.md
```

---

## 7. How to Run the Application

### Step 1: Install Required Libraries

```bash
pip install customtkinter Pillow tkcalendar pygame
```

### Step 2: Run the Application

```bash
python Main.py
```

---

## 8. Data Storage

The app uses a TSV (Tab-Separated Values) format for high portability.
---

## 9. Learning Outcomes

- Advanced GUI state management with CustomTkinter.
- Data parsing and math-based reporting logic.
- File I/O operations for real-time data persistence.
- Integrating multimedia (Audio/Images) into functional software.
- Project modularity and file-linking (cross-module communication).
---

## 10. Conclusion

This project demonstrates a fully functional, multi-page fitness ecosystem. It successfully integrates specialized Python libraries to solve the real-world problem of digital fitness tracking while maintaining a small, portable storage footprint.
---

## 11. Future Improvements

- Cloud Integration: Syncing user_info.txt to an online database (Firebase/SQL).
- Visualization: Adding Matplotlib charts to the Report page for visual progress.
- Social Features: Ability to share workout plans with other local users.




