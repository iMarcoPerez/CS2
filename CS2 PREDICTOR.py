import streamlit as st

# Streamlit app for CS2 predictions
st.title("CS2 Over/Under Predictor with Team Strength Integration")

# Player and match details
player_name = st.text_input("Player Name", "Beastik")
col1, col2 = st.columns(2)
with col1:
    kills_bet_line = st.number_input("Bet Line for Kills", value=26.5, min_value=0.0, step=0.1)
with col2:
    headshots_bet_line = st.number_input("Bet Line for Headshots", value=15.5, min_value=0.0, step=0.1)

player_team = st.text_input("Player's Team", "Sinners Esports")
opponent_team = st.text_input("Opponent Team", "Monte")

# Team Strength Metrics
st.subheader("Team Strength Metrics")
player_team_win_rate = st.number_input(f"{player_team} Win Rate (%)", value=60, min_value=0, max_value=100)
opponent_team_win_rate = st.number_input(f"{opponent_team} Win Rate (%)", value=70, min_value=0, max_value=100)
player_team_kd_ratio = st.number_input(f"{player_team} K/D Ratio", value=1.1, min_value=0.0, step=0.1)
opponent_team_kd_ratio = st.number_input(f"{opponent_team} K/D Ratio", value=1.2, min_value=0.0, step=0.1)

# Section 1: Last 5 Matches
st.subheader("Player Performance (Last 5 Matches)")
kills_last_5 = st.text_input("Kills in Last 5 Matches (comma-separated)", "20,18,22,15,19")
headshots_last_5 = st.text_input("Headshots in Last 5 Matches (comma-separated)", "8,7,12,10,9")

# Section 2: Head-to-Head Performance
st.subheader(f"Head-to-Head Performance Against {opponent_team}")
kills_head_to_head = st.text_input("Kills in Head-to-Head Matches (comma-separated)", "15,14,16,18,17")
headshots_head_to_head = st.text_input("Headshots in Head-to-Head Matches (comma-separated)", "6,5,7,8,6")

# Calculate adjusted averages
if st.button("Calculate Adjusted Performance"):
    try:
        # Parse inputs
        kills_5 = list(map(int, kills_last_5.split(",")))
        kills_h2h = list(map(int, kills_head_to_head.split(",")))
        headshots_5 = list(map(int, headshots_last_5.split(",")))
        headshots_h2h = list(map(int, headshots_head_to_head.split(",")))

        # Calculate averages
        avg_kills_last_5 = sum(kills_5) / len(kills_5)
        avg_kills_h2h = sum(kills_h2h) / len(kills_h2h)
        avg_headshots_last_5 = sum(headshots_5) / len(headshots_5)
        avg_headshots_h2h = sum(headshots_h2h) / len(headshots_h2h)

        # Adjust based on team strength
        team_strength_factor = (player_team_kd_ratio / opponent_team_kd_ratio) * (player_team_win_rate / opponent_team_win_rate)
        team_adjustment_kills = (team_strength_factor - 1) * avg_kills_last_5  # Adjust relative to recent performance
        team_adjustment_headshots = (team_strength_factor - 1) * avg_headshots_last_5

        # Weighted adjustment
        adjusted_kills = (avg_kills_last_5 * 0.5) + (avg_kills_h2h * 0.3) + (team_adjustment_kills * 0.2)
        adjusted_headshots = (avg_headshots_last_5 * 0.5) + (avg_headshots_h2h * 0.3) + (team_adjustment_headshots * 0.2)

        # Display results
        st.write(f"**Adjusted Kills Prediction:** {adjusted_kills:.2f} kills")
        st.write(f"**Adjusted Headshots Prediction:** {adjusted_headshots:.2f} headshots")

        # Compare with betting lines
        if adjusted_kills >= kills_bet_line:
            st.success(f"Prediction: **{player_name} is expected to hit over {kills_bet_line} kills.**")
        else:
            st.error(f"Prediction: **{player_name} is expected to go under {kills_bet_line} kills.**")

        if adjusted_headshots >= headshots_bet_line:
            st.success(f"Prediction: **{player_name} is expected to hit over {headshots_bet_line} headshots.**")
        else:
            st.error(f"Prediction: **{player_name} is expected to go under {headshots_bet_line} headshots.**")

    except ValueError:
        st.error("Error: Please ensure all inputs are numeric and comma-separated.")
