import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account

@pytest.mark.api
class TestAccountDeposit:
    @pytest.mark.parametrize(
        "deposit_amount",
        [1000],
    )

    def test_account_deposit(self, db_session: Session,
                             api_manager: ApiManager,
                             create_user_request: CreateUserRequest,
                             created_account: CreateAccountResponse,
                             deposit_amount):

        initial_balance = created_account.balance

        assert initial_balance == 0

        account_id = created_account.id

        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=deposit_amount)
        account_deposit_response = api_manager.user_steps.account_deposit(create_user_request, account_deposit_request)

        account_from_db = Account.get_account_by_id(db_session, account_deposit_response.id)

        assert account_from_db is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db.balance == initial_balance + deposit_amount, 'Поле баланса для созданного аккаунта отсутствует в БД'



    @pytest.mark.parametrize(
        "amount",
        [-1000],
    )

    def test_account_deposit_invalid(self, db_session: Session,
                             api_manager: ApiManager,
                             create_user_request: CreateUserRequest,
                             created_account: CreateAccountResponse,
                             amount: float):

        initial_balance = created_account.balance

        assert initial_balance == 0

        account_id = created_account.id

        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=amount)
        account_deposit_response = api_manager.user_steps.account_deposit_invalid(create_user_request, account_deposit_request)

        account_from_db = Account.get_account_by_id(db_session, account_id)


        assert account_from_db is not None, 'Аккаунт отсутствует в БД'
        assert account_from_db.balance == initial_balance, 'Поле баланса для созданного аккаунта отсутствует в БД'




