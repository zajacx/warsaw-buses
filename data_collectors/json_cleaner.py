def clean_dict(dict_to_clean):
    new_dict = dict()
    for i in dict_to_clean["values"]:
        new_dict[i["key"]] = i["value"]
    return new_dict
