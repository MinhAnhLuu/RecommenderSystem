from marshmallow import Schema, fields


class OrderDetailSchema(Schema):
    """
        Schema for OrderDetail, NO API
        ************************************
            product_id: Id of Product
            product_name: Name of ordered product
            price: Price of a product
            quantity: Number of ordered products
            currency: Currency in use
        ************************************
    """
    product_id = fields.Str(required=True)
    product_name = fields.Str(required=True)
    price = fields.Decimal(as_string=True)
    quantity = fields.Int()
    currency = fields.Str(required=True)


class OrderSchema(Schema):
    """
        Schema for Order, NO API
        ************************************
            id: Id of Order table in DB
            hash_id: Hashed Id of Order table in DB
            order_details: List of ordered products
        ************************************
    """

    id = fields.Int(required=True)
    hash_id = fields.Str(required=True)
    order_details = fields.Nested(OrderDetailSchema, many=True)
    status = fields.Str()
    customer_id = fields.Str()
