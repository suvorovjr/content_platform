import stripe


class StripeAPIClient:
    """
    Клаас для работы с сервисом Stripe
    """

    def __init__(self, api_key, amount, product_name, currency='rub'):
        """
        Инициализатор класса для работы с сервисом Stripe
        :param api_key: API ключ для работы с сервисом Stripe
        :param amount: Стоимость курса
        :param product_name: Название канала автора
        :param currency: Валюта. По умолчанию это рубли.
        """

        self.api_key = api_key
        self.amount = amount * 100
        self.product_name = product_name
        self.currency = currency
        self.stripe_payment_id = None
        stripe.api_key = self.api_key

    def create_price(self):
        """
        Метод для создание цены на продукт
        :return: ID цены
        """

        response = stripe.Price.create(
            currency=self.currency,
            unit_amount=self.amount,
            recurring={"interval": "month"},
            product_data={"name": self.product_name}
        )

        price_id = response.id
        return price_id

    def create_session(self):
        """
        Метод для создания платежной сессии
        :return: Ссылка на платежную сессию
        """

        response = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[{"price": self.create_price(), "quantity": 1}],
            mode="subscription",
        )
        payment_url = response.url
        self.stripe_payment_id = response.id
        return payment_url

    def get_stripe_payment_id(self):
        """
        Функция для получения stripe id
        :return: stripe id
        """

        return self.stripe_payment_id
