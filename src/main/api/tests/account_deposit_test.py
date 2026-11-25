import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.utils.helpers import generate_deposit_amount, calculate_balance_after_deposit


@pytest.mark.api
class TestAccountDeposit:
    def test_account_deposit(self, db_session: Session,
                             api_manager: ApiManager,
                             create_user_request: CreateUserRequest,
                             created_account: CreateAccountResponse):

        assert created_account.balance == 0

        deposit_amount = generate_deposit_amount()

        account_deposit_request = AccountDepositRequest(
            accountId=created_account.id,
            amount=deposit_amount
        )
        account_deposit_response = api_manager.user_steps.account_deposit(
            create_user_request,
            account_deposit_request
        )

        account_from_db = Account.get_account_by_id(
            db_session,
            account_deposit_response.id
        )

        account_balance_after_deposit = calculate_balance_after_deposit(created_account.balance, deposit_amount)

        assert account_from_db is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db.balance == account_balance_after_deposit, 'Некорректный баланс аккаунта после пополнения'



    @pytest.mark.parametrize(
        "amount",
        [-1000],
    )

    def test_account_deposit_invalid(self, db_session: Session,
                             api_manager: ApiManager,
                             create_user_request: CreateUserRequest,
                             created_account: CreateAccountResponse,
                             amount: float):


        assert created_account.balance == 0


        account_deposit_request = AccountDepositRequest(
            accountId=created_account.id,
            amount=amount
        )
        account_deposit_response = api_manager.user_steps.account_deposit_invalid(
            create_user_request,
            account_deposit_request
        )

        account_from_db = Account.get_account_by_id(
            db_session,
            created_account.id
        )


        assert account_from_db is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db.balance == created_account.balance, 'Баланс изменился после неуспешного пополнения'




