import vcr
import json


def replace_nested_dict_values(input_dict, key_to_replace, new_value):
    if isinstance(input_dict, dict):
        for key, value in input_dict.items():
            if key == key_to_replace:
                input_dict[key] = new_value
            elif isinstance(value, (dict, list)):
                replace_nested_dict_values(value, key_to_replace, new_value)
    elif isinstance(input_dict, list):
        for item in input_dict:
            replace_nested_dict_values(item, key_to_replace, new_value)
    return input_dict


def scrub_strings():
    KEYS_TO_SCRUB = ['numero', 'cnpj', 'ip', 'contrato',
                     'logradouro', 'cep', 'cidade', 'token']

    def before_record_response(response):
        data = json.loads(response['body']['string'])
        for k in KEYS_TO_SCRUB:
            data = replace_nested_dict_values(data, k, '***')

        response['body']['string'] = json.dumps(data).encode('utf-8')
        return response
    return before_record_response


trackr_vcr = vcr.VCR(
    cassette_library_dir='tests/recorded',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    filter_headers=['authorization'],
    filter_post_data_parameters=['numero'],
    before_record_response=scrub_strings(),

)
