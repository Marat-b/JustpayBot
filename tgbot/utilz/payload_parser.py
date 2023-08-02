def payload_parser(payload: str):
    # payload = payload.split('_')
    # if len(payload) == 3:
    #     customer_id = payload[0]
    if payload[0] == 'p': # articipant
        print(f'participant_number={payload[1:]}')
        return {"client_id":'', "participant_number":payload[1:]} # only "participant_number is used
    elif payload[0] == 'c':
        return {"customer_id":payload[1:], "customer_number": 0}
    else:
        return {}

    # return None