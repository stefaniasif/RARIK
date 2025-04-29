# RARIK_33Kv_2.py
import pandapower as pp
import pandapower.plotting as pplot
import matplotlib.pyplot as plt
import numpy as np
import code


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
    'r_ohm_per_km': 0.061,     # resistance in ohm per km
    'x_ohm_per_km': 0.358,     # reactance in ohm per km
    'c_nf_per_km': 10.28,      # capacitance in nF per km
    'max_i_ka': 1.140          # maximum current in kA
}
strengur_33_TXSP_AL_3x1x800 = {
    'r_ohm_per_km': 0.037,    # resistance in ohm per km
    'x_ohm_per_km': 0.16,     # reactance in ohm per km
    'c_nf_per_km': 350,       # capacitance in nF per km
    'max_i_ka': 0.780         # maximum current in kA    gildi m.v. samskonar streng, má bara keyra 60%-70% af hitaþolsstraum
}
strengur_36_AXAL_1x3x300 = {     # ÞRÍLEIÐARI
    'r_ohm_per_km': 0.1,      # resistance in ohm per km
    'x_ohm_per_km': 0.18,     # reactance in ohm per km
    'c_nf_per_km': 230,       # capacitance in nF per km
    'max_i_ka': 0.500         # maximum current in kA    gildi m.v. samskonar streng, má bara keyra 60%-70% af hitaþolsstraum
}
strengur_33_TXSP_AL_3x1x1000 = {
    'r_ohm_per_km' : 0.029,   # resistance in ohm per km
    'x_ohm_per_km' : 0.15,    # reactance in ohm per km
    'c_nf_per_km' : 390,      # capacitance in nF per km
    'max_i_ka' : 0.850        # maximum current in kA    gildi m.v. samskonar streng, má bara keyra 60%-70% af hitaþolsstraum
}



