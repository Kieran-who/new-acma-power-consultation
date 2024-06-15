import weaviate
from .classes import weav_classes
import copy

weav_classes_to_check = copy.deepcopy(weav_classes)

def add_prop(client, class_name, prop):
    class_val = client.collections.get(class_name)
    class_val.config.add_property(prop)    

def check_properties(client):
    classes = client.collections.list_all(simple=True)
    class_properties = {}    
    for config in classes.values():
        # Extract the class name
        class_name = config.name
        
        # Extract the property names
        property_names = [prop.name for prop in config.properties]
        
        # Store the class name and its property names in the dictionary
        class_properties[class_name] = property_names
    
    for class_obj in weav_classes_to_check["classes"]:
        class_name = class_obj["class"]
        for prop in class_obj["properties"]:            
            prop_name = prop.name            
            if class_name in class_properties:
                if prop_name not in class_properties[class_name]:
                    print(f'Adding property "{prop_name}" to class "{class_name}"')
                    add_prop(client, class_name, prop)                
            else:
                print(f'Class "{class_name}" not found in class_properties')
    

def setup_classes(client):    
    try:
        classes = client.collections.list_all(simple=True)                
        test_classes = [config.name for config in classes.values()]
        # This creates newly defined classes that are not currently setup in DB
        for class_obj in weav_classes_to_check["classes"]:            
            class_name = class_obj["class"]            
            if not any(existing_class_name == class_name for existing_class_name in test_classes):
                try:
                    print(f"Creating class: {class_name}")
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
        check_properties(client)
        return
    except Exception as e:
        print("Error setting up classes")
        print(e)

def client_start():
    client = weaviate.connect_to_embedded()
    
    client.connect()
    # Creates the schema if it doesn't exist
    setup_classes(client)
    return client

def weav_setup():
    client = client_start()
    return client