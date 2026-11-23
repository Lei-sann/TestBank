import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.credit_request import CreditRequest





class TestCreditRequest:
    @pytest.mark.parametrize(
        "credit_amount, term_months",
        [
            (10000, 12)
        ]
    )

    def test_credit_request(self,
                            db_session: Session,
                            api_manager: ApiManager,
                            create_credit_user_request: CreateCreditUserRequest,
                            created_credit_account: CreateAccountResponse,
                            credit_amount: float,
                            term_months: int):

        initial_balance = created_credit_account.balance

        assert initial_balance == 0

        account_id = created_credit_account.id

        credit_request = CreditRequest(accountId=account_id, amount=credit_amount, termMonths=term_months)
        credit_response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

        account_from_db = Account.get_account_by_id(db_session, account_id)

        assert account_from_db is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db.balance == initial_balance + credit_amount, 'Поле баланса для созданного аккаунта отсутствует в БД'


    @pytest.mark.parametrize(
        "credit_amount, term_months",
        [
            (10000, 12)
        ]
    )

    def test_repeated_credit_request(self,
                            db_session: Session,
                            api_manager: ApiManager,
                            create_credit_user_request: CreateCreditUserRequest,
                            created_credit_account: CreateAccountResponse,
                            credit_amount: float,
                            term_months: int):

        initial_balance = created_credit_account.balance

        assert initial_balance == 0

        account_id = created_credit_account.id

        credit_request = CreditRequest(accountId=account_id, amount=credit_amount, termMonths=term_months)
        credit_response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

        account_from_db = Account.get_account_by_id(db_session, account_id)

        assert account_from_db is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db.balance == initial_balance + credit_amount, 'Поле баланса для созданного аккаунта отсутствует в БД'



        repeated_credit_request = CreditRequest(accountId=account_id, amount=credit_amount, termMonths=term_months)
        repeated_credit_response = api_manager.user_steps.repeated_credit_request(create_credit_user_request, repeated_credit_request)

        db_session.expire_all()

        account_from_db_after_repeated_credit_request = Account.get_account_by_id(db_session, account_id)

        assert account_from_db_after_repeated_credit_request is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db_after_repeated_credit_request.balance == account_from_db.balance, 'Баланс счёта изменился после повторного запроса кредита'

