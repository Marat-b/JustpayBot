def payload_parser(payload: str):
    words = payload.split('_')
    if len(words) == 3:
        customer_id = words[0]
        if words[1] == 'p': # articipant
            print(f'participant_number={words[2]}')
            return {"client_id":words[0], "participant_number":words[2]}
        elif words[1] == 'customer':
            return {"client_id":words[0], "customer_number":words[2]}
        else:
            return {}

    return None