import os


def change_config_variable(var_name:str, value):
    path_to_config = os.path.join(os.path.dirname(__file__), 'config.py')
    with open(path_to_config, 'r', encoding='utf-8') as config_file:
        lines = config_file.read().split('\n')
    with open(path_to_config, 'w', encoding='utf-8') as config_file:
        new_text = ''
        for line in lines:
            if var_name in line:
                new_text += f'{var_name} = {value}\n' #xss there
                continue
            new_text += line
            new_text += '\n' if line != lines[-1] else ''
        config_file.write(new_text)
