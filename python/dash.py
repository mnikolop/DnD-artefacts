import streamlit as st
import pandas as pd
import numpy as np


st.title('Dungeons & Dragons Monsters')

monsters = pd.read_json('../data/creatures/srd_5e_monsters.json')

monsters = monsters[['name', 'meta', 'Armor Class', 'Hit Points', 'Speed', 'STR', 'STR_mod',
                     'DEX', 'DEX_mod', 'CON', 'CON_mod', 'INT', 'INT_mod', 'WIS', 'WIS_mod',
                     'CHA', 'CHA_mod', 'Saving Throws', 'Skills', 'Senses', 'Languages',
                     'Challenge', 'Damage Immunities', 'Condition Immunities', 'Damage Resistances',
                     'Damage Vulnerabilities', 'Reactions']]

monsters = monsters.rename(columns={"Armor Class": "AC", 
                         "Hit Points": "HP", 
                         "Saving Throw": "SavavingThrows",
                         "Damage Immunities": "DamageImmunitites", 
                         "Condition Immunities": "ConditionImmunities",
                         'Damage Resistances': 'DamageResistances',
                         'Damage Vulnerabilities': 'DamageVulnerabilities'})




if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(monsters)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)


names = st.multiselect(
    "Choose Monster(s)", list(monsters.name), []
)
if not names:
    st.error("Please select at least one Monster.")
else:
    # st.write(monsters[monsters['name'].isin(names)] )
    data = monsters[monsters['name'].isin(names)]
    # st.write(data.sort_index())

    data = data.reset_index()
    data = pd.melt(data, id_vars=["index"]).rename(
        columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    )
    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.3)
        .encode(
            x="year:T",
            y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
            color="Region:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)
