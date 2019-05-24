from marshmallow import Schema, fields


class CreateOrderDetailSchema(Schema):
    """
        Request Schema for OrderDetail, NO API
        ************************************
            product_id: Id of Product
            product_name: Name of ordered product
            price: Price of a product
            quantity: Number of ordered products
            Currency: Currency in use
        ************************************
    """
    product_id = fields.Str(required=True)
    product_name = fields.Str(required=True)
    price = fields.Decimal(as_string=True, required=True)
    quantity = fields.Int(required=True)
    currency = fields.Str(required=True)


class CreateOrderSchema(Schema):
    """
        Request Schema for Order, POST API
        ************************************
            order_details: List of ordered products
        ************************************
    """
    order_details = fields.Nested(
        CreateOrderDetailSchema, many=True, required=True
    )


class ProductSchema(Schema):
    """
        Schema for Product
        ************************************
            id: Id of a product
            title: Name of product
            maximum_speed: Max speed of product
            in_stock: Number of available items
            passenger_capacity: Capacity of a product
        ************************************
    """
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    maximum_speed = fields.Int(required=True)
    in_stock = fields.Int(required=True)
    passenger_capacity = fields.Int(required=True)
    category = fields.Str(required=True)


class CreateProductSchemaList(Schema):
    """
        Request Schema for Product, POST API
        ************************************
            products: List of products with information
        ************************************
    """
    products = fields.Nested(
        ProductSchema, many=True, required=True
    )


class GetOrderSchema(Schema):
    """
        Response Schema for Order, GET API
        ************************************
            id: Id of Order table in DB
            order_details: List of ordered product information
        ************************************
    """
    class OrderDetail(Schema):
        """
            Schema for OrderDetail
            ************************************
                id: Id of OrderDetails table in DB
                quantity: Number of ordered products
                product_name: Name of product
                image: Image URL of product
                price: Price of each product
                product: Product in detail
                currency: Currency in use
            ************************************
        """

        id = fields.Str()
        quantity = fields.Int()
        product_name = fields.Str()
        image = fields.Str()
        price = fields.Decimal(as_string=True)
        product = fields.Nested(ProductSchema, many=False)
        currency = fields.Str()

    id = fields.Str(required=True)
    order_details = fields.Nested(OrderDetail, many=True)
