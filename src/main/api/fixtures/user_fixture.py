import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def created_account(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

@pytest.fixture
def created_accounts(api_manager, create_user_request):
    account_1 = api_manager.user_steps.create_account(create_user_request)
    account_2 = api_manager.user_steps.create_account(create_user_request)
    return account_1, account_2

@pytest.fixture
def created_credit_account(api_manager, create_credit_user_request):
    return api_manager.user_steps.create_account(create_credit_user_request)


