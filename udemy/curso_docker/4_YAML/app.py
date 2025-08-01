import yaml

if __name__ == '__main__':
    stream = open("test.yaml", 'r')
    dictionary = yaml.safe_load(stream)
    
    if dictionary is None:
        print("YAML vazio")
    else:
        for key, value in dictionary.items():
            print(f'{key}: {str(value)}')