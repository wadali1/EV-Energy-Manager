import streamlit as st
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB
import time
import plotly.graph_objects as go
import seaborn as sns
import numpy as np

# Simulated database of users
USER_CREDENTIALS = {
    "anmoljeet.wadali": "test123",
    "admin":"test123",
    "testuser": "test123"
}

# Function to check login credentials
def authenticate_user(username, password):
    return USER_CREDENTIALS.get(username.lower()) == password

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# 🚀 Login Page
def login_page():
    st.title("EV Energy Manager")

    username_input = st.text_input("Username", key="user_input",placeholder="Enter your username")
    password_input = st.text_input("Password", type="password", key="pass_input",placeholder="Enter your password")
    login_button = st.button("Login")

    if login_button:
        if authenticate_user(username_input, password_input):
            st.session_state.logged_in = True
            st.session_state.current_user = username_input  # Update the session state variable
            st.success("✅ Login successful! Redirecting...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Incorrect username or password")

# 🚪 Logout Function
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.rerun()


def dashboard():
    # Set up Streamlit page
    st.set_page_config(page_title="EV Energy Manager - Login", page_icon="⚡", layout="centered")

    # Title and Description
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>⚡ EV Energy Manager</h1>
            <h3>A smart dashboard for monitoring EV charging and energy distribution</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar Navigation
    st.sidebar.text(f"Welcome 🙏 {st.session_state.current_user} ")
    st.sidebar.header("Navigation")
    if st.sidebar.button("Logout"):
        logout()
    page = st.sidebar.radio("Go to:", ["Home", "Charging Overview", "Energy Analysis", "Optimization Analysis"])

    # Sidebar Configuration
    st.sidebar.header("⚙️ Configuration")
    num_level2_chargers = st.sidebar.slider("Level 2 Chargers", 1, 10, 5)
    num_level3_chargers = st.sidebar.slider("Level 3 Chargers", 1, 5, 3)

    st.sidebar.header("💰 Cost Estimation")

    # User inputs for power rating
    power_level2 = st.sidebar.slider("Power Rating (kW) - Level 2 Charger", 3, 19, 7)  # Level 2 chargers: 3kW to 19kW
    power_level3 = st.sidebar.slider("Power Rating (kW) - Level 3 Charger", 50, 350, 150)  # Level 3 chargers: 50kW to 350kW

    # Charging time per day
    charging_hours = st.sidebar.slider("Charging Time per Day (hours)", 1, 24, 5)

    # Cost per kWh
    cost_per_kWh = st.sidebar.number_input("Electricity Cost per kWh ($)", min_value=0.01, max_value=1.0, value=0.15, step=0.01)

    # Calculate energy consumption (kWh) per day
    energy_level2 = num_level2_chargers * power_level2 * charging_hours
    energy_level3 = num_level3_chargers * power_level3 * charging_hours

    # Total energy consumption
    total_energy = energy_level2 + energy_level3

    # Cost calculations
    daily_cost = total_energy * cost_per_kWh
    monthly_cost = daily_cost * 30  # Assuming 30 days per month

    # Display results in a structured way
    st.sidebar.markdown("### 🔢 Cost Breakdown")

    col1, col2 = st.sidebar.columns(2)
    col1.metric("⚡ Total Energy (kWh/day)", f"{total_energy:.2f} kWh")
    col2.metric("💲 Daily Cost", f"${daily_cost:.2f}")

    st.sidebar.metric("📅 Monthly Cost", f"${monthly_cost:.2f}", delta=f"{daily_cost:.2f}/day", delta_color="inverse")

    # Energy Data
    hours = list(range(24))
    load_demand = [5, 4, 3, 3, 4, 6, 8, 10, 12, 14, 13, 12, 11, 10, 8, 7, 9, 10, 11, 12, 11, 8, 6, 5]  # kW
    pv_generation = [0, 0, 0, 1, 2, 3, 5, 7, 9, 10, 9, 8, 7, 5, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0]  # kW

    if page == "Home":
        st.markdown("<h2>🏠 Welcome to the EV Energy Manager Dashboard!</h2>", unsafe_allow_html=True)
        st.markdown("<p>Use the sidebar to navigate different sections and customize filters.</p>", unsafe_allow_html=True)

    elif page == "Charging Overview":
        st.markdown("<h2>📊 Charging Overview</h2>", unsafe_allow_html=True)
        st.markdown("<p>This section will display real-time charging statistics and insights.</p>", unsafe_allow_html=True)

    elif page == "Energy Analysis":
        st.markdown("<h2>🔍 Energy Analysis</h2>", unsafe_allow_html=True)
        st.markdown("<p>This section provides a visualization of Load Demand vs PV Generation.</p>", unsafe_allow_html=True)

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(hours, load_demand, label="Load Demand (kW)", marker="o", linestyle="-", color="blue")
        ax.plot(hours, pv_generation, label="PV Generation (kW)", marker="s", linestyle="--", color="green")

        ax.set_xlabel("Hour of the Day")
        ax.set_ylabel("Power (kW)")
        ax.set_title("Load Demand vs PV Generation")
        ax.legend()
        ax.grid(True)

        # Display the plot in Streamlit
        st.pyplot(fig)

    elif page == "Optimization Analysis":
        st.markdown("<h2>🧠 Optimization Analysis</h2>", unsafe_allow_html=True)
        st.markdown("<p>Optimizing energy usage with Solar, battery and grid integration.</p>", unsafe_allow_html=True)

        # Optimization Parameters
        #battery_capacity = 20  # kWh
        battery_capacity = st.slider("Select battery_capacity (Kwh):", min_value=0, max_value=50,value= 25, step=1)

        battery_soc_min = 0.2 * battery_capacity
        battery_soc_max = 0.8 * battery_capacity
        battery_power_max = 5  # kW
        eta_charge = 0.9
        eta_discharge = 0.9
        #cost_grid = 0.15  # $/kWh
        cost_pv = st.number_input("Cost of Electricity from PV($/kwh):", min_value=0.0,value=0.0, max_value=10.0, step=0.1, format="%.2f")
        COST_GRID = st.number_input("Cost of Electricity from grid($/kwh):", min_value=0.0,value=1.25, max_value=10.0, step=0.1, format="%.2f")
        #Incorporated time-of-use (TOU) pricing, where the cost of power from the grid is reduced after 7 PM (hour 19)
        cost_grid = {t:COST_GRID  if t < 19 else 0.5*COST_GRID for t in hours} 

        #cost_battery = 0.05  # $/kWh
        cost_battery=st.number_input("Cost of Electricity from battery($/kwh):", min_value=0.0,value=0.05, max_value=10.0, step=0.1, format="%.2f")
        soc_initial = 0.5 * battery_capacity

        if st.button('Run Optimisation!!'):
            # Create model
            with st.spinner("⚡ Running optimization, please wait..."):
                time.sleep(5)
                model = gp.Model("Smart_Microgrid_Optimization")

                # Decision variables
                P_pv = model.addVars(hours, lb=0, ub={t: pv_generation[t] for t in hours}, name="P_pv")
                P_bat = model.addVars(hours, lb=-battery_power_max, ub=battery_power_max, name="P_bat")
                P_grid = model.addVars(hours, lb=0, name="P_grid")
                SOC = model.addVars(hours, lb=battery_soc_min, ub=battery_soc_max, name="SOC")
                P_bat_charge = model.addVars(hours, lb=0, ub=battery_power_max, name="P_bat_charge")
                P_bat_discharge = model.addVars(hours, lb=0, ub=battery_power_max, name="P_bat_discharge")

                # Linking charge and discharge components to P_bat
                for t in hours:
                    model.addConstr(P_bat[t] == P_bat_discharge[t] - P_bat_charge[t], f"Bat_Charge_Discharge_{t}")

                # Objective function: Minimize total cost
                model.setObjective(
                    gp.quicksum(P_pv[t]*cost_pv+cost_battery * P_bat_discharge[t] + cost_grid[t] * P_grid[t] for t in hours),
                    GRB.MINIMIZE
                )

                # Constraints
                # Load balancing constraint
                for t in hours:
                    model.addConstr(P_pv[t] + P_bat[t] + P_grid[t] == load_demand[t], f"Load_Balance_{t}")

                # Battery SOC constraints
                model.addConstr(SOC[0] == soc_initial, "Initial_SOC")
                for t in hours[1:]:
                    model.addConstr(
                        SOC[t] == SOC[t-1] + eta_charge * P_bat_charge[t-1] - P_bat_discharge[t-1] / eta_discharge,
                        f"SOC_Update_{t}"
                    )

                # PV generation constraint
                for t in hours:
                    model.addConstr(P_pv[t] <= pv_generation[t], f"PV_Limit_{t}")

                # Optimize the model
                model.optimize()

                # Check if the model found an optimal solution
                if model.status == GRB.OPTIMAL:
                    st.success("Optimization successful! ✅")
                    
                    # Extracting results
                    optimized_pv = [P_pv[t].X for t in hours]
                    optimized_battery = [P_bat[t].X for t in hours]
                    optimized_grid = [P_grid[t].X for t in hours]
                    optimized_soc = [SOC[t].X for t in hours]

                    # Plot the results
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(hours, optimized_pv, label="Optimized PV (kW)", marker="o", linestyle="-", color="green")
                    ax.plot(hours, optimized_battery, label="Optimized Battery (kW)", marker="s", linestyle="--", color="red")
                    ax.plot(hours, optimized_grid, label="Grid Power (kW)", marker="^", linestyle=":", color="black")
                    ax.plot(hours, optimized_soc, label="SOC (kWh)", marker="d", linestyle="dashdot", color="purple")

                    ax.set_xlabel("Hour of the Day")
                    ax.set_ylabel("Power (kW) / SOC (kWh)")
                    ax.set_title("Optimized Energy Distribution")
                    ax.legend()
                    ax.grid(True)

                    # Show the plot
                    st.pyplot(fig)

                    # Create an interactive plot using Plotly
                    fig = go.Figure()

                    fig.add_trace(go.Scatter(x=hours, y=optimized_pv, mode='lines+markers', name='Optimized PV (kW)', line=dict(color='green')))
                    fig.add_trace(go.Scatter(x=hours, y=optimized_battery, mode='lines+markers', name='Optimized Battery (kW)', line=dict(color='red', dash='dash')))
                    fig.add_trace(go.Scatter(x=hours, y=optimized_grid, mode='lines+markers', name='Grid Power (kW)', line=dict(color='black', dash='dot')))
                    fig.add_trace(go.Scatter(x=hours, y=optimized_soc, mode='lines+markers', name='SOC (kWh)', line=dict(color='purple', dash='longdash')))

                    # Add layout details
                    fig.update_layout(
                        title="Optimized Energy Distribution",
                        xaxis_title="Hour of the Day",
                        yaxis_title="Power (kW) / SOC (kWh)",
                        legend_title="Legend",
                        template="plotly_dark"
                    )

                    # Display the interactive Plotly chart
                    st.plotly_chart(fig, use_container_width=True)

                    # Display detailed results
                    #if st.checkbox("### Show Hourly Results"):
                    st.markdown("### Optimization Results :")
                    hourly_costs = {}
                    total_cost = 0
                    with st.expander("Show Hourly Results"):
                        for t in range(24): 
                            pv = P_pv[t].X
                            battery = P_bat[t].X
                            grid = P_grid[t].X
                            soc = SOC[t].X
                            hour_cost = cost_battery * P_bat[t].X + cost_grid[t] * grid  # Compute hourly cost
                            hourly_costs[t] = hour_cost
                            total_cost += hour_cost
                            st.write(f"**Hour {t}:** PV={optimized_pv[t]:.2f} kW, Battery={optimized_battery[t]:.2f} kW, Grid={optimized_grid[t]:.2f} kW, SOC={optimized_soc[t]:.2f} kWh ,Cost=${hour_cost:.2f}")
                            #print(f"Hour {t}: PV={pv:.2f} kW, Battery={battery:.2f} kW, Grid={grid:.2f} kW, SOC={soc:.2f} kWh, Cost=${hour_cost:.2f}")
                    st.markdown(f"Total Cost: ${total_cost:.2f}")
                    st.balloons()
            

                else:
                    st.error("Optimization failed. ❌")

# 🛠 Run the login system first, then dashboard if authenticated
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()

