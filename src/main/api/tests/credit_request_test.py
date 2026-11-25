import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.credit_request import CreditRequest
from src.main.api.utils.helpers import generate_credit_amount, calculate_balance_after_credit_request


class TestCreditRequest:
    @pytest.mark.parametrize(
        "term_months",
        [12]
    )

    def test_credit_request(self,
                            db_session: Session,
                            api_manager: ApiManager,
                            create_credit_user_request: CreateCreditUserRequest,
                            created_credit_account: CreateAccountResponse,
                            term_months: int):

        initial_balance = created_credit_account.balance

        assert initial_balance == 0

        credit_amount = generate_credit_amount()

        credit_request = CreditRequest(
            accountId=created_credit_account.id,
            amount=credit_amount,
            termMonths=term_months
        )

        credit_response = api_manager.user_steps.credit_request(
            create_credit_user_request,
            credit_request
        )

        account_from_db = Account.get_account_by_id(
            db_session,
            created_credit_account.id
        )

        account_balance_after_credit_request = calculate_balance_after_credit_request(
            initial_balance,
            credit_amount
        )

        assert account_from_db is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db.balance == account_balance_after_credit_request, 'Некорректный баланс аккаунта после получения кредита'


    @pytest.mark.parametrize(
        "term_months", [12]
    )

    def test_repeated_credit_request(self,
                            db_session: Session,
                            api_manager: ApiManager,
                            create_credit_user_request: CreateCreditUserRequest,
                            created_credit_account: CreateAccountResponse,
                            term_months: int):

        initial_balance = created_credit_account.balance

        assert initial_balance == 0

        credit_amount = generate_credit_amount()

        credit_request = CreditRequest(
            accountId=created_credit_account.id,
            amount=credit_amount,
            termMonths=term_months
        )

        credit_response = api_manager.user_steps.credit_request(
            create_credit_user_request,
            credit_request
        )

        account_from_db = Account.get_account_by_id(
            db_session,
            created_credit_account.id
        )

        account_balance_after_credit_request = calculate_balance_after_credit_request(
            initial_balance,
            credit_amount
        )

        assert account_from_db is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db.balance == account_balance_after_credit_request, 'Некорректный баланс аккаунта после получения кредита'


        repeated_credit_request = CreditRequest(
            accountId=created_credit_account.id,
            amount=credit_amount, termMonths=term_months
        )

        repeated_credit_response = api_manager.user_steps.repeated_credit_request(
            create_credit_user_request,
            repeated_credit_request
        )

        db_session.expire_all()

        account_from_db_after_repeated_credit_request = Account.get_account_by_id(
            db_session,
            created_credit_account.id)

        assert account_from_db_after_repeated_credit_request is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db_after_repeated_credit_request.balance == account_balance_after_credit_request, 'Баланс счёта изменился после повторного запроса кредита'

