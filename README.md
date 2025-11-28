# City Pollution Reduction Planner
## Complete Documentation & User Manual

**Galvin M. Gonzales**
**B-3L**
**CMSC 150 Final Project**  
**Academic Year 2025-2026, 1st Semester**

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Overview](#2-system-overview)
3. [Installation Guide](#3-installation-guide)
4. [User Manual](#4-user-manual)
5. [Technical Documentation](#5-technical-documentation)
6. [Troubleshooting](#6-troubleshooting)
7. [Appendices](#7-appendices)

---

## 1. Introduction

### 1.1 Purpose

The City Pollution Reduction Planner is an optimization tool designed to help the City of Greenvale minimize the cost of implementing pollution reduction projects while meeting mandatory reduction targets for 10 different pollutants.

### 1.2 Problem Statement

Greenvale must reduce its pollution footprint across ten priority pollutants:
- **CO₂** (Carbon Dioxide)
- **NOₓ** (Nitrogen Oxides)
- **SO₂** (Sulfur Dioxide)
- **PM2.5** (Particulate Matter 2.5)
- **CH₄** (Methane)
- **VOC** (Volatile Organic Compounds)
- **CO** (Carbon Monoxide)
- **NH₃** (Ammonia)
- **BC** (Black Carbon)
- **N₂O** (Nitrous Oxide)

### 1.3 Goals

- **Primary**: Minimize total implementation cost
- **Constraint**: Meet or exceed all pollutant reduction targets
- **Limitation**: Each project can be implemented 0-20 units

---

## 2. System Overview

### 2.1 Architecture

The system uses a **client-server architecture**:

```
┌─────────────────┐         HTTP/JSON          ┌─────────────────┐
│   Streamlit     │ ─────────────────────────> │   R Plumber     │
│   Frontend      │                             │   Backend       │
│  (Python)       │ <───────────────────────── │   (Simplex)     │
└─────────────────┘                             └─────────────────┘
```

### 2.2 Components

**Frontend (project_gui.py)**
- Built with Streamlit
- Interactive data table for project selection
- Real-time feasibility checking
- Results visualization

**Backend (plumber_project.R)**
- RESTful API using Plumber
- Simplex method solver
- Dual problem transformation
- Iteration tracking

**Deployment (Dockerfile)**
- Containerized R backend
- Deployed on Render.com
- Accessible at: `https://cmsc150finalproject.onrender.com`

### 2.3 Key Features

Interactive project selection via editable table  
Select All / Reset buttons for quick selection  
Real-time feasibility validation  
Dual problem formulation (following CMSC 150 curriculum)  
Complete iteration history display  
Cost breakdown by project  
Responsive web interface  

---

## 3. Getting Started

### 3.1 System Requirements

**Minimum Requirements:**
- Modern web browser (Chrome, Firefox, Safari, or Edge)
- Internet connection
- No software installation needed!

**Recommended Browsers:**
- Google Chrome (version 90+)
- Mozilla Firefox (version 88+)
- Microsoft Edge (version 90+)
- Safari (version 14+)

### 3.2 Accessing the Application

**🌐 Live Application URL:**
```
https://cmsc150finalproject-h3brbqgtlfdlqxqpbcz7nt.streamlit.app
```

**Quick Access Steps:**

1. **Open your web browser**

2. **Navigate to the URL above**
   - Or click this link: [City Pollution Reduction Planner](https://cmsc150finalproject-h3brbqgtlfdlqxqpbcz7nt.streamlit.app)

3. **Wait for the app to load**
   - First visit may take 10-15 seconds
   - Subsequent visits load faster

4. **Start using immediately** - No installation, no setup, no configuration needed!

### 3.3 Application Architecture

The application is fully cloud-hosted:

```
┌──────────────────────────────────────────────┐
│  Your Browser                                 │
│  (No installation needed)                     │
└────────────────┬─────────────────────────────┘
                 │ HTTPS
                 ▼
┌──────────────────────────────────────────────┐
│  Streamlit Community Cloud                    │
│  Frontend: Python + Streamlit                 │
│  URL: cmsc150finalproject-...streamlit.app   │
└────────────────┬─────────────────────────────┘
                 │ HTTPS/JSON
                 ▼
┌──────────────────────────────────────────────┐
│  Render.com Backend                           │
│  Simplex Solver: R + Plumber                  │
│  URL: cmsc150finalproject.onrender.com       │
└──────────────────────────────────────────────┘
```

**Key Benefits:**
- Zero installation required
- Access from any device
- Automatic updates
- Always available (24/7)
- No local resources used

### 3.4 First-Time Setup (Optional)

**Bookmark the Application:**
1. Visit the URL
2. Press `Ctrl+D` (Windows/Linux) or `Cmd+D` (Mac)
3. Save bookmark for quick access

**Add to Mobile Home Screen:**
1. Visit the URL on mobile browser
2. Tap browser menu (⋮ or ⋯)
3. Select "Add to Home Screen"
4. App appears as icon on your device

---

## 4. User Manual

### 4.1 Selecting Projects

#### Method 1: Manual Selection via Table

The main interface displays an **interactive data table** with all 30 projects:

- **Select Column**: Check/uncheck to include/exclude projects
- **Sortable Columns**: Click column headers to sort by ID, Name, Cost, or pollutant reductions
- **Fixed Height**: Table is scrollable for easy navigation

**Steps:**
1. Browse through the project list
2. Click checkboxes in the "Select" column for projects you want to include
3. Your selections are automatically saved

#### Method 2: Quick Actions

**Select All Button:**
- Click to instantly select all 30 projects
- Useful for finding the global optimal solution

**Reset Button:**
- Click to deselect all projects
- Clears your current selection

### 4.2 Understanding the Data Table

Each row shows:

| Column | Description | Example |
|--------|-------------|---------|
| Select | Checkbox to include project | ☑ |
| ID | Project number (1-30) | 5 |
| Project Name | Full project description | Boiler Retrofit |
| Cost ($) | Cost per unit in dollars | $1,400 |
| CO2...N2O | Pollutant reductions per unit | 20, 0.9, 0.4... |

### 4.3 Running the Optimization

1. **Select your projects** using any method above

2. **Review the summary:**
   - Below the table, you'll see: "X project(s) selected: [IDs]"
   - Or "All 30 projects selected" if you selected all

3. **Click "Calculate Optimal Mix"** button
   - Button is disabled if no projects are selected
   - Solver begins immediately

4. **Wait for results:**
   - A spinner shows "Solving linear program..."
   - Typically takes 2-5 seconds for 30 projects
   - More projects = slightly longer processing time

### 4.4 Understanding the Results

#### Debug Information

First, you'll see validation data: (Initiall used for debugging but it's useful for the user figure out which projects they're over the cap)

```
Problem appears theoretically feasible

Pollutant CO2: Target=1000, Max possible=11844.00
Pollutant NOx: Target=35, Max possible=340.00
...
```

This confirms whether your selected projects **can** meet all targets.

#### Your Input

Shows which projects you selected:
- Lists all selected project names
- Or states "all possible mitigation projects"

#### The Optimized Cost

```
## $238,931.81
The cost of this optimal mitigation project
```

This is the **minimum cost** to meet all pollution targets using your selected projects.

#### Solution Breakdown Table

A detailed table showing exactly how many units of each project to implement:

| Mitigation Project | Number of Project Units | Cost ($) |
|-------------------|------------------------|----------|
| Boiler Retrofit | 20.000000 | $28,000.00 |
| Traffic Signal/Flow Upgrade | 6.993230 | $6,993.23 |
| Low-Emission Stove Program | 20.000000 | $3,600.00 |
| ... | ... | ... |

**Key points:**
- Only shows projects with non-zero allocation
- Units can be fractional (e.g., 6.993)
- Cost = Units × Cost per unit

#### Simplex Tableau Iterations

Expandable sections showing the algorithm's progress:

**Iteration 0 (Initial):** Starting tableau  
**Iteration 1, 2, 3...:** Each pivot operation  
**Final Iteration:** Optimal solution reached

Each iteration shows:
- Pivot Row, Column, and Element
- Complete tableau state
- Useful for understanding the algorithm

### 4.6 Handling Infeasible Cases

If you see:

```
The problem is infeasible.
The selected projects cannot meet all pollution reduction targets.
```

**What this means:**
- Your selected projects cannot meet all pollutant targets
- Even using 20 units of each selected project isn't enough

**Solutions:**
1. Select more projects
2. Click "Select All" to include all options
3. Check which pollutants can't be met in the debug section

### 4.7 Example Walkthrough

**Scenario: Finding the optimal solution with all projects**

1. **Access the app:**
   - Visit: `https://cmsc150finalproject-h3brbqgtlfdlqxqpbcz7nt.streamlit.app`
   - Wait for the page to load (10-15 seconds on first visit)

2. **Select all projects:** 
   - Click the "Select All" button at the top
   - All 30 checkboxes will be marked

3. **Verify selection:** 
   - See "All 30 projects selected" message below the table

4. **Run optimization:** 
   - Click the blue "Calculate Optimal Mix" button
   - Wait for solver (2-5 seconds)

5. **Review results:**
   ```
   The Optimized Cost: $238,931.81
   
   13 projects recommended with specific units:
   - Boiler Retrofit: 20 units ($28,000)
   - Traffic Signal Upgrade: 6.99 units ($6,993)
   - Low-Emission Stove Program: 20 units ($3,600)
   - ... and 10 more projects
   ```

6. **Examine details:** 
   - Scroll down to "Simplex Tableau Iterations"
   - Expand any iteration to see algorithm steps
   - Review final tableau for verification

**Scenario: Custom Selection**

1. **Start fresh:** Click "Reset" to clear all selections

2. **Browse projects:** Scroll through the interactive table

3. **Select specific projects:** 
   - Check boxes for projects you're interested in
   - Example: Select only renewable energy projects (IDs 1-3)

4. **Check feasibility:**
   - Click "Calculate Optimal Mix"
   - If infeasible, you'll see which pollutants can't be met

5. **Add more projects:** Return to table and select additional projects

6. **Re-run:** Click "Calculate Optimal Mix" again

---

## 5. Technical Documentation

### 5.1 Problem Formulation

**Minimization:**

Minimize:
```
Z = Σ(cost_i × x_i)  for i = 1 to 30
```

Subject to:
```
Σ(pollutant_reduction_ij × x_i) ≥ target_j  for all pollutants j
0 ≤ x_i ≤ 20  for all projects i
```

**Converting to Maximization**

The system transforms the minimization problem to its dual based on the Laboratory handout:

Maximize:
```
W = Σ(target_j × y_j) - 20 × Σ(u_i)
```

Subject to:
```
Σ(pollutant_reduction_ij × y_j) - u_i ≤ cost_i  for all projects i
y_j ≥ 0, u_i ≥ 0
```

Where:
- `y_j` = dual variables for pollutant constraints
- `u_i` = dual variables for upper bound constraints

### 5.2 Algorithm: Simplex Method

1. **Dual Transformation:**
   - Converts minimization with ≥ constraints to maximization with ≤ constraints
   - Adds slack variables to convert inequalities to equations

2. **Tableau Construction:**
   ```
   [A^T | -I | I | c]  (constraint rows)
   [-b  | 20 | 0 | 0]  (objective row)
   ```
   Where:
   - `A^T` = transpose of constraint matrix
   - `-I` = negative identity (u variables)
   - `I` = identity (slack variables)
   - `c` = costs vector
   - `-b` = negative targets
   - `20` = upper bound penalty

3. **Simplex Iterations:**
   - Select pivot column (most negative objective coefficient)
   - Select pivot row (minimum ratio test)
   - Perform pivot operation (Gauss-Jordan elimination)
   - Repeat until all objective coefficients ≥ 0

4. **Solution Extraction:**
   - Primal solution = slack variable values in final tableau
   - Optimal cost = Z value from last row, last column

### 5.3 Data Structures

**Pollutant Targets:**
```python
TARGETS = {
    "CO2": 1000, "NOx": 35, "SO2": 25,
    "PM2.5": 20, "CH4": 60, "VOC": 45,
    "CO": 80, "NH3": 12, "BC": 6, "N2O": 10
}
```

**Project Data Structure:**
```python
(id, name, cost, [CO2, NOx, SO2, PM2.5, CH4, VOC, CO, NH3, BC, N2O])
```

**Example:**
```python
(5, "Boiler Retrofit", 1400, [20, 0.9, 0.4, 0.2, 0.1, 0.05, 1.2, 0.02, 0.01, 0.05])
```

### 5.4 API Specification

**Endpoint:** `POST /simplex`

**Request:**
```json
{
  "tableau": [[row1], [row2], ..., [objective_row]],
  "isMax": true
}
```

**Response (Success):**
```json
{
  "finalTableau": {...},
  "finalSolution": {...},
  "Z": 238931.81,
  "iterations": [{...}, {...}, ...],
  "infeasible": false
}
```

**Response (Failure):**
```json
{
  "error": "Linear program is infeasible",
  "infeasible": true
}
```

### 5.5 Session State Management

The app uses Streamlit's session state to persist:

```python
st.session_state.selected_projects  # Set of selected project IDs
st.session_state.project_editor_df  # DataFrame with selections
```

This ensures selections persist across button clicks and reruns.

---

## 6. Troubleshooting

### 6.1 Common Issues

#### Issue: App won't load or shows "Waking up..."

**Symptoms:**
- Page displays "Your app is waking up"
- Loading takes more than 30 seconds
- Blank screen

**Causes:**
1. Streamlit Community Cloud app was sleeping (inactive)
2. Internet connection issues
3. Browser cache problems

**Solutions:**
- **Wait 10-15 seconds** - First load wakes up the app
- **Refresh the page** - Press F5 or reload button
- **Clear browser cache** - Ctrl+Shift+Del, clear cached images
- **Try a different browser** - Test in Chrome, Firefox, or Edge
- **Check internet connection** - Ensure stable connection

#### Issue: "Could not reach R backend"

**Symptoms:**
```
Could not reach R backend. Make sure plumber is running...
```

**Causes:**
1. Render.com backend is sleeping (first request, usually the cpu spins down after awhile of inactivity)
2. Internet connection lost
3. Backend temporarily unavailable

**Solutions:**
- **Wait and retry** - First request wakes backend (10-20 seconds)
- **Click "Calculate" again** - Second attempt usually works
- **Check internet connection** - Ensure stable connection
- **Wait a few minutes** - Backend may be restarting

#### Issue: Page keeps reloading

**Symptoms:**
- Selections disappear
- Page refreshes unexpectedly
- Can't complete actions

**Causes:**
- Browser compatibility issues
- Session timeout
- Network interruption

**Solutions:**
- **Use recommended browser** - Chrome or Firefox preferred
- **Avoid going idle** - Complete tasks within 30 minutes
- **Don't use browser back button** - Stay on the page
- **Check network stability** - Avoid spotty WiFi

#### Issue: "No projects selected"

**Symptoms:**
- "Calculate Optimal Mix" button is disabled
- Warning: "No projects selected..."

**Solutions:**
- Check at least one project in the table
- Or click "Select All" button

#### Issue: "Problem is infeasible"

**Symptoms:**
```
The problem is infeasible.
```

**Causes:**
- Selected projects cannot meet all targets
- Specific pollutants are undersupplied

**Solutions:**
1. Check debug section to see which pollutants can't be met
2. Select more projects that reduce the missing pollutants
3. Try selecting all projects to see the global solution

#### Issue: Slow performance

**Causes:**
- First request to Render.com wakes up sleeping server
- Large number of projects selected
- Network latency

**Solutions:**
- First request may take 10-20 seconds (server wake-up)
- Subsequent requests are fast (2-5 seconds)
- Be patient and wait for the spinner to complete

### 6.2 Error Messages

| Error | Meaning | Action |
|-------|---------|--------|
| "Linear program is unbounded" | Objective can increase infinitely | Check constraint formulation |
| "Linear program is infeasible" | No solution satisfies constraints | Select more projects |
| "Backend error: 400" | Invalid request sent to API | Check project_gui.py code |
| "Backend error: 500" | Server-side error | Check R backend logs |

### 6.3 Data Validation

**The system automatically validates:**

✓ Project IDs are valid (1-30)  
✓ All project data is complete  
✓ Constraints are properly formatted  
✓ Tableau dimensions are correct  

**Manual checks you can do:**

1. Verify selections match your intent
2. Check debug output for feasibility warnings
3. Confirm optimal cost is reasonable ($200k-$300k for all projects)

---

## 7. Appendices

### 7.1 Complete Project List

| ID | Project Name | Cost ($) | Best For |
|----|--------------|----------|----------|
| 1 | Large Solar Park | 4,000 | CO2 reduction |
| 2 | Small Solar Installations | 1,200 | CO2 reduction |
| 3 | Wind Farm | 3,800 | CO2 reduction |
| 4 | Gas-to-renewables conversion | 3,200 | Multi-pollutant |
| 5 | Boiler Retrofit | 1,400 | Multi-pollutant |
| 6 | Catalytic Converters for Buses | 2,600 | NOx, CO |
| 7 | Diesel Bus Replacement | 5,000 | NOx, CO |
| 8 | Traffic Signal/Flow Upgrade | 1,000 | CO2, CO |
| 9 | Low-Emission Stove Program | 180 | PM2.5, BC |
| 10 | Residential Insulation/Efficiency | 900 | CO2 |
| 11 | Industrial Scrubbers | 4,200 | SO2 |
| 12 | Waste Methane Capture System | 3,600 | CH4 |
| 13 | Landfill Gas-to-energy | 3,400 | CH4 |
| 14 | Reforestation (acre-package) | 220 | CO2, CH4 |
| 15 | Urban Tree Canopy Program | 300 | CO2, CH4 |
| 16 | Industrial Energy Efficiency Retrofit | 1,600 | Multi-pollutant |
| 17 | Natural Gas Leak Repair | 1,800 | CH4 |
| 18 | Agricultural Methane Reduction | 2,800 | CH4 |
| 19 | Clean Cookstove & Fuel Switching | 450 | PM2.5, BC |
| 20 | Rail Electrification | 6,000 | CO2, NOx, CO |
| 21 | EV Charging Infrastructure | 2,200 | CO2 |
| 22 | Biochar for soils | 1,400 | CO2, CH4, NH3 |
| 23 | Industrial VOC Reduction | 2,600 | VOC |
| 24 | Heavy-Duty Truck Retrofit | 4,200 | Multi-pollutant |
| 25 | Port/Harbor Electrification | 4,800 | Multi-pollutant |
| 26 | Black Carbon reduction | 600 | BC, PM2.5 |
| 27 | Wetlands restoration | 1,800 | CH4, NH3 |
| 28 | Household LPG conversion program | 700 | PM2.5, BC |
| 29 | Industrial process change | 5,000 | N2O |
| 30 | Behavioral demand-reduction program | 400 | Multi-pollutant |

### 7.2 Pollutant Targets

| Pollutant | Target (tons) | Main Sources |
|-----------|---------------|--------------|
| CO2 | 1,000 | Energy, transport |
| NOx | 35 | Vehicles, industry |
| SO2 | 25 | Industry, energy |
| PM2.5 | 20 | Combustion, dust |
| CH4 | 60 | Waste, agriculture |
| VOC | 45 | Industry, solvents |
| CO | 80 | Vehicles, stoves |
| NH3 | 12 | Agriculture |
| BC | 6 | Incomplete combustion |
| N2O | 10 | Industry, agriculture |

### 7.3 Expected Results

**With all 30 projects selected:**
- **Optimal Cost**: ~$238,931.81
- **Projects Used**: 13 out of 30
- **Solution Type**: Fractional units for most projects
- **Computation Time**: 2-5 seconds

**Sample optimal allocation:**
- Boiler Retrofit: 20 units (maxed out)
- Traffic Signal Upgrade: ~7 units
- Low-Emission Stove: 20 units (maxed out)
- Industrial Scrubbers: ~2.25 units
- Plus 9 more projects

### 7.4 Deployment Information

**Frontend Hosting:**
- **Platform**: Streamlit Community Cloud
- **URL**: https://cmsc150finalproject-h3brbqgtlfdlqxqpbcz7nt.streamlit.app
- **Status**: Always available (auto-wakes from sleep)
- **Technology**: Python 3.x with Streamlit

**Backend Hosting:**
- **Platform**: Render.com (Free Tier)
- **URL**: https://cmsc150finalproject.onrender.com
- **API Endpoint**: POST /simplex
- **Technology**: R 4.x with Plumber
- **Note**: May sleep after 15 minutes of inactivity (wakes on first request)

**System Behavior:**
- **First visit**: 10-20 seconds (both frontend and backend wake up)
- **Subsequent visits**: 2-5 seconds (already awake)
- **Inactivity**: Apps sleep after 15-30 minutes
- **Wake time**: 10-15 seconds on next use

### 7.5 Source Code

The complete source code for this project is available and includes:

```
project/
├── project_gui.py              # Streamlit frontend
├── plumber_project.R           # R Simplex solver
├── run_plumber.R               # R backend launcher
├── Dockerfile                  # Docker configuration
└── README.md                   # Documentation
```

**Key Features in Code:**
- Interactive data editor with session state
- Dual problem transformation
- Real-time feasibility checking
- Complete iteration tracking
- Responsive error handling

**For Developers:**
If you want to modify or run locally:
1. Clone/download the source files
2. Install dependencies: `pip install streamlit pandas numpy requests`
3. Run locally: `streamlit run project_gui.py`
4. Modify `project_gui.py` to point to your own backend if needed

### 7.5 References

**Course Materials:**
- CMSC 150 Laboratory Topic 5: Simplex Method
- CMSC 150 Final Project Specifications S1AY25-26

**External Resources:**
- Streamlit Documentation: https://docs.streamlit.io
- Plumber Documentation: https://www.rplumber.io
- Linear Programming Theory: Chapra & Canale, Numerical Methods for Engineers

---

## Support

**For Technical Issues:**

1. **Check this documentation** - Review the Troubleshooting section (Section 6)
2. **Verify internet connection** - Ensure stable connectivity
3. **Try a different browser** - Test in Chrome, Firefox, or Edge
4. **Wait and retry** - First-time loads may take 10-20 seconds
5. **Contact Me** - either here in Github SenjoNanaya or write an email to gmgonzales6@up.edu.ph
   
**Application Access:**

**Live URL**: https://cmsc150finalproject-h3brbqgtlfdlqxqpbcz7nt.streamlit.app

**Feedback**: Use the feedback widget in the app (☰ menu → Report a bug)

---

## Credits

**Developed for:** CMSC 150 - Numerical and Symbolic Computation  
**Institution:** University of the Philippines Los Baños  
**Academic Year:** 2025-2026, 1st Semester  
**Special thanks to Claude for helping in writing and creating the diagrams + formulas + tables for this documentation**

**Technologies Used:**
- Python 3.x with Streamlit
- R 4.x with Plumber
- Docker for deployment
- Render.com for hosting

---

*End of Documentation*

**Version History:**
- v1.0 (December 2025) - Initial release
