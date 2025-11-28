import streamlit as st
import pandas as pd
import requests
import json
import numpy as np

st.set_page_config(page_title="Greenvale Pollution Planner", layout="wide")

st.title("City Pollution Reduction Planner")
st.markdown("### Greenvale Environmental Commission")

# hardcoding allat so that I don't need to actually make a separate csv file to read it all (ALSO DONT NEED TO SINCE ITS NOT LIKE WE'RE PUTTING NEW DATA HERE ANYWAYS)
POLLUTANTS = ["CO2","NOx","SO2","PM2.5","CH4","VOC","CO","NH3","BC","N2O"]
TARGETS = {"CO2":1000, "NOx":35, "SO2":25, "PM2.5":20, "CH4":60, "VOC":45, "CO":80, "NH3":12, "BC":6, "N2O":10}

# DA DATA
PROJECTS = [
    (1,  "Large Solar Park", 4000, [60, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (2,  "Small Solar Installations", 1200, [18, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (3,  "Wind Farm", 3800, [55, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (4,  "Gas-to-renewables conversion", 3200, [25, 1, 0.2, 0.1, 1.5, 0.5, 2, 0.05, 0.01, 0.3]),
    (5,  "Boiler Retrofit", 1400, [20, 0.9, 0.4, 0.2, 0.1, 0.05, 1.2, 0.02, 0.01, 0.05]),
    (6,  "Catalytic Converters for Buses", 2600, [30, 2.8, 0.6, 0.8, 0, 0.5, 5, 0.01, 0.05, 0.02]),
    (7,  "Diesel Bus Replacement", 5000, [48, 3.2, 0.9, 1.0, 0, 0.7, 6, 0.02, 0.08, 0.03]),
    (8,  "Traffic Signal/Flow Upgrade", 1000, [12, 0.6, 0.1, 0.4, 0.05, 0.2, 3, 0.02, 0.02, 0.01]),
    (9, "Low-Emission Stove Program", 180, [2, 0.02, 0.01, 0.7, 0, 0.01, 1.5, 0.03, 0.2, 0]),
    (10, "Residential Insulation/Efficiency", 900, [15, 0.1, 0.05, 0.05, 0.02, 0.02, 0.5, 0, 0, 0.01]),
    (11, "Industrial Scrubbers", 4200, [6, 0.4, 6, 0.4, 0, 0.1, 0.6, 0.01, 0.01, 0]),
    (12, "Waste Methane Capture System", 3600, [28, 0.2, 0.1, 0.05, 8, 0.2, 0.1, 0, 0, 0.05]),
    (13, "Landfill Gas-to-energy", 3400, [24, 0.15, 0.05, 0.03, 6.5, 0.1, 0.05, 0, 0, 0.03]),
    (14, "Reforestation (acre-package)", 220, [3.5, 0.04, 0.02, 0.01, 0.8, 0.03, 0.1, 0.01, 0.005, 0.005]),
    (15, "Urban Tree Canopy Program", 300, [4.2, 0.06, 0.01, 0.03, 0.6, 0.02, 0.15, 0.005, 0.02, 0.002]),
    (16, "Industrial Energy Efficiency Retrofit", 1600, [22, 0.5, 0.3, 0.15, 0.2, 0.1, 1, 0.01, 0.01, 0.03]),
    (17, "Natural Gas Leak Repair", 1800, [10, 0.05, 0.01, 0.01, 4, 0.02, 0.02, 0, 0, 0.01]),
    (18, "Agricultural Methane Reduction", 2800, [8, 0.02, 0.01, 0.02, 7.2, 0.05, 0.02, 0.1, 0, 0.05]),
    (19, "Clean Cookstove & Fuel Switching", 450, [3.2, 0.04, 0.02, 0.9, 0.1, 0.02, 2, 0.05, 0.25, 0]),
    (20, "Rail Electrification", 6000, [80, 2, 0.4, 1.2, 0, 0.6, 10, 0.02, 0.1, 0.05]),
    (21, "EV Charging Infrastructure", 2200, [20, 0.3, 0.05, 0.1, 0, 0.05, 0.5, 0.01, 0.01, 0.01]),
    (22, "Biochar for soils", 1400, [6, 0.01, 0, 0.01, 2.5, 0.01, 0.01, 0.2, 0, 0.02]),
    (23, "Industrial VOC Reduction", 2600, [2, 0.01, 0, 0, 0, 6.5, 0.1, 0, 0, 0]),
    (24, "Heavy-Duty Truck Retrofit", 4200, [36, 2.2, 0.6, 0.6, 0, 0.3, 4.2, 0.01, 0.04, 0.02]),
    (25, "Port/Harbor Electrification", 4800, [28, 1.9, 0.8, 0.7, 0, 0.2, 3.6, 0.01, 0.03, 0.02]),
    (26, "Black Carbon reduction", 600, [1.8, 0.02, 0.01, 0.6, 0.05, 0.01, 1, 0.02, 0.9, 0]),
    (27, "Wetlands restoration", 1800, [10, 0.03, 0.02, 0.02, 3.2, 0.01, 0.05, 0.15, 0.02, 0.04]),
    (28, "Household LPG conversion program", 700, [2.5, 0.03, 0.01, 0.4, 0.05, 0.02, 1.2, 0.03, 0.1, 0]),
    (29, "Industrial process change", 5000, [3, 0.02, 0.01, 0, 0, 0, 0, 0, 0, 1.5]),
    (30, "Behavioral demand-reduction program", 400, [9, 0.4, 0.05, 0.05, 0.01, 0.3, 2.5, 0.01, 0.01, 0.01])
]

# session state for reset/select all shenanigans
if 'selected_projects' not in st.session_state:
    st.session_state.selected_projects = set()
if 'select_all_flag' not in st.session_state:
    st.session_state.select_all_flag = False

proj_rows = []
for p in PROJECTS:
    proj_rows.append({
        "id": p[0],
        "projectname": p[1],
        "cost": p[2],
        **{POLLUTANTS[i]: p[3][i] for i in range(len(POLLUTANTS))}
    })
df_proj = pd.DataFrame(proj_rows)

st.markdown("---")
st.subheader("Select Mitigation Projects")
st.markdown("Use the table below to select projects. Click column headers to sort by Cost or Efficiency.")

# initialize table, very familiar with pandas
# using a dataframe in session state to hold the 'Selected' status
if 'project_editor_df' not in st.session_state:
    # create a copy of the base data
    df_init = df_proj.copy()
    # insert 'Selected' column at the start (default to False)
    df_init.insert(0, "Selected", False)
    st.session_state.project_editor_df = df_init

# control
col1, col2, col3 = st.columns([1, 1, 4])

# helper function to update the dataframe state
def update_selection(val):
    st.session_state.project_editor_df["Selected"] = val

with col1:
    if st.button("Select All"):
        update_selection(True)
        st.rerun()

with col2:
    if st.button("Reset"):
        update_selection(False)
        st.rerun()

# id quick select (NO NEED ANYMORE SESSIONS SAVE THE DAY)
# with st.expander("Quick Select by IDs"):
#     ids_input = st.text_input("Enter comma-separated IDs (e.g., 1, 5, 30)")
#     if st.button("Apply IDs") and ids_input:
#         try:
#             target_ids = [int(x.strip()) for x in ids_input.split(",") if x.strip()]
#             # Update 'Selected' column: True if ID is in list, False otherwise
#             st.session_state.project_editor_df["Selected"] = \
#                 st.session_state.project_editor_df["id"].isin(target_ids)
#             st.rerun()
#         except ValueError:
#             st.error("Invalid format. Please use numbers separated by commas.")


# spreadsheet to  allow user to see the data and click a checkmark button to select which projects go in
edited_df = st.data_editor(
    st.session_state.project_editor_df,
    column_config={
        "Selected": st.column_config.CheckboxColumn(
            "Select",
            help="Check to include this project",
            default=False,
        ),
        "id": st.column_config.NumberColumn("ID", format="%d", width="small"),
        "projectname": st.column_config.TextColumn("Project Name", width="large"),
        "cost": st.column_config.NumberColumn("Cost ($)", format="$%d"),
        # Format pollutants to 2 decimal places for cleaner look
        **{pol: st.column_config.NumberColumn(pol, format="%.2f") for pol in POLLUTANTS}
    },
    disabled=["id", "projectname", "cost"] + POLLUTANTS, # User can ONLY edit the 'Selected' column
    hide_index=True,
    use_container_width=True,
    height=500  # Fixed height with scrollbar
)

# save manual edits back to session state so they persist
st.session_state.project_editor_df = edited_df

# extract the IDs of selected rows to pass to the Rscript
selected_rows = edited_df[edited_df["Selected"]]
selected = selected_rows["id"].tolist()
st.session_state.selected_projects = set(selected)

st.markdown("---")

# SUMMARY
if len(selected) == 0:
    st.warning("No projects selected. Please select at least one project before solving.")
elif len(selected) == 30:
    st.info(f"**All {len(selected)} projects selected**")
else:
    st.info(f"**{len(selected)} project(s) selected**: {', '.join(map(str, sorted(selected)))}")

# SOLVE
st.markdown("---")
if st.button("Calculate Optimal Mix", type="primary", disabled=(len(selected) == 0)):
    with st.spinner("Solving linear program..."):
        # Build LP for selected projects
        sel_df = df_proj[df_proj["id"].isin(selected)].reset_index(drop=True)
        n = len(sel_df)
        m = len(POLLUTANTS)

        c = sel_df["cost"].values.tolist()
        A = []
        for pol in POLLUTANTS:
            A.append(sel_df[pol].values.tolist())
        b = [TARGETS[pol] for pol in POLLUTANTS]

        # DEBUG: Print constraint info
        st.write("### DEBUG INFO")
        st.write(f"Number of projects (n): {n}")
        st.write(f"Number of pollutants (m): {m}")
        st.write(f"Targets: {b}")
        
        # Check if problem is theoretically feasible
        A_np = np.array(A)
        max_reductions = []
        for j in range(m):
            # Maximum possible reduction for pollutant j if we use 20 units of every project (which is yes that's the idea here)
            max_red = sum(A_np[j, :] * 20)
            max_reductions.append(max_red)
            st.write(f"Pollutant {POLLUTANTS[j]}: Target={b[j]}, Max possible={max_red:.2f}")
        
        # Check feasibility
        feasible_check = all(max_reductions[j] >= b[j] for j in range(m))
        if not feasible_check:
            st.error("PROBLEM IS THEORETICALLY INFEASIBLE!")
            st.write("Even with 20 units of each project, cannot meet all targets.")
            for j in range(m):
                if max_reductions[j] < b[j]:
                    st.write(f"{POLLUTANTS[j]}: Need {b[j]}, can only get {max_reductions[j]:.2f}")
        else:
            st.success("Problem appears theoretically feasible")

        st.write("### Converting to Dual Problem (Maximization)")
        
        # Primal problem construction
        # Dual: Maximize W = b*y - 20*u
        # Standard Simplex Tableau for Max W: (Row 0) Z - b*y + 20*u = 0
        # need coefficients: -b for y, +20 for u. (just like how you'd construct the initial tableau)
        
        A_transpose = A_np.T
        dual_decision_vars = m + n
        dual_constraints = n
        
        st.write(f"Dual problem: {dual_decision_vars} variables, {dual_constraints} constraints")
        
        tableau = []
        
        # build n constraint rows: A^T*y - u <= c
        for i in range(n):
            row = []
            # Coefficients for y
            row.extend(A_transpose[i, :].tolist())
            # Coefficients for u
            u_coeffs = [-1 if j == i else 0 for j in range(n)]
            row.extend(u_coeffs)
            # Slack variable
            slack = [1 if j == i else 0 for j in range(n)]
            row.extend(slack)
            # RHS should be at c[i]
            row.append(c[i])
            tableau.append(row)
        
        # objectiv row
        obj_row = []
        obj_row.extend([-val for val in b])  # -b for the objective row
        obj_row.extend([20] * n)             # +20 (constraints)
        obj_row.extend([0] * n)              # Slacks
        obj_row.append(0)                    # RHS
        tableau.append(obj_row)

        st.write(f"Dual tableau: {len(tableau)} rows × {len(tableau[0])} columns")
        
        # set isMax=True so R does NOT flip our signs since the signs are already flipped (did not bother to remove this bool)
        payload = {"tableau": tableau, "isMax": True}
        
        try:
            r = requests.post("https://cmsc150finalproject.onrender.com/simplex", 
                            data=json.dumps(payload), 
                            headers={"Content-Type":"application/json"}, 
                            timeout=30)
            
            if r.status_code != 200:
                st.error(f"Backend error: {r.status_code} {r.text}")
            else:
                res = r.json()
                
                # check for error/infeasibility DEBUGG
                if res.get("infeasible") == True or ("error" in res and res["error"]):
                    st.error("### The problem is infeasible or unbounded.")
                    if "error" in res:
                        st.error(f"Details: {res['error']}")
                else:
                    st.success("### Optimization Complete!")
                    
                    finalTableau = res["finalTableau"]
                    if isinstance(finalTableau, list) and len(finalTableau) > 0 and isinstance(finalTableau[0], dict):
                        df_tableau = pd.DataFrame(finalTableau)
                        # sort columns numerically (V1, V2...V10)
                        import re
                        def sort_key(col_name):
                            match = re.search(r'(\d+)', str(col_name))
                            return int(match.group(1)) if match else 0
                        sorted_cols = sorted(df_tableau.columns, key=sort_key)
                        tableau_array = df_tableau[sorted_cols].values
                    elif isinstance(finalTableau, dict):
                         # handle dict format
                        first_key = next(iter(finalTableau))
                        num_rows = len(finalTableau[first_key])
                        num_cols = len(finalTableau)
                        tableau_array = np.zeros((num_rows, num_cols))
                        for col_idx in range(num_cols):
                            col_key = str(col_idx) if str(col_idx) in finalTableau else f"V{col_idx+1}"
                            if col_key in finalTableau:
                                tableau_array[:, col_idx] = finalTableau[col_key]
                    else:
                        tableau_array = np.array(finalTableau)

                    last_row = tableau_array[-1, :]
                    
                    # primal values
                    slack_start_col = m + n
                    xvals = last_row[slack_start_col:slack_start_col + n].tolist()
                    
                    optimal_cost = last_row[-1]
                    
                    st.write("### Solution Extraction from Dual")
                    st.write(f"Primal optimal cost: {optimal_cost:,.2f}")
                    st.write(f"Last row has {len(last_row)} elements")
                    st.write(f"Slack columns: {slack_start_col} to {slack_start_col + n - 1}")
                    st.write(f"Primal x values (from dual slacks): {[round(x, 4) for x in xvals[:30]]}")
                    st.write(f"Dual Z: {res['Z']}")
                    st.write(f"Primal optimal cost: {optimal_cost}")
                    
                    # input section of the webpage
                    st.markdown("---")
                    st.markdown("### Your Input")
                    if len(selected) == 30:
                        st.markdown("You selected **all** the possible mitigation projects")
                    else:
                        st.markdown(f"You selected **{len(selected)} projects**:")
                        project_names = [df_proj[df_proj['id'] == pid]['projectname'].values[0] for pid in sorted(selected)]
                        for name in project_names:
                            st.markdown(f"• {name}")
                    
                    # results section
                    st.markdown("---")
                    st.markdown("### The Optimized Cost")
                    st.markdown(f"## ${optimal_cost:,.2f}")
                    st.caption("The cost of this optimal mitigation project")
                    
                    st.markdown("---")
                    st.markdown("### The Solution and Cost Breakdown by Mitigation Project")
                    
                    breakdown = []
                    for i, xi in enumerate(xvals):
                        if abs(xi) > 0.0001:  # Only show non-zero allocations
                            project = sel_df.iloc[i]["projectname"]
                            cost_per_unit = sel_df.iloc[i]["cost"]
                            total_cost_item = abs(xi) * cost_per_unit
                            breakdown.append({
                                "Mitigation Project": project,
                                "Number of Project Units": round(abs(xi), 6),
                                "Cost ($)": f"${total_cost_item:,.2f}"
                            })
                    
                    if breakdown:
                        st.table(pd.DataFrame(breakdown))
                    else:
                        st.info("No projects allocated (all values zero)")
                    
                    # iteration section based on project specs
                    st.markdown("---")
                    st.markdown("### Simplex Tableau Iterations (Dual Problem)")
                    
                    if "iterations" in res and res["iterations"]:
                        for iter_data in res["iterations"]:
                            raw_iter = iter_data.get("iteration", 0)
                            # Handle case where R returns a list like [1] HAPPENED TOO MANY TIMES BEFORE
                            if isinstance(raw_iter, list):
                                iter_num = raw_iter[0]
                            else:
                                iter_num = raw_iter                            
                            with st.expander(f"Iteration {iter_num}" + (" (Initial)" if iter_num == 0 else ""), 
                                           expanded=(iter_num == 0)):
                                if iter_num > 0:
                                    st.markdown(f"""
                                    **Pivot Row:** {iter_data.get('pivotRow', 'N/A')}  
                                    **Pivot Column:** {iter_data.get('pivotCol', 'N/A')}  
                                    **Pivot Element:** {iter_data.get('pivotElement', 'N/A')}
                                    """)
                                st.dataframe(pd.DataFrame(iter_data["tableau"]))
                    else:
                        st.info("Iteration data not available")
                    
                    # FINAL TABLEAU
                    st.markdown("---")
                    with st.expander("Final Tableau", expanded=False):
                        st.dataframe(pd.DataFrame(res["finalTableau"]))
                        
        except requests.exceptions.RequestException as e:
            st.error("Could not reach R backend. Make sure plumber is running at https://cmsc150finalproject.onrender.com/simplex")
            st.error(f"Error details: {str(e)}")
# Footer
st.markdown("---")
st.caption("Greenvale Environmental Commission | Pollution Reduction Optimization System")