from tgbot.services.db.client_service import ClientDbService
from tgbot.services.db.user_service import UserDbService
from tgbot.utilz.payload_parser import payload_parser


def create_user(chat_id: int, text: str):
    user = payload_parser(text)
    print(f'user={user}')
    if 'participant_number' in user:
        print('Has attribute participant_number')
        user_service = UserDbService()
        user_service.create(user['client_id'], user['participant_number'], chat_id)
    if 'customer_number' in user:
        client_service = ClientDbService()
        client_service.create(user['client_id'], user['customer_number'], chat_id)