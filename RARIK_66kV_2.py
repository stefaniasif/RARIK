# RARIK_66Kv_2.py
import pandapower as pp
import pandapower.plotting as pplot
import matplotlib.pyplot as plt
import numpy as np
import code


net = pp.create_empty_network()

# Create buses
bus1 = pp.create_bus(net, name="132kv Prestbakki Transformer Bus 1", vn_kv=132, type="b")
bus2 = pp.create_bus(net, name="66kv Prestbakki Transformer Bus 2", vn_kv=66, type="b")

bus3 = pp.create_bus(net, name="Bus 3", vn_kv=66, type="n")
bus4 = pp.create_bus(net, name="Bus 4", vn_kv=66, type="n")
bus5 = pp.create_bus(net, name="Bus 5", vn_kv=66, type="n")

bus6 = pp.create_bus(net, name="66kv Vik Transformer Bus 6", vn_kv=66, type="b")
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
pp.create_ext_grid(net, bus1, vm_pu=1.00, va_degree=0, name= "Aðveitustöð Prestbakka") # Er þetta rétt stillt va og pu?
# pp.create_ext_grid(net, bus7, vm_pu=1.00, va_degree=0, name= "Aðveitustöð Vík í Mýrdal")


# Create transformers

# Define HV transformer parameters
sn_mva = 30         # Rated apparent power in MVA
vn_hv_kv = 132      # High voltage side (primary) rated voltage in kV
vn_lv_kv = 66       # Low voltage side (secondary) rated voltage in kV
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
    name="132/66 kV Transformer"
)

# Define the MV transformer parameters
#sn_mva_2 = 30          # Rated apparent power in MVA
#vn_hv_kv_2 = 66        # High voltage side (primary) rated voltage in kV
#vn_lv_kv_2 = 33        # Low voltage side (secondary) rated voltage in kV
#vk_percent_2 = 10      # Short-circuit voltage (%)
#vkr_percent_2 = 0.5    # Real part of short-circuit impedance (%)
#pfe_kw_2 = 30          # Iron (core) losses in kW, (ca. kw per mva)
#i0_percent_2 = 0.07    # No-load, Magnetizing current (%)
#shift_degree_2 = 0     # Phase shift between HV and LV sides (e.g., delta-star configuration)

# Create the MV transformer
#pp.create_transformer_from_parameters(
#    net, bus6, bus7,
#    sn_mva=sn_mva_2,
#    vn_hv_kv=vn_hv_kv_2,
#    vn_lv_kv=vn_lv_kv_2,
#    vk_percent=vk_percent_2,
#    vkr_percent=vkr_percent_2,
#    pfe_kw=pfe_kw_2,
#    i0_percent=i0_percent_2,
#    shift_degree=shift_degree_2,
#    name="66/33 kV Transformer"
#)


# Create lines

# Define line parameters
loftlina_66_feal300 = {
    'r_ohm_per_km': 0.061,  # resistance in ohm per km
    'x_ohm_per_km': 0.358,   # reactance in ohm per km
    'c_nf_per_km': 10.28,    # capacitance in nF per km
    'max_i_ka': 1.140       # maximum current in kA
}
loftlina_66_Alloy107_D2000 = {  # EKKI NOTUÐ, höfð hér svo ég prófi hana ekki aftur
    'r_ohm_per_km': 0.168,  # resistance in ohm per km
    'x_ohm_per_km': 0.37,   # reactance in ohm per km
    'c_nf_per_km': 9.919,    # capacitance in nF per km
    'max_i_ka': 0.530       # maximum current in kA
}
loftlina_66_Alloy185_D2000 = {  # EKKI NOTUÐ, höfð hér svo ég prófi hana ekki aftur
    'r_ohm_per_km': 0.093,  # resistance in ohm per km
    'x_ohm_per_km': 0.350,   # reactance in ohm per km
    'c_nf_per_km': 10.485,    # capacitance in nF per km
    'max_i_ka': 0.832       # maximum current in kA
}
strengur_66_3x240 = {
    'r_ohm_per_km': 0.125,  # resistance in ohm per km
    'x_ohm_per_km': 0.190,   # reactance in ohm per km
    'c_nf_per_km': 150,    # capacitance in nF per km
    'max_i_ka': 0.465       # maximum current in kA    gildi m.v. samskonar streng, má bara keyra 60%-70% af hitaþolsstraum
}
strengur_66_3x300 = {        # NEI !
    'r_ohm_per_km': 0.100,  # resistance in ohm per km
    'x_ohm_per_km': 0.190,   # reactance in ohm per km
    'c_nf_per_km': 160,    # capacitance in nF per km
    'max_i_ka': 0.495       # maximum current in kA    gildi m.v. samskonar streng, má bara keyra 60%-70% af hitaþolsstraum
}
strengur_66_3x400 = { 
    'r_ohm_per_km': 0.078,  # resistance in ohm per km
    'x_ohm_per_km': 0.180,   # reactance in ohm per km
    'c_nf_per_km': 180,    # capacitance in nF per km
    'max_i_ka': 0.545       # maximum current in kA    gildi m.v. samskonar streng, má bara keyra 60%-70% af hitaþolsstraum
}




