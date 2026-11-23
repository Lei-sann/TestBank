import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest




class TestCreditRepay:
        @pytest.mark.parametrize(
            "credit_amount, term_months",
            [
                (10000, 12)
            ]
        )
        def test_credit_repay_request(self,
                                db_session: Session,
                                api_manager: ApiManager,
                                create_credit_user_request: CreateCreditUserRequest,
                                created_credit_account: CreateAccountResponse,
                                credit_amount: float,
                                term_months: int):
            initial_balance = created_credit_account.balance

            assert initial_balance == 0

            account_id = created_credit_account.id

            credit_request = CreditRequest(
                accountId=account_id,
                amount=credit_amount,
                termMonths=term_months
            )

            credit_response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

            account_from_db = Account.get_account_by_id(db_session, account_id)

            assert account_from_db is not None, 'Аккаунт отсутствует в БД'
            assert account_from_db.balance == initial_balance + credit_amount, 'Поле баланса для созданного аккаунта отсутствует в БД'

            balance_after_credit = account_from_db.balance
            credit_id = credit_response.creditId

            credit_repay_request = CreditRepayRequest(
                creditId=credit_id,
                accountId=account_id,
                amount=credit_amount
            )

            credit_repay_response = api_manager.user_steps.credit_repay(create_credit_user_request, credit_repay_request)

            db_session.expire_all()

            account_from_db_after_credit_repay = Account.get_account_by_id(db_session, account_id)

            assert account_from_db_after_credit_repay is not None,  'Аккаунт отсутствует в БД'
            assert account_from_db_after_credit_repay.balance == balance_after_credit - credit_amount, 'Поле баланса для аккаунта отсутствует в БД'
            assert credit_repay_response.amountDeposited == credit_amount




        @pytest.mark.parametrize(
            "credit_amount, term_months",
            [
                (10000, 12)
            ]
        )
        def test_partial_credit_repay(self,
                                db_session: Session,
                                api_manager: ApiManager,
                                create_credit_user_request: CreateCreditUserRequest,
                                created_credit_account: CreateAccountResponse,
                                credit_amount: float,
                                term_months: int):
            initial_balance = created_credit_account.balance

            assert initial_balance == 0

            account_id = created_credit_account.id

            credit_request = CreditRequest(
                accountId=account_id,
                amount=credit_amount,
                termMonths=term_months
            )

            credit_response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

            account_from_db = Account.get_account_by_id(db_session, account_id)

            assert account_from_db is not None, 'Аккаунт отсутствует в БД'
            assert account_from_db.balance == initial_balance + credit_amount, 'Поле баланса для созданного аккаунта отсутствует в БД'

            balance_after_credit = account_from_db.balance
            credit_id = credit_response.creditId

            partial_amount = credit_amount / 2

            partial_credit_repay_request = CreditRepayRequest(
                creditId=credit_id,
                accountId=account_id,
                amount=partial_amount
            )

            api_manager.user_steps.partial_credit_repay(create_credit_user_request, partial_credit_repay_request)

            db_session.expire_all()

            account_from_db_after_credit_repay = Account.get_account_by_id(db_session, account_id)

            assert account_from_db_after_credit_repay is not None,  'Аккаунт отсутствует в БД'
            assert account_from_db_after_credit_repay.balance == balance_after_credit, 'Поле баланса для аккаунта отсутствует в БД'





