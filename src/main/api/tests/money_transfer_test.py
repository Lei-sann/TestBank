import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.money_transfer_request import MoneyTransferRequest
from src.main.api.utils.helpers import generate_deposit_amount, calculate_balance_after_deposit, \
    generate_transfer_amount, calculate_account_1_balance_after_transfer, \
    calculate_account_2_balance_after_transfer, generate_deposit_amount_for_insufficient_funds_transfer, \
    generate_transfer_amount_exceeding_balance


class TestMoneyTransfer:
    def test_money_transfer(self, db_session: Session,
                            api_manager: ApiManager,
                            create_user_request: CreateUserRequest,
                            created_accounts: tuple[CreateAccountResponse, CreateAccountResponse]):

        account_1, account_2 = created_accounts


        account_1_from_db = Account.get_account_by_id(
            db_session,
            account_1.id
        )
        account_2_from_db = Account.get_account_by_id(
            db_session,
            account_2.id
        )

        assert account_1_from_db is not None, 'Аккаунт 1 отсутствует в БД'
        assert account_2_from_db is not None, 'Аккаунт 2 отсутствует в БД'
        assert account_1_from_db.balance == 0, 'Баланс не равен 0'
        assert account_2_from_db.balance == 0, 'Баланс не равен 0'

        account_1_initial_balance = account_1_from_db.balance
        account_2_initial_balance = account_2_from_db.balance

        deposit_amount = generate_deposit_amount()

        account_1_deposit_request = AccountDepositRequest(
            accountId=account_1.id,
            amount=deposit_amount
        )
        account_1_deposit_response = api_manager.user_steps.account_deposit(
            create_user_request,
            account_1_deposit_request
        )

        db_session.expire_all()

        account_1_from_db_after_deposit = Account.get_account_by_id(
            db_session,
            account_1.id
        )

        account_1_balance_after_deposit = calculate_balance_after_deposit(
            account_1_initial_balance,
            deposit_amount
        )

        assert account_1_from_db_after_deposit is not None, 'Аккаунт 1 отсутствует в БД после пополнения'
        assert account_1_from_db_after_deposit.balance == account_1_balance_after_deposit, 'Баланс аккаунта в БД после пополнения некорректен'

        transfer_amount = generate_transfer_amount(account_1_balance_after_deposit)

        money_transfer_request = MoneyTransferRequest(
            fromAccountId=account_1.id,
            toAccountId=account_2.id,
            amount=transfer_amount
        )

        money_transfer_response = api_manager.user_steps.money_transfer(
            create_user_request,
            money_transfer_request
        )

        db_session.expire_all()

        account_1_from_db_after_transfer = Account.get_account_by_id(
            db_session,
            account_1.id
        )
        account_2_from_db_after_transfer = Account.get_account_by_id(
            db_session,
            account_2.id
        )

        account_1_balance_after_transfer = calculate_account_1_balance_after_transfer(
            account_1_balance_after_deposit,
            transfer_amount
        )
        account_2_balance_after_transfer = calculate_account_2_balance_after_transfer(
            account_2_initial_balance,
            transfer_amount
        )


        assert account_1_from_db_after_transfer is not None, 'Аккаунт 1 отсутствует в БД после перевода денег'
        assert account_2_from_db_after_transfer is not None, 'Аккаунт 2 отсутствует в БД после перевода денег'
        assert account_1_from_db_after_transfer.balance == account_1_balance_after_transfer, 'Баланс аккаунта 1 в БД после перевода денег некорректен'
        assert account_2_from_db_after_transfer.balance == account_2_balance_after_transfer, 'Баланс аккаунта 2 в БД после перевода денег некорректен'


    def test_money_transfer_insufficient_funds(self, db_session: Session,
                            api_manager: ApiManager,
                            create_user_request: CreateUserRequest,
                            created_accounts: tuple[CreateAccountResponse, CreateAccountResponse]):

        account_1, account_2 = created_accounts

        account_1_id = account_1.id
        account_2_id = account_2.id


        account_1_from_db = Account.get_account_by_id(
            db_session,
            account_1_id
        )
        account_2_from_db = Account.get_account_by_id(
            db_session,
            account_2_id
        )

        assert account_1_from_db is not None, 'Аккаунт 1 отсутствует в БД'
        assert account_2_from_db is not None, 'Аккаунт 2 отсутствует в БД'
        assert account_1_from_db.balance == 0, 'Поле баланса для аккаунта 1 отсутствует в БД'
        assert account_2_from_db.balance == 0, 'Поле баланса для аккаунта 2 отсутствует в БД'

        account_1_initial_balance = account_1_from_db.balance
        account_2_initial_balance = account_2_from_db.balance

        deposit_amount = generate_deposit_amount_for_insufficient_funds_transfer()


        account_1_deposit_request = AccountDepositRequest(
            accountId=account_1_id,
            amount=deposit_amount
        )
        account_1_deposit_response = api_manager.user_steps.account_deposit(
            create_user_request,
            account_1_deposit_request
        )

        db_session.expire_all()

        account_1_from_db_after_deposit = Account.get_account_by_id(
            db_session,
            account_1_id
        )

        account_1_balance_after_deposit = calculate_balance_after_deposit(
            account_1_initial_balance,
            deposit_amount
        )

        assert account_1_from_db_after_deposit is not None, 'Аккаунт 1 отсутствует в БД после пополнения'
        assert account_1_from_db_after_deposit.balance == account_1_balance_after_deposit, 'Баланс аккаунта в БД после пополнения некорректен'

        transfer_amount = generate_transfer_amount_exceeding_balance(account_1_balance_after_deposit)

        money_transfer_request = MoneyTransferRequest(
            fromAccountId=account_1_id,
            toAccountId=account_2_id,
            amount=transfer_amount
        )

        money_transfer_response = api_manager.user_steps.money_transfer_insufficient_funds(
            create_user_request,
            money_transfer_request
        )

        db_session.expire_all()

        account_1_from_db_after_transfer = Account.get_account_by_id(
            db_session,
            account_1_id
        )
        account_2_from_db_after_transfer = Account.get_account_by_id(
            db_session,
            account_2_id
        )


        assert account_1_from_db_after_transfer is not None, 'Аккаунт 1 отсутствует в БД после перевода денег'
        assert account_2_from_db_after_transfer is not None, 'Аккаунт 2 отсутствует в БД после перевода денег'
        assert account_1_from_db_after_transfer.balance == account_1_balance_after_deposit, 'Баланс аккаунта 1 в БД после перевода денег некорректен'
        assert account_2_from_db_after_transfer.balance == account_2_initial_balance, 'Баланс аккаунта 2 в БД после перевода денег некорректен'


