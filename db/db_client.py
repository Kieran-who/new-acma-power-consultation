import weaviate
from .classes import weav_classes
import copy

weav_classes_to_check = copy.deepcopy(weav_classes)

def add_prop(client, class_name, prop):
    class_val = client.collections.get(class_name)
    class_val.config.add_property(prop)    

def check_properties(client):
    weav_classes_test = weav_classes["classes"]
    classes = client.collections.list_all(simple=False)
    test_classes = classes.get('classes', [])
    # Create dictionaries for weav_classes and test_classes
    weav_dict = {
        weav_class['class']: {
            prop['name']: prop for prop in weav_class.get('properties', [])
        } for weav_class in weav_classes_test
    }
    test_dict = {
        test_class['class']: set(prop['name'] for prop in test_class.get('properties', [])) for test_class in test_classes
    }
    for weav_class, weav_props in weav_dict.items():
        for weav_prop_name, weav_prop in weav_props.items():
            if weav_class not in test_dict or weav_prop_name not in test_dict[weav_class]:
                add_prop(client, weav_class, weav_prop)

def setup_classes(client):    
    try:
        classes = client.collections.list_all(simple=True)    
        test_classes = classes        
        for class_obj in weav_classes_to_check["classes"]:
            class_name = class_obj["class"]
            if not any(obj["class"] == class_name for obj in test_classes):
                try:
                    client.collections.create(
                        name=class_name,
                        description=class_obj['description'],
                        vectorizer_config=class_obj["vectorizer_config"],                                               
                        properties=class_obj["properties"]
                    )
                except Exception as e:
                    print("Error creating class")
                    print(e)
        # ensures all schema properties are up to date
        # await check_properties(client)
        return
    except Exception as e:
        print("Error setting up classes")
        print(e)

def client_start():
    client = weaviate.connect_to_embedded(persistence_data_path = './db/data')                
    
    client.connect()
    # Creates the schema if it doesn't exist
    setup_classes(client)
    return client

def weav_setup():
    client = client_start()
    return client