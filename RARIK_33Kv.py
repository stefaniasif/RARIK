# RARIK_33Kv.py
import pandapower as pp
import pandapower.plotting as pplot
import matplotlib.pyplot as plt


net = pp.create_empty_network()

# Create buses
bus1 = pp.create_bus(net, name="132kv Prestbakki Transformer Bus 1", vn_kv=132, type="b")
bus2 = pp.create_bus(net, name="33kv Prestbakki Transformer Bus 2", vn_kv=33, type="b")

bus3 = pp.create_bus(net, name="Bus 3", vn_kv=33, type="n")
bus4 = pp.create_bus(net, name="Bus 4", vn_kv=33, type="n")
bus5 = pp.create_bus(net, name="Bus 5", vn_kv=33, type="n")

bus6 = pp.create_bus(net, name="33kv Vik Transformer Bus 6", vn_kv=33, type="b")
#bus7 = pp.create_bus(net, name="33kv Vik Transformer Bus 7", vn_kv=33, type="n")


# Ensure bus_geodata has columns for x and y coordinates
if net.bus_geodata.empty:
    net.bus_geodata = net.bus_geodata.reindex(columns=["x", "y"])

# Add coordinates for the buses
net.bus_geodata.loc[bus1] = [0, 0]  # Coordinates for Bus 1
net.bus_geodata.loc[bus2] = [0, -1]  # Coordinates for Bus 2
net.bus_geodata.loc[bus3] = [-0.5, -2]  # Coordinates for Bus 3
net.bus_geodata.loc[bus4] = [-1.5, -2]  # Coordinates for Bus 4
net.bus_geodata.loc[bus5] = [-2.5, -2]  # Coordinates for Bus 5
net.bus_geodata.loc[bus6] = [-3, -1]  # Coordinates for Bus 6
# net.bus_geodata.loc[bus7] = [-3, 0]  # Coordinates for Bus 7 


# Create external grid
pp.create_ext_grid(net, bus1, vm_pu=1.00, va_degree=0, name= "Aðveitustöð Prestbakka")
# pp.create_ext_grid(net, bus7, vm_pu=1.00, va_degree=0, name= "Aðveitustöð Vík í Mýrdal")


# Create transformers

# Define HV transformer parameters
sn_mva = 30         # Rated apparent power in MVA
vn_hv_kv = 132      # High voltage side (primary) rated voltage in kV
vn_lv_kv = 33       # Low voltage side (secondary) rated voltage in kV
vk_percent = 10     # Short-circuit voltage (%)
vkr_percent = 0.5   # Real part of short-circuit impedance (%)
pfe_kw = 30         # Iron (core) losses (kW), (ca. kw per mva!)
i0_percent = 0.07   # No-load, Magnetizing current (%)
shift_degree = 0    # Phase shift between HV and LV sides (e.g., delta-star configuration)

# Create the HV transformer
pp.create_transformer_from_parameters(
    net, bus1, bus2,
    sn_mva=sn_mva,
    vn_hv_kv=vn_hv_kv,
    vn_lv_kv=vn_lv_kv,
    vk_percent=vk_percent,
    vkr_percent=vkr_percent,
    pfe_kw=pfe_kw,
    i0_percent=i0_percent,
    shift_degree=shift_degree,
    name="132/33 kV Transformer"
)

# sleppum við auka spenni til að tengjast yfir í Rimakot ef spennan er 33Kv


# Create lines
# Fæ útreiknað 437 A: 25MW/(sqrt(3)*33kv)

# Define line parameters

loftlina_66_feal300 = {
    'r_ohm_per_km': 0.061,  # resistance in ohm per km
    'x_ohm_per_km': 0.358,   # reactance in ohm per km
    'c_nf_per_km': 10.28,    # capacitance in nF per km
    'max_i_ka': 1.140       # maximum current in kA
}
strengur_33_TXSP_AL_3x1x800 = {
    'r_ohm_per_km': 0.037,  # resistance in ohm per km
    'x_ohm_per_km': 0.16,   # reactance in ohm per km
    'c_nf_per_km': 350,    # capacitance in nF per km
    'max_i_ka': 0.780       # maximum current in kA    gildi m.v. samskonar streng, má bara keyra 60%-70% af hitaþolsstraum
}
strengur_36_AXAL_1x3x300 = {     # ÞRÍLEIÐARI
    'r_ohm_per_km': 0.1,  # resistance in ohm per km
    'x_ohm_per_km': 0.18,   # reactance in ohm per km
    'c_nf_per_km': 230,    # capacitance in nF per km
    'max_i_ka': 0.500       # maximum current in kA    gildi m.v. samskonar streng, má bara keyra 60%-70% af hitaþolsstraum
}