Utfaerslur = {
    'Leid_1': {     # þarf ekki spólur miðað við fullt álag en ef álagið minnkar eykst launaflið og þá þarf spólur
        'lines': [  # skilar 2.545 mvar aftur til Landsnets, strengurinn framleiðir 13.170 mvar, 6% spennufall
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=19.925, **strengur_66_3x240  , name="Jarðstrengur 1 - TXSP AL 3X1X240"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=19.925, **strengur_66_3x240  , name="Jarðstrengur 2 - TXSP AL 3X1X240"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=19.925, **strengur_66_3x240  , name="Jarðstrengur 3 - TXSP AL 3X1X240"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=19.925, **strengur_66_3x240  , name="Jarðstrengur 4 - TXSP AL 3X1X240")
        ],
        'shunts':[ # með þessa útjöfnun skilar hún engu launafli til baka niður í 21MW, 9.1%-6% spennufall
            pp.create_shunt(net, bus6, q_mvar=0.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Spóla"),   # mjög dýrt að hafa auka tengivirki bara f.spólu
            pp.create_shunt(net, bus2, q_mvar=0*8.0, p_mw=0, name="Spóla")    # positive for inductive reactive compensation
        ]   # cosphi 0.9 af álaginu, sem er leyfilegt samkv. reglugerð, spóla sem tikkar inn ef álagið minnkar því þá hækkar p.f.
    },      # tan(arccos0.9)×25 MW is 12.11 MVAr. Álagið étur 8.217 mvar.
    'Leid_2': {
        'lines': [ # skilar 1.982 mvar aftur til Landsnets, strengurinn framleiðir 12.586 mvar, 6% spennufall
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=19.1, **strengur_66_3x240  , name="Jarðstrengur 1 - TXSP AL 3X1X240"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=19.1, **strengur_66_3x240  , name="Jarðstrengur 2 - TXSP AL 3X1X240"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=19.1, **strengur_66_3x240  , name="Jarðstrengur 3 - TXSP AL 3X1X240"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=19.1, **strengur_66_3x240  , name="Jarðstrengur 4 - TXSP AL 3X1X240")
        ],
        'shunts':[ # engin útjöfnun
            pp.create_shunt(net, bus6, q_mvar=0.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Spóla"),   # mjög dýrt að hafa auka tengivirki bara f.spólu
            pp.create_shunt(net, bus2, q_mvar=0*17.0, p_mw=0, name="Spóla")   # positive for inductive reactive compensation
        ]   # cosphi 0.9 af álaginu, sem er leyfilegt samkv. reglugerð, spóla sem tikkar inn ef álagið minnkar því þá hækkar p.f.
    },      # tan(arccos0.9)×25 MW is 12.11 MVAr. Álagið étur 8.217 mvar
    'Leid_3': {     # no-load = -12.946 mvar
        'lines': [  # 9.3% spennufall án útjöfnunar, -7.400 mvar launaflsframleiðsla, 3.213 mvar frá Landsneti
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=29.7, **strengur_66_3x240  , name="Jarðstrengur 1 - TXSP AL 3X1X240"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=17.3, **strengur_66_3x240  , name="Jarðstrengur 1 - TXSP AL 3X1X240"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=23.7, **loftlina_66_feal300, name="Loftlína 1 - FEAL300"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=9.0 , **strengur_66_3x240  , name="Jarðstrengur 2 - TXSP AL 3X1X240")
        ],
        'shunts':[
            pp.create_shunt(net, bus6, q_mvar=0.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus2, q_mvar=0*12.0, p_mw=0, name="Spóla")   # positive for inductive reactive compensation
        ]
    },
    'Leid_4': {
        'lines': [  # dregur 8.870 mvar frá Landsneti, 10.1% spennufall
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=29.7, **loftlina_66_feal300, name="Loftlína 1 - FEAL300"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=17.3, **strengur_66_3x400  , name="Jarðstrengur 1 - TXSP AL 3X1X400"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=23.7, **loftlina_66_feal300, name="Loftlína 2 - FEAL300"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=9.0 , **strengur_66_3x400  , name="Jarðstrengur 2 - TXSP AL 3X1X400")
        ],          # spennufallið lækkar úr 12% í 11% við að skipta úr 240kvaðrötum upp í 300kvaðröt.
        'shunts':[
            pp.create_shunt(net, bus6, q_mvar=0.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Spóla"),   # of dýrt að sögn Magga að hafa auka spólur á miðri leið
            pp.create_shunt(net, bus2, q_mvar=0*8.0, p_mw=0, name="Spóla")   # positive for inductive reactive compensation
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

# Create load,  pf = 0.95, q_mvar er þá 8.217 mvar
#pp.create_load(net, bus6, p_mw=25, q_mvar=25 *np.tan(np.arccos(0.95)), name="Vík í Mýrdal load")



# Plotta launafl sem þarf að útjafna á móti raunhluta álags
def plot_reactive_power_vs_active_load(net, bus6, pf=0.95):
    
    arr = np.arange(0, 25.1, 0.5)  # Counts from 0 to 25 in steps of 0.5
    launafl = np.zeros_like(arr)
    cosphi = np.zeros_like(arr)

    for idx, i in enumerate(arr):
        net.load.drop(net.load.index, inplace=True)  # Remove previous loads

        q_mvar = i * np.tan(np.arccos(pf))
        pp.create_load(net, bus6, p_mw=i, q_mvar=q_mvar, name="Vík í Mýrdal load")
        pp.runpp(net)

        launafl[idx] = net.res_bus.loc[0, "q_mvar"]
        if i == 0:
            cosphi[idx] = 0.1  # Avoid division by zero
        else:
            cosphi[idx] = np.cos(np.arctan(launafl[idx]/i))

    min_cosphi = np.min(cosphi)
    print(f"Minnsta gildi cosphi: {min_cosphi:.2f}")

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.plot(arr, launafl, marker='o', linestyle='-', color='blue')
    q_value = net.shunt.loc[net.shunt.bus == bus2, 'q_mvar'].values[0]
    plt.text(arr[0], launafl[0], f"    Spóla: {q_value:.1f} Mvar", fontsize=10)

    mask = cosphi < 0.9
    plt.scatter(arr[mask], launafl[mask], color='red', s=80, label='cos(ϕ) < 0.9')

    plt.title('Launafl sem þarf að útjafna sem fall af raunhluta álags')
    plt.xlabel('Raunaflshluti álags (P_MW)')
    plt.ylabel('Launafl (Q_Mvar)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Plotta launafl sem þarf að útjafna á móti raunhluta álags og finna hentugar spólustærðir
def plot_reactive_power_shunt_sizing(net, bus_load, bus_shunt, pf=0.95):
    plt.figure(figsize=(8, 5))
    arr = np.arange(0, 25.1, 0.5)
    launafl = np.zeros_like(arr)
    cosphi = np.zeros_like(arr)
    last = 0

    for idx, i in enumerate(arr):
        # Create load,  pf = 0.95, q_mvar er þá 8.217 mvar
        net.load.drop(net.load.index, inplace=True) # to prevent stacking loads in each step
        pp.create_load(net, bus_load, p_mw=i, q_mvar=i *np.tan(np.arccos(pf)), name="Vík í Mýrdal load")
        pp.runpp(net)
        launafl[idx] = net.res_bus.loc[0,"q_mvar"]  # finnur launafl sem er dregið frá Landsneti eða sent aftur til baka

        if i == 0:
            cosphi[idx] = 1.0                               # áætlun fyrir 0 MW, ekki hægt að deila með núlli
            rounded_launafl = np.floor(launafl[idx])        # þannig spólan sé heil tala
            net.shunt.drop(net.shunt.index, inplace=True)   # to prevent stacking shunts
            pp.create_shunt(net, bus_shunt, q_mvar=rounded_launafl, p_mw=0, name="Spóla")
            print(f"Spóla sett. Stærð spólu: {rounded_launafl} Mvar. Álag: {i} MW")
            pp.runpp(net)
            launafl[idx] = net.res_bus.loc[0, "q_mvar"]
        else:
            cosphi[idx] = np.cos(np.arctan(launafl[idx] / i))

        v6 = net.res_bus.vm_pu.at[bus6]
        # Track the current shunt
        shunt_idx = net.shunt[net.shunt.bus == bus2].index[0]
        q_shunt = net.shunt.at[shunt_idx, 'q_mvar']
        v6_pre = net.res_bus.vm_pu.at[bus6]     # spenna í Vík áður en spólan tikkar inn
        # Size of shunt at bus 2
        q_value_last = net.shunt.loc[net.shunt.bus == bus2, 'q_mvar'].values[0]
        q_value = net.shunt.loc[net.shunt.bus == bus2, 'q_mvar'].values[0]

        while ((cosphi[idx] < 0.9) or (v6 < 0.9)) and (q_shunt > -20) and (q_value > 0):  # Regla spólu
            if i < 3:           # þarf að vera, annars festist lykkjan í 0.5 MW
                q_shunt -= 0.5  # shed 0.5 Mvar per step
            else:
                q_shunt -= q_value  # tekur spóluna alveg út og tikkar inn í 0.5 Mvar skrefum þangað til spennufall er undir 3.5%
        
            # Minnka gildi á spólu
            net.shunt.at[shunt_idx, 'q_mvar'] = q_shunt

            # new values
            pp.runpp(net)
            launafl[idx] = net.res_bus.loc[0, "q_mvar"]
            cosphi[idx] = np.cos(np.arctan(launafl[idx] / i))
            v6 = net.res_bus.vm_pu.at[bus6]
            spennubreyting = (v6 - v6_pre) * 100

            # passa að spennufall verði ekki meira en 3.5% þegar spólan kemur inn þegar álag minnkar
            while spennubreyting > 3.5:
                q_shunt += 0.5
                net.shunt.at[shunt_idx, 'q_mvar'] = q_shunt
                
                # new values
                pp.runpp(net)
                launafl[idx] = net.res_bus.loc[0, "q_mvar"]
                cosphi[idx] = np.cos(np.arctan(launafl[idx] / i))
                v6 = net.res_bus.vm_pu.at[bus6]
                spennubreyting = (v6 - v6_pre) * 100

            q_value = net.shunt.loc[net.shunt.bus == bus2, 'q_mvar'].values[0]
            plt.plot(arr[last:idx], launafl[last:idx], marker='o', linestyle='-', color='blue')
            plt.text(arr[last], launafl[last], f"  Spóla: {q_value_last:.1f} Mvar (P = {arr[last]} : {i} MW)", fontsize=10)
            last = idx
            print(f"Spólu breytt: {q_value:.1f} Mvar. Álag: {i} MW. Spenna: {v6:.2f} pu. cosφ: {cosphi[idx]:.2f}")

        if i == 25 and last != idx:
            q_value = net.shunt.loc[net.shunt.bus == bus_shunt, 'q_mvar'].values[0]
            plt.plot(arr[last:idx+1], launafl[last:idx+1], marker='o', linestyle='-', color='blue')
            plt.text(arr[last], launafl[last], f"  Spóla: {q_value_last:.1f} Mvar (P = {arr[last]} : {i} MW)", fontsize=10)

    min_cosphi = np.min(cosphi)
    print(f"Minnsta gildi cosφ: {min_cosphi:.2f}")

    # Mark points where cos(phi) < 0.9
    mask = cosphi < 0.9
    plt.scatter(arr[mask], launafl[mask], color='red', s=80)

    plt.title('Launafl sem þarf að útjafna sem fall af raunhluta álags')
    plt.xlabel('Raunaflshluti álags (P_MW)')
    plt.ylabel('Launafl (Q_Mvar)')
    plt.minorticks_on()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


plot_reactive_power_shunt_sizing(net, bus6, bus2, pf=0.95)
#plot_reactive_power_vs_active_load(net, bus6, pf=0.95)

# Create switches
#sw1 = pp.create_switch(net, bus1, pp.get_element_index(net, "trafo", '132/66 kV Transformer'), et="t", type="LBS", closed=True)
#sw2 = pp.create_switch(net, bus2, pp.get_element_index(net, "trafo", '132/66 kV Transformer'), et="t", type="LBS", closed=True)
#sw3 = pp.create_switch(net, bus6, pp.get_element_index(net, "trafo", '66/33 kV Transformer'), et="t", type="LBS", closed=False)
#sw4 = pp.create_switch(net, bus7, pp.get_element_index(net, "trafo", '66/33 kV Transformer'), et="t", type="LBS", closed=False)


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

print("Fletta upp til að sjá spólustærðir")

#launafl = net.res_bus.loc[0,"q_mvar"]
#print(f"Launafl skilað aftur til Landsnets(jákvæð stærð): {launafl:.4f}")

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

# Start interactive session to explore values in system
# net.res_bus.loc[0,"q_mvar"] finnur launafl sem er skilað (jákvætt) aftur til Landsnets 
# net.res_trafo['q_hv_mvar'] + net.res_trafo['q_lv_mvar'] finnur launafl sem spennir tekur
#code.interact(local=locals())
