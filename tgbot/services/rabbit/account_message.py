from datetime import datetime, timezone


def account_message(account_dict) -> str:
    text = "Счёт:\t{}\nНазвание счёта:\t{}\nОписание счёта:\t{}\nСумма на счёте\t{}\nСчёт создан\t{}".format(
        account_dict["account"],account_dict["campaign_name"],account_dict["campaign_description"],account_dict["amount"],
        account_dict["campaign_create_date"]
    )
    return text