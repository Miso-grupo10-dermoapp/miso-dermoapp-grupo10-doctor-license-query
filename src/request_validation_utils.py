import json



def validate_property_exist(property, loaded_body):
    if property in loaded_body:
        if loaded_body[property] is not None:
            return True
        else:
            return False
    else:
        return False
