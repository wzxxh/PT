import PT_Visit_Sign,analysis_config


if __name__ == '__main__':
    my_config_dict = analysis_config.read_config()
    PT_Visit_Sign.visit_and_signin_all_websites(my_config_dict)
