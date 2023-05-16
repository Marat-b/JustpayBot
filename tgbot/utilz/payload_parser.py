def payload_parser(payload: str):
    words = payload.split('_')
    if len(words) == 3:
        customer_id = words[0]
        if words[1] == 'participant':
            return {"customer_id":words[0], "participant_id":words[2]}
        else:
            return {}

    return None