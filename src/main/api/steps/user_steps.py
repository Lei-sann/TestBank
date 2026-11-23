import allure

from src.main.api.fixtures.user_fixture import create_user_request
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.money_transfer_request import MoneyTransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps



class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest | CreateCreditUserRequest):
        with allure.step(f"Создание счета для пользователя: {create_user_request.username}"):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_ACCOUNT,
                ResponseSpecs.request_created()
            ).post(create_user_request)
        return response

    def account_deposit(self, create_user_request: CreateUserRequest, account_deposit_request: AccountDepositRequest):
        with allure.step(f"Пополнение счета {account_deposit_request.accountId} "
                         f"на сумму {account_deposit_request.amount}"):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.ACCOUNT_DEPOSIT,
                ResponseSpecs.request_ok()
            ).post(account_deposit_request)
        return response

    def account_deposit_invalid(self, create_user_request: CreateUserRequest, account_deposit_request: AccountDepositRequest):
        with allure.step(f"Некорректное пополнение счета {account_deposit_request.accountId} " 
                         f"на сумму {account_deposit_request.amount}"):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.ACCOUNT_DEPOSIT,
                ResponseSpecs.request_bad()
            ).post(account_deposit_request)
        return response

    def money_transfer(self, create_user_request: CreateUserRequest, money_transfer_request: MoneyTransferRequest):
        with allure.step(
                f"Перевод {money_transfer_request.amount} "
                f"со счёта {money_transfer_request.fromAccountId} "
                f"на счёт {money_transfer_request.toAccountId}"
        ):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.MONEY_TRANSFER,
                ResponseSpecs.request_ok()
            ).post(money_transfer_request)
        return response


    def money_transfer_insufficient_funds(self, create_user_request: CreateUserRequest, money_transfer_request: MoneyTransferRequest):
        with allure.step(
                f"Попытка перевода {money_transfer_request.amount}, "
                f"превышающего доступный баланс, "
                f"со счёта {money_transfer_request.fromAccountId} "
                f"на счёт {money_transfer_request.toAccountId}"
        ):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.MONEY_TRANSFER,
                ResponseSpecs.request_unprocessable_entity()
            ).post(money_transfer_request)
        return response

    def credit_request(self, create_credit_user_request: CreateCreditUserRequest, credit_request: CreditRequest):
        with allure.step(
                f"Запрос кредита на счет {credit_request.accountId} "
                f"на сумму {credit_request.amount} "
                f"на срок {credit_request.termMonths} месяцев"
        ):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
                Endpoint.CREDIT_REQUEST,
                ResponseSpecs.request_created()
            ).post(credit_request)
        return response

    def repeated_credit_request(self, create_credit_user_request: CreateCreditUserRequest, credit_request: CreditRequest):
        with allure.step(
                f"Повторный запрос кредита на счет {credit_request.accountId} "
                f"на сумму {credit_request.amount} "
                f"на срок {credit_request.termMonths} месяцев"
        ):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
                Endpoint.CREDIT_REQUEST,
                ResponseSpecs.request_not_found()
            ).post(credit_request)
        return response

    def credit_repay(self, create_credit_user_request: CreateCreditUserRequest, credit_repay_request: CreditRepayRequest):
        with allure.step(
                f"Погашение кредита {credit_repay_request.creditId} "
                f"со счета {credit_repay_request.accountId} "
                f"на сумму {credit_repay_request.amount}"
        ):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
                Endpoint.CREDIT_REPAY,
                ResponseSpecs.request_ok()
            ).post(credit_repay_request)
        return response

    def partial_credit_repay(self, create_credit_user_request: CreateCreditUserRequest, credit_repay_request: CreditRepayRequest):
        with allure.step(
                f"Попытка частичного погашения кредита {credit_repay_request.creditId} "
                f"со счета {credit_repay_request.accountId} "
                f"на сумму {credit_repay_request.amount}"
        ):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
                Endpoint.CREDIT_REPAY,
                ResponseSpecs.request_unprocessable_entity()
            ).post(credit_repay_request)
        return response