Utfaerslur = {
    'Leid_1': { # 1, jarðstrengur í sömu lengd og núverandi tenging, 79.7 km, keyrður á 61% af hitaþolsstraum
        'lines': [
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=19.925, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 1 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=19.925, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 2 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=19.925, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 3 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=19.925, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 4 - 3x1x800")
        ],
        'shunts':[ # ef gildin á þéttunum eru hækkuð þá lækkar cosphi en launaflsframleiðsla eykst
            pp.create_shunt(net, bus6, q_mvar= 0*-2.0, p_mw=0, name="Þéttir"),   # negative for capacitive reactive compensation
            pp.create_shunt(net, bus4, q_mvar= 0.0, p_mw=0, name="Þéttir"),   # of dýrt að sögn Magga að hafa auka spólur á miðri leið
            pp.create_shunt(net, bus2, q_mvar= 0*-4.0, p_mw=0, name="Þéttir")   # positive for inductive reactive compensation
        ]   # spólur settar þannig að 2/3 sé í stöð, 1/3 í aðveitustöð Vík
    },
    'Leid_2': { #2,  jarðstrengur sem fylgir þjóðveginum, 76.4km, keyrður á 61% af hitaþolsstraum
        'lines': [  # LÍTIL LAUNAFLSFRAMLEIÐSLA, KOSTUR FYRIR FLÖKT Í ÁLAGI
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=19.1, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 1 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=19.1, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 2 - 3X1X800"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=19.1, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 3 - 3X1X800"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=19.1, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 4 - 3X1X800")
        ],
        'shunts':[
            pp.create_shunt(net, bus6, q_mvar=-2.0, p_mw=0, name="Þéttir"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Þéttir"),   # mjög dýrt að hafa auka tengivirki bara f.spólu
            pp.create_shunt(net, bus3, q_mvar=-4.0, p_mw=0, name="Þéttir")   
        ]   
    },      
    'Leid_3': {
        'lines': [  # jarðstrengurinn er þá keyrður á 62% af hitaþolsstraum
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=29.7, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 1 - 3X1X800"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=17.3, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 2 - 3X1X800"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=23.7, **loftlina_66_feal300, name="Loftlína 1 - 66_feal300"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=9.0 , **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 3 - 3X1X800")
        ],
        'shunts':[
            pp.create_shunt(net, bus6, q_mvar=-6.0, p_mw=0, name="Þéttir"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Þéttir"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus5, q_mvar=0.0, p_mw=0, name="Þéttir"),   # hægt að setja þétti hér til að rétta af spennu/cosphi
            pp.create_shunt(net, bus3, q_mvar=-4.0, p_mw=0, name="Þéttir")   # positive for inductive reactive compensation
        ]
    },
    'Leid_4': {
        'lines': [  # TVÆR ÞRÍLEIÐARATENGINGAR
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=19.1, **strengur_36_AXAL_1x3x300, name="Jarðstrengur 1.1 - þríleiðari"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=19.1, **strengur_36_AXAL_1x3x300, name="Jarðstrengur 1.2 - þríleiðari"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=19.1, **strengur_36_AXAL_1x3x300, name="Jarðstrengur 1.3 - þríleiðari"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=19.1, **strengur_36_AXAL_1x3x300, name="Jarðstrengur 1.4 - þríleiðari"),
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=19.1, **strengur_36_AXAL_1x3x300, name="Jarðstrengur 2.1 - þríleiðari"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=19.1, **strengur_36_AXAL_1x3x300, name="Jarðstrengur 2.2 - þríleiðari"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=19.1, **strengur_36_AXAL_1x3x300, name="Jarðstrengur 2.3 - þríleiðari"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=19.1, **strengur_36_AXAL_1x3x300, name="Jarðstrengur 2.4 - þríleiðari")
        ],
        'shunts':[
            pp.create_shunt(net, bus6, q_mvar=-2.0, p_mw=0, name="Þéttir"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Þéttir"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus3, q_mvar=-4.0, p_mw=0, name="Þéttir")   # positive for inductive reactive compensation
        ]   # spólurnar minnka launafl en auka spennufall, cosphi vel innan marka svo þarf ekki spólu
    },
    'Leid_5': {
        'lines': [
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=29.7, **loftlina_66_feal300, name="Loftlína 1 - FEAL 1x300"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=17.3, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 1 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=23.7, **loftlina_66_feal300, name="Loftlína 2 - FEAL 1x300"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=9.0 , **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 2 - 3x1x800")
        ],
        'shunts':[ # ef gildin á þéttunum eru hækkuð þá lækkar cosphi en spennan í Vík hækkar upp í 1.13pu, cosphi núna 0.904
            pp.create_shunt(net, bus6, q_mvar=-8.8, p_mw=0, name="Þéttir"),   # negative for capacitive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=-1.0, p_mw=0, name="Þéttir"),   # of dýrt að sögn Magga að hafa auka spólur á miðri leið
            pp.create_shunt(net, bus3, q_mvar=-3.5, p_mw=0, name="Þéttir")   # positive for inductive reactive compensation
        ]   # spólur settar þannig að 2/3 sé í stöð, 1/3 í aðveitustöð Vík
    }
}

def activate_leid(leid_name, activate=True):
    """ Activate or deactivate a leid (set of lines and shunts). """
    if leid_name in Utfaerslur:
        # Activate or deactivate lines
        for line_idx in Utfaerslur[leid_name]['lines']:
            net.line.at[line_idx, 'in_service'] = activate

        # Activate or deactivate shunts
        for shunt_idx in Utfaerslur[leid_name]['shunts']:
            net.shunt.at[shunt_idx, 'in_service'] = activate

        print(f"{leid_name} {'activated' if activate else 'deactivated'}.")
    else:
        print(f"Error: {leid_name} not found.")


# Velja leiðir og sett af spólum
activate_leid('Leid_1', activate=True)  # Activate leid_1 (both lines and shunts)
activate_leid('Leid_2', activate=False)  # Activate leid_2 (both lines and shunts)
activate_leid('Leid_3', activate=False)  # Activate leid_3 (both lines and shunts)
activate_leid('Leid_4', activate=False)  # Activate leid_4 (both lines and shunts)
activate_leid('Leid_5', activate=False)  # Activate leid_5 (both lines and shunts)


# Create load
pp.create_load(net, bus6, p_mw=25, q_mvar=0, name="Vík í Mýrdal load")#


# Create switches
#sw1 = pp.create_switch(net, bus1, pp.get_element_index(net, "trafo", '132/66 kV Transformer'), et="t", type="LBS", closed=True)
#sw2 = pp.create_switch(net, bus2, pp.get_element_index(net, "trafo", '132/66 kV Transformer'), et="t", type="LBS", closed=True)
#sw3 = pp.create_switch(net, bus6, pp.get_element_index(net, "trafo", '66/33 kV Transformer'), et="t", type="LBS", closed=False)
#sw4 = pp.create_switch(net, bus7, pp.get_element_index(net, "trafo", '66/33 kV Transformer'), et="t", type="LBS", closed=False)


pp.runpp(net, numba=False)

# Filter active lines
active_lines = net.res_line[net.line['in_service'] == True]

# Calculate line current and loading for active lines
print("Line current and loading for active lines (kA, %):")
print(active_lines[['i_ka', 'loading_percent']])

# Real power absorbed or created in each active line
active_line_losses = active_lines['p_from_mw'] + active_lines['p_to_mw']
print("Line Losses for Active Lines (MW):")
print(active_line_losses)

# Total real power absorbed or created in the lines
total_line_power = active_line_losses.sum()
print(f"Total Power Loss in Active Lines: {total_line_power:.4f} MW")

# Reactive power absorbed or created in each active line
active_line_reactive_losses = active_lines['q_from_mvar'] + active_lines['q_to_mvar']
print("Reactive power in Active Lines (MVAR):")
print(active_line_reactive_losses)

import pdb; pdb.set_trace()
# Total reactive power absorbed or created in the lines
total_reactive_power = active_line_reactive_losses.sum()
print(f"Total Reactive Power in Lines: {total_reactive_power:.4f} MVAR")

# Calculate transformer real power losses
if not net.trafo.empty:
    trafo_losses = net.res_trafo['p_hv_mw'] + net.res_trafo['p_lv_mw']
    print("Transformer Losses (MW):")
    print(trafo_losses)


# Total real power system losses
total_losses = active_line_losses.sum() + trafo_losses.sum()
print(f"Total Real Power System Losses: {total_losses:.4f} MW")


print("Bus Voltages:")
print(net.res_bus.vm_pu)

#import pdb; pdb.set_trace()

#print(net.bus) # show bus table
#print(net.ext_grid) #show external grid table
#print(net.trafo) # transformer information


# Create the network plot

ax = pplot.simple_plot(net, show_plot=False)  # Get the axis object, do not show plot yet

# Now, loop through each switch and add a custom marker on the plot
for idx, switch in net.switch.iterrows():
    # Find the bus to which the switch is connected
    bus_idx = switch.bus
    bus_coords = net.bus_geodata.loc[bus_idx]

    # Determine the color based on switch status
    color = 'green' if switch.closed else 'red'
    marker = 'o' if switch.closed else 'x'
    label = 'Closed' if switch.closed else 'Open'

    # Add annotation to the plot with a high zorder to ensure it is on top
    ax.scatter(bus_coords.x, bus_coords.y, color=color, s=300, marker=marker, 
    label=f'Switch {idx} {"Closed" if switch.closed else "Open"}', zorder=5)  # Higher zorder to ensure visibility on top

# Add load markers
for idx, load in net.load.iterrows():
    bus_idx = load.bus
    bus_coords = net.bus_geodata.loc[bus_idx]
    ax.scatter(bus_coords.x, bus_coords.y, color='yellow', s=300, marker='s', label=f'Load at Bus {bus_idx+1}', zorder=4)

# Show plot with legends
#ax.legend()
#plt.show()