Utfaerslur = {
    'Leid_1': { # 1, jarðstrengur í sömu lengd og núverandi tenging, 79.7 km, keyrður á 61% af hitaþolsstraum
        'lines': [  # no-load =  -10.596 Mvar, full-load = 6.423 mvar, eins og rýmdin aukist hraðar en spanið þegar strengurinn lengist
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=19.925, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 1 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=19.925, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 2 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=19.925, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 3 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=19.925, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 4 - 3x1x800")
        ],      # ÞOLIR 16.5 mw p.f. 0.95 án þess að spennufall fari niður í 10% (9.5%), 17MW eru 10.4% spennufall
        'shunts':[ # lágmarks-útjöfnun til að ná samleitni, 10.436 mvar dregin frá Landsneti, 26 % spennufall
            pp.create_shunt(net, bus6, q_mvar= 0.0, p_mw=0, name="Spóla"),   # -3.0 til að ná samleitni m.25MW, negative for capacitive reactive compensation
            pp.create_shunt(net, bus4, q_mvar= 0.0, p_mw=0, name="Shunt"),   # of dýrt að sögn Magga að hafa auka spólur á miðri leið
            pp.create_shunt(net, bus2, q_mvar= 0*1.0, p_mw=0, name="Spóla")   # -6.0 til að ná samleitni m.25MW, positive for inductive reactive compensation
        ]   # spólur settar þannig að 2/3 sé í stöð, 1/3 í aðveitustöð Vík
    },
    'Leid_2': { #2,  jarðstrengur sem fylgir þjóðveginum, 76.4km, keyrður á 61% af hitaþolsstraum
        'lines': [  # no-load = -10.095 mvar,  full-load = 9.024 mvar
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=19.1, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 1 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=19.1, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 2 - 3X1X800"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=19.1, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 3 - 3X1X800"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=19.1, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 4 - 3X1X800")
        ],      # ÞOLIR 16.5 mw p.f. 0.95 án þess að spennufall fari niður í 10% (9.2%), 17MW eru 10.1% spennufall
        'shunts':[ # lágmarks-útjöfnun til að ná samleitni, 17.383 mvar dregin frá Landsneti, 31% spennufall
            pp.create_shunt(net, bus6, q_mvar=0*-2.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Spóla"),   # mjög dýrt að hafa auka tengivirki bara f.spólu
            pp.create_shunt(net, bus2, q_mvar=0*-3.0, p_mw=0, name="Spóla")
        ]   
    },      
    'Leid_3': {     # Þessi tenging án útjöfnunar þolir 11.5 MW p.f. 0.95 með spennufall 9.5%
        'lines': [  # no-load = -7.255 mvar, full-load = 7.184 mvar, 17% spennufall, keyrður á 62% af hitaþolsstraum
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=29.7, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 1 - 3X1X800"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=17.3, **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 2 - 3X1X800"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=23.7, **loftlina_66_feal300, name="Loftlína 1 - 66_feal300"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=9.0 , **strengur_33_TXSP_AL_3x1x800  , name="Jarðstrengur 3 - 3X1X800")
        ],
        'shunts':[ # lágmarks útjöfnun til að ná samleitni
            pp.create_shunt(net, bus6, q_mvar=0.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus2, q_mvar=0*8.0, p_mw=0, name="Spóla")   # positive for inductive reactive compensation
        ]
    },
    'Leid_4': {     # TVÆR ÞRÍLEIÐARATENGINGAR      þolir 20 MW, 9.9% spennufall, dregur 0.33mvar frá Landsneti, þarf spólu ef álag minnkar
        'lines': [  # no-load = -13.406 mvar, full-load = -3.995 mvar, 17.4% spennufall, dregur 7.077 mvar frá Landsneti
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
            pp.create_shunt(net, bus6, q_mvar=0.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0.0, p_mw=0, name="Spóla"),   # positive for inductive reactive compensation
            pp.create_shunt(net, bus2, q_mvar=0*2.0, p_mw=0, name="Spóla")   # positive for inductive reactive compensation
        ]   # spólurnar minnka launafl en auka spennufall
    },
    'Leid_5': {     # þessi tenging þolir 9 MW, 9.5% spennufall, dregur 2.46mvar frá Landsneti
        'lines': [  # no-load = -3.563 mvar, full-load = 10.658 mvar, útaf loftlínum, skilar 17.2 mvar til Landsnets, þetta er weird case
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=29.7, **loftlina_66_feal300, name="Loftlína 1 - FEAL 1x300"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=17.3, **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 1 - 3x1x800"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=23.7, **loftlina_66_feal300, name="Loftlína 2 - FEAL 1x300"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=9.0 , **strengur_33_TXSP_AL_3x1x800, name="Jarðstrengur 2 - 3x1x800")
        ],
        'shunts':[ # minnstu gildi á þéttum til að ná samleitni
            pp.create_shunt(net, bus6, q_mvar=0, p_mw=0, name="Þéttir"),   # negative for capacitive reactive compensation
            pp.create_shunt(net, bus4, q_mvar=0, p_mw=0, name="Þéttir"),
            pp.create_shunt(net, bus2, q_mvar=0*4, p_mw=0, name="Þéttir")   # positive for inductive reactive compensation
        ]   # þegar ég eyk stærð á þéttum þá lækkar spennan í Vík?
    },
    'Leid_6': { # 1, Sama og Leid 1, nema annar strengur, þolir 18.5 MW load (pf 0.95), 9.5% spennufall, dregur 2.22 mvar frá Landsneti
        'lines': [  # no-load =  -11.922 Mvar, full-load = 6.906 mvar, spennufall 30%
            pp.create_line_from_parameters(net, from_bus=bus2, to_bus=bus3, length_km=19.925, **strengur_33_TXSP_AL_3x1x1000, name="Jarðstrengur 1 - 3x1x1000"),
            pp.create_line_from_parameters(net, from_bus=bus3, to_bus=bus4, length_km=19.925, **strengur_33_TXSP_AL_3x1x1000, name="Jarðstrengur 2 - 3x1x1000"),
            pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=19.925, **strengur_33_TXSP_AL_3x1x1000, name="Jarðstrengur 3 - 3x1x1000"),
            pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus6, length_km=19.925, **strengur_33_TXSP_AL_3x1x1000, name="Jarðstrengur 4 - 3x1x1000")
        ],      
        'shunts':[ # náði samleitni með engri útjöfnun
            pp.create_shunt(net, bus6, q_mvar= 0.0, p_mw=0, name="Þéttir"),   # negative for capacitive reactive compensation
            pp.create_shunt(net, bus4, q_mvar= 0.0, p_mw=0, name="Shunt"),   # of dýrt að sögn Magga að hafa auka spólur á miðri leið
            pp.create_shunt(net, bus2, q_mvar= 0.0, p_mw=0, name="Þéttir")   # positive for inductive reactive compensation
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
activate_leid('Leid_6', activate=False)  # Activate leid_5 (both lines and shunts)


# til að keyra forritið án þess að fara í föllin til að plotta
# Create load,  pf = 0.95, q_mvar er þá 8.217 mvar
#pp.create_load(net, bus6, p_mw=19, q_mvar=19 *np.tan(np.arccos(0.95)), name="Vík í Mýrdal load")
#pp.runpp(net)


# Plotta launafl sem þarf að útjafna á móti raunhluta álags
def plot_reactive_power_vs_active_load(net, bus6, pf=0.95, hamark= 17):
    
    arr = np.arange(0, hamark + 0.1, 0.5)  # Counts from 0 to 25 in steps of 0.5
    launafl = np.zeros_like(arr)
    cosphi = np.zeros_like(arr)

    for idx, i in enumerate(arr):
        net.load.drop(net.load.index, inplace=True)  # Remove previous loads

        q_mvar = i * np.tan(np.arccos(pf))
        pp.create_load(net, bus6, p_mw=i, q_mvar= q_mvar, name="Vík í Mýrdal load")
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
    q_value = net.shunt.loc[(net.shunt.bus == bus2) & (net.shunt.in_service), 'q_mvar'].values[0]
    plt.text(arr[0], launafl[0], f"      Spóla: {q_value:.1f} Mvar", fontsize=10)
    
    mask = cosphi < 0.9
    plt.scatter(arr[mask], launafl[mask], color='red', s=80, label='cos(ϕ) < 0.9')

    plt.title('Launafl sem þarf að útjafna sem fall af raunhluta álags, án útjöfnunar')
    plt.xlabel('Raunaflshluti álags (P_MW)')
    plt.ylabel('Launafl (Q_Mvar)')
    plt.legend()
    plt.minorticks_on()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()




# Plotta launafl sem þarf að útjafna á móti raunhluta álags og finna hentugar spólustærðir
def plot_reactive_power_shunt_sizing(net, bus_load, bus_shunt, pf=0.95, hamark = 17):
    plt.figure(figsize=(8, 5))
    arr = np.arange(0, hamark + 0.1, 0.5)
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
            rounded_launafl = np.floor(launafl[idx])    # þannig spólan sé heil tala
            net.shunt.drop(net.shunt.index, inplace=True)   # to prevent stacking shunts
            pp.create_shunt(net, bus_shunt, q_mvar=rounded_launafl, p_mw=0, name="Spóla")
            print(f"Spóla sett. Stærð spólu: {rounded_launafl} Mvar. Álag: {i} MW")
            pp.runpp(net)
            launafl[idx] = net.res_bus.loc[0, "q_mvar"]
        elif i == (hamark+2):       # til neyða fallið til að droppa spólunni í endann, hamark - staðsetning
            q_shunt -= q_value
            # Minnka gildi á spólu
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
            print(f"Spólu breytt: {q_value:.1f} Mvar. Álag: {i} MW. Spenna: {v6:.2f} pu. cosφ: {cosphi[idx]:.2f}. Spennubreyting: {spennubreyting:.1f} %")
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
            while (spennubreyting > 3.5 or cosphi[idx] < 0.9 or (v6 < 0.9)) and (q_shunt > -20) and (q_value > 0):
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
            plt.text(arr[last], launafl[last], f"  Spóla: {q_value_last:.1f} Mvar\n (P = {arr[last]} : {i} MW)", fontsize=10)
            last = idx
            print(f"Spólu breytt: {q_value:.1f} Mvar. Álag: {i} MW. Spenna: {v6:.2f} pu. cosφ: {cosphi[idx]:.2f}. Spennubreyting: {spennubreyting:.1f} %")

        if i == hamark and last != idx:
            q_value = net.shunt.loc[net.shunt.bus == bus_shunt, 'q_mvar'].values[0]
            plt.plot(arr[last:idx+1], launafl[last:idx+1], marker='o', linestyle='-', color='blue')
            plt.text(arr[last], launafl[last], f"  Spóla: {q_value_last:.1f} Mvar\n (P = {arr[last]} : {i} MW)", fontsize=10)

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



#plot_reactive_power_vs_active_load(net, bus6, pf=0.95)
plot_reactive_power_shunt_sizing(net, bus6, bus2, pf=0.95)


# Create switches
#sw1 = pp.create_switch(net, bus1, pp.get_element_index(net, "trafo", '132/66 kV Transformer'), et="t", type="LBS", closed=True)
#sw2 = pp.create_switch(net, bus2, pp.get_element_index(net, "trafo", '132/66 kV Transformer'), et="t", type="LBS", closed=True)
#sw3 = pp.create_switch(net, bus6, pp.get_element_index(net, "trafo", '66/33 kV Transformer'), et="t", type="LBS", closed=False)


# Filter active lines
active_lines = net.res_line[net.line['in_service'] == True]

# Calculate line current and loading for active lines
print("Line current and loading for active lines (kA, %):")
formatted = active_lines[['i_ka', 'loading_percent']].copy()
formatted['i_ka'] = formatted['i_ka'].round(2)
formatted['loading_percent'] = formatted['loading_percent'].round(0).astype(int).astype(str) + '%'
print(formatted)

# Real power absorbed or created in each active line
active_line_losses = active_lines['p_from_mw'] + active_lines['p_to_mw']
#print("Line Losses for Active Lines (MW):")
#print(active_line_losses)

# Total real power absorbed or created in the lines
total_line_power = active_line_losses.sum()
print(f"Total Power Loss in Active Lines: {total_line_power:.2f} MW")

# Reactive power absorbed or created in each active line
active_line_reactive_losses = active_lines['q_from_mvar'] + active_lines['q_to_mvar']
#print("Reactive power in Active Lines (MVAR):")
#print(active_line_reactive_losses)

# Total reactive power absorbed or created in the lines
total_reactive_power = active_line_reactive_losses.sum()
print(f"Total Reactive Power in Lines: {total_reactive_power:.2f} MVAR")

# Calculate transformer real power losses
if not net.trafo.empty:
    trafo_losses = net.res_trafo['p_hv_mw'] + net.res_trafo['p_lv_mw']
    print("Transformer Losses (MW):")
    print(trafo_losses.round(2))


# Total real power system losses
total_losses = active_line_losses.sum() + trafo_losses.sum()
print(f"Total Real Power System Losses: {total_losses:.2f} MW")


print("Bus Voltages:")
print(net.res_bus.vm_pu.round(3))


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
# net.res_trafo['q_hv_mvar'] + net.res_trafo['q_lv_mvar'] finnur launafl sem spennir tekur
#code.interact(local=locals())
