from appliance.appliances_reader import create_appliances

appliances = create_appliances()


for a in appliances:
    print(a)
